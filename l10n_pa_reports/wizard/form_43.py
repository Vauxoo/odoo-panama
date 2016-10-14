# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>

import base64
import csv
import time
import os
import tempfile

from openerp import fields, models, api, _


class AccountForm43Report(models.TransientModel):
    """Formulario 43"""

    _name = 'account.pa.form43.report'

    form43_columns = [
        'entity', 'vat', 'dv', 'name', 'supplier_invoice_number', 'date',
        'concept', 'type', 'subtotal', 'tax']

    name = fields.Char(readonly=True)
    company_id = fields.Many2one(
        'res.company', 'Company', required=True,
        default=lambda self: self.env.user.company_id)
    filename = fields.Char(
        size=128, readonly=True, help='This is File name')
    file_txt = fields.Binary(
        readonly=True, help='This file, you can import the SAT')
    state = fields.Selection(
        [('choose', 'Choose'), ('get', 'Get'), ('not_file', 'Not File')],
        default='choose')
    period_id = fields.Many2one(
        'account.period', 'Period', required=True)

    @api.multi
    def create_form43(self):
        """This function create the file for report to Form 43"""
        ai_obj = self.env['account.invoice']

        domain_args = [
            ('type', '=', 'in_invoice'),
            ('period_id', '=', self.period_id.id),
            ('state', 'in', ['open', 'paid']),
        ]
        lines_form43 = ai_obj.search(domain_args)

        dict_return = {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'res_model': 'account.pa.form43.report',
            'target': 'new',
        }
        if not lines_form43:
            self.write({'state': 'not_file'})
            return dict_return

        data_lines, partner_ids, invoice_ids = lines_form43.get_data()
        if partner_ids:
            return {
                'name': _('Partners to fix Data for Form 43'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'res.partner',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', partner_ids)],
            }
        if invoice_ids:
            return {
                'name': _('Invoices to fix Data for Form 43'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.invoice',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', invoice_ids)],
            }
        name = "Informe43_%s_%s.%s"
        ruc = self.company_id.partner_id.vat_alone or 'fix-ruc-on-company'
        period = time.strftime(
            '%Y%m', time.strptime(self.period_id.date_start, '%Y-%m-%d'))
        txt = self._get_file_txt(data_lines)
        self.write({
            'state': 'get',
            'file_txt': txt,
            'filename': name % (ruc, period, 'txt'),
        })
        return dict_return

    @api.model
    def _get_file_txt(self, dict_data):
        (fileno, fname) = tempfile.mkstemp('.txt', 'tmp')
        os.close(fileno)
        f_write = open(fname, 'wb')
        fcsv = csv.DictWriter(f_write, self.form43_columns, delimiter='\t')
        small_dict = {}
        for form43 in dict_data:
            for f43c in self.form43_columns:
                small_dict[f43c] = form43[f43c]
            fcsv.writerow(small_dict)
        f_write.close()
        with open(fname, "rb") as f_read:
            fdata = f_read.read()
            out = base64.encodestring(fdata)
        return out

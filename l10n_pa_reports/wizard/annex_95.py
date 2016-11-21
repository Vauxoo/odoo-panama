# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>

import base64
import csv
import time
import os
import tempfile

from openerp import fields, models, api


class AccountAnnex95Report(models.TransientModel):
    """Anexo 95"""

    _name = 'account.pa.annex95.report'

    annex95_columns = [
        'entity', 'vat', 'dv', 'name', 'invoice_number', 'wh_line',
        'tax_amount', 'subject', 'wh_amount']

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
    def create_annex95(self):
        """This function create the file for report to Annex 95"""
        aitw_obj = self.env['account.invoice.tax.wh']

        domain_args = [
            ('invoice_id.type', '=', 'out_invoice'),
            ('invoice_id.period_id', '=', self.period_id.id),
            ('invoice_id.state', 'in', ['open', 'paid']),
        ]
        lines_annex95 = aitw_obj.search(domain_args)

        dict_return = {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'res_model': 'account.pa.annex95.report',
            'target': 'new',
        }
        if not lines_annex95:
            self.write({'state': 'not_file'})
            return dict_return

        data_lines = lines_annex95.get_data()

        name = "Anexo95_%s_%s.%s"
        ruc = self.company_id.partner_id.vat_alone or 'fix-ruc-on-company'
        period = time.strftime(
            '%Y%m', time.strptime(self.period_id.date_start, '%Y-%m-%d'))
        txt = self._get_file_txt_annex95(data_lines)
        self.write({
            'state': 'get',
            'file_txt': txt,
            'filename': name % (ruc, period, 'txt'),
        })
        return dict_return

    @api.model
    def _get_file_txt_annex95(self, dict_data):
        (fileno, fname) = tempfile.mkstemp('.txt', 'tmp')
        os.close(fileno)
        f_write = open(fname, 'wb')
        fcsv = csv.DictWriter(f_write, self.annex95_columns, delimiter='\t')
        small_dict = {}
        for annex95 in dict_data:
            for col in self.annex95_columns:
                small_dict[col] = annex95[col]
            fcsv.writerow(small_dict)
        f_write.close()
        with open(fname, "rb") as f_read:
            fdata = f_read.read()
            out = base64.encodestring(fdata)
        return out

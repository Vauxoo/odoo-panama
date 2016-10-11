# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>

import base64
import cgi
import csv
import logging
import time
import os
import tempfile
import StringIO

from openerp import fields, models, api, _
_logger = logging.getLogger(__name__)

try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')


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
    filename_csv = fields.Char(size=128, readonly=True)
    filename_xls = fields.Char('File name', size=128, readonly=True)
    file_txt = fields.Binary(
        readonly=True, help='This file, you can import the SAT')
    file_csv = fields.Binary(
        readonly=True, help='Download information on CSV')
    file_xls = fields.Binary(
        readonly=True,
        help='It will open in your excel program, to validate numbers')
    state = fields.Selection(
        [('choose', 'Choose'), ('get', 'Get'), ('not_file', 'Not File')],
        default='choose')
    period_id = fields.Many2one(
        'account.period', 'Period', required=True)

    @api.model
    def csv2xls(self, csv_content):
        wbk = xlwt.Workbook(encoding='UTF-8')
        xls_path = tempfile.NamedTemporaryFile(suffix='.xls', delete=False)
        cur_format = xlwt.XFStyle()
        cur_format.num_format_str = '$#,##0.00'
        wsh = wbk.add_sheet('form43')
        wsh._cell_overwrite_ok = True
        spam_reader = csv.reader(
            StringIO.StringIO(base64.decodestring(csv_content)))
        for rowx, row in enumerate(spam_reader):
            for colx, value in enumerate(row):
                wsh.write(rowx, colx, value)
                if rowx > 0 and colx >= 7:
                    try:
                        wsh.write(
                            rowx, colx, float(value), style=cur_format)
                    except ValueError:
                        pass
        wbk.save(xls_path.name)
        return base64.encodestring(open(xls_path.name, 'r').read())

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
        name = name % (ruc, period, '%s')
        txt = self._get_file_txt(data_lines)
        csv_file = self._get_file_csv(data_lines)
        file_xls = self.csv2xls(csv_file)
        self.write({
            'state': 'get',
            'file_txt': txt,
            'file_csv': csv_file,
            'filename': name % 'txt',
            'filename_csv': name % 'cvs',
            'file_xls': file_xls,
            'filename_xls': name % 'xls',
        })
        return dict_return

    @api.model
    def str_format(self, text):
        if text:
            return cgi.escape(text, True).encode(
                'ascii', 'xmlcharrefreplace').replace('\n\n', ' ')

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

    def _get_file_csv(self, dict_data):
        (fileno, fname_csv) = tempfile.mkstemp('.csv', 'tmp_csv')
        os.close(fileno)
        f_write_csv = open(fname_csv, 'wb')
        fcsv_csv = csv.DictWriter(
            f_write_csv, self.form43_columns, delimiter=',')
        fcsv_csv.writerow({
            'entity': 'Tipo de Persona',
            'vat': 'RUC',
            'dv': 'DV',
            'name': 'Nombre o Razon Social',
            'supplier_invoice_number': 'Factura',
            'date': 'Fecha',
            'concept': 'Concepto',
            'type': 'Compra de Bienes y Servicios',
            'subtotal': 'Monto en Balboas',
            'tax': 'ITBMS Pagado en Balboas',
        })
        f_write_csv.close()
        with open(fname_csv, "rb") as f_read_csv:
            fdata_csv = f_read_csv.read()
            out_csv = base64.encodestring(fdata_csv)
        return out_csv

# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>

import base64
from openerp import fields
from openerp.tests.common import TransactionCase


class TestAccountPaAnnex95Report(TransactionCase):

    def setUp(self):
        super(TestAccountPaAnnex95Report, self).setUp()
        self.invoice_obj = self.env['account.invoice']
        self.partner_obj = self.env['res.partner']
        self.partner_id = self.partner_obj.browse(
            self.ref('l10n_pa_reports.res_partner_panama'))
        self.annex95_obj = self.env['account.pa.annex95.report']
        self.date = fields.Datetime.from_string(fields.Datetime.now())
        self.date = self.date.replace(day=1)
        if self.date.month % 12 == 0:
            self.date = self.date.replace(month=11)
        else:
            self.date = self.date.replace(month=self.date.month + 1)
        self.period_id = self.ref(
            'account.period_%s' % self.date.month)
        self.company_id = self.ref('base.main_company')
        self.date_str = fields.Datetime.to_string(self.date)
        self.inv_obj = self.env['account.invoice']
        self.invoice_id = self.inv_obj.browse(
            self.ref('l10n_pa_reports.demo_invoice_1'))
        self.invoice_id.date_invoice = fields.Datetime.to_string(self.date)
        self.filename = "Anexo95_fix-ruc-on-company_%s%s.txt" % (
            self.date.year, self.date.month)

    def test_001_annex95_without_txt(self):
        """Send to generate annex95 report without movements"""
        wizard = self.annex95_obj.create({
            'period_id': self.period_id,
            'company_id': self.company_id,
        })
        wizard.create_annex95()
        self.assertFalse(wizard.file_txt, "File generated without documents.")
        self.assertEqual(
            wizard.state, 'not_file', "Wrong State on Wizard")
        return True

    def test_002_create_txt_file(self):
        """Create a txt file for Form 95"""
        self.invoice_id.company_id.wh_sale_itbms_account_id = self.ref(
            'account.iva')
        self.invoice_id.company_id.wh_sale_itbms_journal_id = self.ref(
            'account.miscellaneous_journal')
        self.invoice_id.signal_workflow('invoice_open')
        self.assertEquals(
            bool(self.invoice_id.wh_move_id), True,
            'Journal Entry for Withholding should be Filled')
        wizard = self.annex95_obj.create({
            'period_id': self.period_id,
            'company_id': self.company_id,
        })
        wizard.create_annex95()
        self.assertEqual(wizard.filename, self.filename,
                         'There should be a File here!')
        wh_txt = base64.decodestring(wizard.file_txt).split('\n')
        self.assertEqual(len(wh_txt), 2, 'There should be Two lines in File')
        wh_txt = wh_txt[0]
        wh_exp = ('J\t123456-7-890123\t40\tPanamanian Partner (test)\t9XU3974'
                  '\t4000.0\t280.0\t4\t140.0\r')
        self.assertEqual(wh_txt, wh_exp, 'Unexpected TXT File')
        return True

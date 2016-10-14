# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>

from openerp import fields
from openerp.tests.common import TransactionCase


class TestAccountPaForm43Report(TransactionCase):

    def setUp(self):
        super(TestAccountPaForm43Report, self).setUp()
        self.invoice_obj = self.env['account.invoice']
        self.partner_obj = self.env['res.partner']
        self.partner_id = self.partner_obj.browse(
            self.ref('l10n_pa_reports.res_partner_panama'))
        self.form43_obj = self.env['account.pa.form43.report']
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
            self.ref('l10n_pa_reports.demo_invoice_0'))
        self.invoice_id.date_invoice = fields.Datetime.to_string(self.date)
        self.filename = "Informe43_fix-ruc-on-company_%s%s.txt" % (
            self.date.year, self.date.month)

    def test_001_form43_without_txt(self):
        """Send to generate form43 report without movements"""
        wizard = self.form43_obj.create({
            'period_id': self.period_id,
            'company_id': self.company_id,
        })
        wizard.create_form43()
        self.assertFalse(wizard.file_txt, "File generated without documents.")

    def test_002_create_txt_file(self):
        """Create a txt file for Form 43"""
        self.invoice_id.signal_workflow('invoice_open')
        wizard = self.form43_obj.create({
            'period_id': self.period_id,
            'company_id': self.company_id,
        })
        wizard.create_form43()
        self.assertEqual(wizard.filename, self.filename)

    def test_003_partners_to_fix(self):
        """Cannot create txt because of Partners to fix Form 43"""
        self.partner_id.l10n_pa_entity = False
        self.invoice_id.signal_workflow('invoice_open')
        wizard = self.form43_obj.create({
            'period_id': self.period_id,
            'company_id': self.company_id,
        })
        res = wizard.create_form43()
        self.assertEqual(
            res.get('domain'),
            [('id', 'in', [self.partner_id.id])])

    def test_004_invoices_to_fix(self):
        """Cannot create txt because of Invoices to fix Form 43"""
        self.invoice_id.l10n_pa_concept = False
        self.invoice_id.signal_workflow('invoice_open')
        wizard = self.form43_obj.create({
            'period_id': self.period_id,
            'company_id': self.company_id,
        })
        res = wizard.create_form43()
        self.assertEqual(
            res.get('domain'),
            [('id', 'in', [self.invoice_id.id])])

    def test_005_foreign_partner(self):
        """create txt for Foreign Partner in Form 43"""
        self.partner_id.l10n_pa_entity = 'E'
        self.invoice_id.signal_workflow('invoice_open')
        wizard = self.form43_obj.create({
            'period_id': self.period_id,
            'company_id': self.company_id,
        })
        wizard.create_form43()
        self.assertEqual(wizard.filename, self.filename)

# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>

from openerp import fields
from openerp.tests.common import TransactionCase


class TestAccountPaForm43Report(TransactionCase):

    def setUp(self):
        super(TestAccountPaForm43Report, self).setUp()
        self.invoice_obj = self.env['account.invoice']
        self.partner = self.env.ref('l10n_pa_reports.res_partner_panama')
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

    def test_001_form43_without_moves(self):
        """Send to generate form43 report without movements"""
        wizard = self.form43_obj.create({
            'period_id': self.period_id,
            'company_id': self.company_id,
        })
        wizard.create_form43()
        self.assertFalse(wizard.file_txt, "File generated without documents.")

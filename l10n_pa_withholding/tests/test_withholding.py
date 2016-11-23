# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>

from openerp.exceptions import except_orm
from openerp.tests.common import TransactionCase


class TestWithholding(TransactionCase):

    def setUp(self):
        super(TestWithholding, self).setUp()
        self.so_obj = self.env['sale.order']
        self.sapi_obj = self.env['sale.advance.payment.inv']
        self.inv_obj = self.env['account.invoice']
        self.sio_obj = self.env['stock.invoice.onshipping']
        self.sale_id = self.ref('l10n_pa_withholding.so_01')
        self.sale_brw = self.so_obj.browse(self.sale_id)
        self.refund_wzd_obj = self.env['account.invoice.refund']

    def create_invoice_from_sales_order(self, sale_id):
        sapi_brw = self.sapi_obj.create({'advance_payment_method': 'all'})
        context = {'open_invoices': True, 'active_ids': [sale_id]}
        res = sapi_brw.with_context(context).create_invoices()
        return self.inv_obj.browse(res['res_id'])

    def test_01_propagate_fiscal_info_from_so_to_inv(self):
        """Test that fiscal info is passed on to newly created invoice"""
        self.sale_brw.action_button_confirm()
        self.assertEquals(self.sale_brw.state, 'manual', 'Wrong State on SO')
        inv = self.create_invoice_from_sales_order(self.sale_id)
        self.assertEquals(
            inv.wh_agent_itbms, True,
            'This should be a Withholding Agent - True')
        self.assertEquals(
            inv.l10n_pa_wh_subject, 'na',
            'This should be "No Aplica" - "na"')
        return True

    def test_02_create_an_invoice_with_without_wh(self):
        """Test withholding in an invoice without taxes"""
        self.sale_brw.l10n_pa_wh_subject = '7'
        self.sale_brw.action_button_confirm()
        self.assertEquals(self.sale_brw.state, 'manual', 'Wrong State on SO')
        inv = self.create_invoice_from_sales_order(self.sale_id)
        inv.signal_workflow('invoice_open')
        self.assertEquals(
            inv.state, 'open', 'Wrong State on Invoice it should be "open"')
        self.assertEquals(
            bool(inv.wh_move_id), False,
            'Journal Entry for Withholding should be Empty')

        inv.journal_id.update_posted = True

        inv.signal_workflow('invoice_cancel')

        self.assertEquals(
            inv.state, 'cancel',
            'State should be "cancel" on Invoice')
        self.assertEquals(
            bool(inv.wh_move_id), False,
            'Journal Entry for Withholding should be Empty')

        self.assertEquals(
            len(inv.wh_tax_line), 0,
            'Invoice Should not have any Withholding Lines')

        inv.action_cancel_draft()
        self.assertEquals(
            inv.state, 'draft',
            'State should be "draft" on Invoice')

        return True

    def test_02_create_an_invoice_without_tax_with_wh_tdc(self):
        """Test withholding in an invoice without taxes and Withholding Subject
        is TDD/TDC"""
        sale_id = self.ref('l10n_pa_withholding.so_05')
        sale_brw = self.so_obj.browse(sale_id)

        sale_brw.action_button_confirm()
        self.assertEquals(sale_brw.state, 'manual', 'Wrong State on SO')
        inv = self.create_invoice_from_sales_order(sale_id)

        self.assertEquals(
            inv.l10n_pa_wh_subject, '5', 'Withholding Concept Should be "5"')

        inv.signal_workflow('invoice_open')

        self.assertEquals(
            inv.state, 'open', 'Wrong State on Invoice it should be "open"')

        self.assertEquals(
            bool(inv.wh_move_id), True,
            'Journal Entry for Withholding should be Filled')

        # /!\ NOTE: Assert amount withheld
        inv.withholding_reconciliation()
        self.assertEquals(
            inv.residual, 98.0,
            'Residual should be 98.0')

        inv.journal_id.update_posted = True
        inv.wh_move_id.journal_id.update_posted = True

        inv.signal_workflow('invoice_cancel')

        self.assertEquals(
            inv.state, 'cancel',
            'State should be "cancel" on Invoice')
        self.assertEquals(
            bool(inv.wh_move_id), False,
            'Journal Entry for Withholding should be Empty')

        self.assertEquals(
            len(inv.wh_tax_line), 0,
            'Invoice Should not have any Withholding Lines')

        inv.action_cancel_draft()
        self.assertEquals(
            inv.state, 'draft',
            'State should be "draft" on Invoice')

        return True

    def test_03_create_an_invoice_with_taxes_no_wh(self):
        """Test withholding in invoice with taxes but wh_agent_itbms=False"""
        sale_id = self.ref('l10n_pa_withholding.so_02')
        sale_brw = self.so_obj.browse(sale_id)

        sale_brw.wh_agent_itbms = False
        sale_brw.action_button_confirm()

        inv = self.create_invoice_from_sales_order(sale_id)
        inv.signal_workflow('invoice_open')
        self.assertEquals(
            bool(inv.wh_move_id), False,
            'Journal Entry for Withholding should be Empty')
        return True

    def test_04_create_an_invoice_with_exempt_no_wh(self):
        """Test Withholding in exempt taxed invoice and wh_agent_itbms=True"""
        sale_id = self.ref('l10n_pa_withholding.so_03')
        sale_brw = self.so_obj.browse(sale_id)

        sale_brw.action_button_confirm()

        inv = self.create_invoice_from_sales_order(sale_id)
        inv.signal_workflow('invoice_open')
        self.assertEquals(
            bool(inv.wh_move_id), False,
            'Journal Entry for Withholding should be Empty')

        inv.withholding_reconciliation()

        aml_ids = [line.id for line in inv.payment_ids]
        self.assertEquals(
            len(aml_ids), 0,
            'There should be no payment in the Invoice after reconciling')

        return True

    def test_05_create_an_invoice_with_taxes_wh(self):
        """Test withholding in invoice with taxes and wh_agent_itbms=True"""
        sale_id = self.ref('l10n_pa_withholding.so_02')
        sale_brw = self.so_obj.browse(sale_id)

        sale_brw.action_button_confirm()

        inv = self.create_invoice_from_sales_order(sale_id)
        inv.signal_workflow('invoice_open')
        self.assertEquals(
            bool(inv.wh_move_id), True,
            'Journal Entry for Withholding should be Filled')

        aml_ids = [True
                   for line in inv.wh_move_id.line_id
                   if line.account_id.id == inv.account_id.id and
                   line.credit > 0]
        self.assertEquals(
            any(aml_ids), True,
            'Withholding Invoice should decrease Receivable on Customer')

        inv.withholding_reconciliation()

        aml_ids = [line.id for line in inv.payment_ids]
        self.assertEquals(
            len(aml_ids), 1,
            'There should be a payment in the Invoice after reconciling')

        inv.journal_id.update_posted = True
        inv.wh_move_id.journal_id.update_posted = True
        wh_move_name = inv.wh_move_id.name

        inv.signal_workflow('invoice_cancel')

        self.assertEquals(
            inv.state, 'cancel',
            'State should be "cancel" on Invoice')
        self.assertEquals(
            bool(inv.wh_move_id), False,
            'Journal Entry for Withholding should be Empty')

        self.assertEquals(
            len(inv.wh_tax_line), 0,
            'Invoice Should not have any Withholding Lines')

        inv.action_cancel_draft()
        self.assertEquals(
            inv.state, 'draft',
            'State should be "draft" on Invoice')

        inv.signal_workflow('invoice_open')
        self.assertEquals(
            inv.state, 'open',
            'State should be "open" on Invoice')

        self.assertEquals(
            inv.wh_move_id.name, wh_move_name,
            'Journal Entry name should not have changed')

        return True

    def test_05_create_an_invoice_with_taxes_wh_no_receivable(self):
        """Test withholding in invoice with taxes and wh_agent_itbms=True
        And there is no change on Customer's Receivable Account"""
        sale_id = self.ref('l10n_pa_withholding.so_04')
        sale_brw = self.so_obj.browse(sale_id)

        sale_brw.action_button_confirm()

        inv = self.create_invoice_from_sales_order(sale_id)
        inv.signal_workflow('invoice_open')
        self.assertEquals(
            bool(inv.wh_move_id), True,
            'Journal Entry for Withholding should be Filled')

        inv.withholding_reconciliation()
        aml_ids = [line.id for line in inv.payment_ids]
        self.assertEquals(
            len(aml_ids), 0,
            'There should be no payment in the Invoice after reconciling')

        aml_ids = [True
                   for line in inv.wh_move_id.line_id
                   if line.account_id.id == inv.account_id.id]
        self.assertEquals(
            any(aml_ids), False,
            'Withholding Invoice should not change Receivable on Customer')

        aml_ids = [True
                   for line in inv.wh_move_id.line_id
                   if line.account_id.id != inv.account_id.id]
        self.assertEquals(
            len(aml_ids), 2,
            'Withholding Invoice should have Two Journal Items')

        inv.journal_id.update_posted = True
        inv.wh_move_id.journal_id.update_posted = True

        inv.signal_workflow('invoice_cancel')

        self.assertEquals(
            inv.state, 'cancel',
            'State should be "cancel" on Invoice')
        self.assertEquals(
            bool(inv.wh_move_id), False,
            'Journal Entry for Withholding should be Empty')

        self.assertEquals(
            len(inv.wh_tax_line), 0,
            'Invoice Should not have any Withholding Lines')

        inv.action_cancel_draft()
        self.assertEquals(
            inv.state, 'draft',
            'State should be "draft" on Invoice')

        return True

    def test_06_apply_wh_on_a_refund(self):
        """Test withholding in a refund"""
        sale_id = self.ref('l10n_pa_withholding.so_02')
        sale_brw = self.so_obj.browse(sale_id)

        sale_brw.action_button_confirm()

        inv = self.create_invoice_from_sales_order(sale_id)
        inv.signal_workflow('invoice_open')

        refund_id = self.refund_wzd_obj.with_context(
            {'active_ids': [inv.id]}).create({
                'filter_refund': 'refund',
            })
        refund_id = refund_id.invoice_refund()
        refund_id = refund_id.get('domain')[1][2]
        refund_brw = self.inv_obj.browse(refund_id)

        self.assertEquals(
            refund_brw.wh_agent_itbms, True,
            'This should not be a Withholding Agent - True')
        self.assertEquals(
            refund_brw.l10n_pa_wh_subject, '7',
            'This should be "7"')

        refund_brw.signal_workflow('invoice_open')

        self.assertEquals(
            refund_brw.state, 'open',
            'State should be "open" on Refund')
        self.assertEquals(
            bool(refund_brw.wh_move_id), True,
            'Journal Entry for Withholding should be Filled on Refund')

        aml_refund_ids = [True
                          for line in refund_brw.wh_move_id.line_id
                          if line.account_id.id == inv.account_id.id and
                          line.debit > 0]
        self.assertEquals(
            any(aml_refund_ids), True,
            'Withholding Refund should increase Receivable on Customer')
        return True

    def test_07_accounting_info_on_company_journal(self):
        """Test withholding in invoice with taxes and wh_agent_itbms=True
        Missing Accounting Information on Company (Journal)"""
        sale_id = self.ref('l10n_pa_withholding.so_02')
        sale_brw = self.so_obj.browse(sale_id)

        sale_brw.action_button_confirm()

        inv = self.create_invoice_from_sales_order(sale_id)
        inv.company_id.wh_sale_itbms_account_id = False
        inv.company_id.wh_sale_itbms_journal_id = False

        with self.assertRaises(except_orm):
            inv.signal_workflow('invoice_open')
        return True

    def test_07_accounting_info_on_company_account(self):
        """Test withholding in invoice with taxes and wh_agent_itbms=True
        Missing Accounting Information on Company (Account)"""
        sale_id = self.ref('l10n_pa_withholding.so_02')
        sale_brw = self.so_obj.browse(sale_id)

        sale_brw.action_button_confirm()

        inv = self.create_invoice_from_sales_order(sale_id)

        inv.company_id.wh_sale_itbms_account_id = False

        with self.assertRaises(except_orm):
            inv.signal_workflow('invoice_open')
        return True

    def test_08_no_wh_subject_set(self):
        """Test withholding in invoice with taxes and wh_agent_itbms=True
        No Withholding Subject set in the Invoice"""
        sale_id = self.ref('l10n_pa_withholding.so_02')
        sale_brw = self.so_obj.browse(sale_id)

        sale_brw.action_button_confirm()

        inv = self.create_invoice_from_sales_order(sale_id)
        inv.l10n_pa_wh_subject = False

        with self.assertRaises(except_orm):
            inv.signal_workflow('invoice_open')

        return True

    def test_09_create_an_exempt_invoice_with_taxes_no_wh(self):
        """Test withholding in exempt invoice with taxes and
        wh_agent_itbms=True"""
        sale_id = self.ref('l10n_pa_withholding.so_02')
        sale_brw = self.so_obj.browse(sale_id)

        sale_brw.action_button_confirm()

        inv = self.create_invoice_from_sales_order(sale_id)
        inv.l10n_pa_wh_subject = 'na'
        inv.signal_workflow('invoice_open')
        self.assertEquals(
            bool(inv.wh_move_id), False,
            'Journal Entry for Withholding should be Empty')
        return True

    def test_10_already_withheld_invoice(self):
        """Test Already Withheld Invoice"""
        sale_id = self.ref('l10n_pa_withholding.so_02')
        sale_brw = self.so_obj.browse(sale_id)

        sale_brw.action_button_confirm()

        inv = self.create_invoice_from_sales_order(sale_id)
        inv.signal_workflow('invoice_open')
        wh_move_id_1 = inv.wh_move_id.id
        inv.action_move_create_withholding()
        wh_move_id_2 = inv.wh_move_id.id
        self.assertEquals(
            wh_move_id_2, wh_move_id_1,
            'Journal Entry for Withholding should be the same')
        return True

    def test_11_propagate_fiscal_info_from_so_to_inv_via_picking(self):
        """Test that fiscal info is passed on to newly created invoice when
        invoicing from picking"""

        self.sale_brw.order_policy = 'picking'
        self.sale_brw.wh_agent_itbms = False
        self.sale_brw.l10n_pa_wh_subject = '7'
        self.sale_brw.action_button_confirm()
        self.assertEquals(self.sale_brw.state, 'progress', 'Wrong State on SO')

        picking = self.sale_brw.picking_ids
        self.assertEqual(1, len(picking))
        picking.action_done()

        sio_wzd = self.sio_obj.with_context({
            'active_id': picking.id,
            'active_ids': [picking.id],
        }).create({})
        inv = self.inv_obj.browse(sio_wzd.create_invoice())
        self.assertEquals(
            inv.wh_agent_itbms, False,
            'This should not be a Withholding Agent - False')
        self.assertEquals(
            inv.l10n_pa_wh_subject, '7',
            'This should be "7"')
        return True

    def test_12_on_change_partner_id_on_sale_order(self):
        """Test setting null partner on Sales Order"""
        res = self.registry('sale.order').onchange_partner_id(
            self.cr, self.uid, False, False, {})
        self.assertEquals(
            res['value']['wh_agent_itbms'], False,
            'This should be a Withholding Agent - True')
        self.assertEquals(
            res['value']['l10n_pa_wh_subject'], False,
            'This should be "Empty" - "False"')
        return True

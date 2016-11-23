# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
from __future__ import division
from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import except_orm


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = ['account.invoice', 'l10n.pa.common.abstract']
    wh_move_id = fields.Many2one(
        'account.move',
        string='Withholding Journal Entry',
        readonly=True,
        index=True,
        copy=False,
        help="Link to the automatically generated Withholding Journal Entry.")
    wh_move_name = fields.Char(
        'Withholding Name', copy=False, help='Withholding Name')
    wh_tax_line = fields.One2many(
        'account.invoice.tax.wh', 'invoice_id', string='Wh Tax Lines',
        readonly=True, copy=False, help='Withheld Tax Lines')

    @api.model
    def wh_move_line_get_item(self, line):
        sign = -1 if 'out' in line.invoice_id.type else 1
        return {
            'type': 'src',
            'name': line.name.split('\n')[0][:64],
            'account_id': line.account_id.id,
            'price': sign * line.wh_amount,
            'tax_code_id': line.tax_code_id.id,
            'tax_amount': line.amount,
        }

    @api.model
    def wh_line_get_convert(self, line, part, date):
        return {
            'partner_id': part,
            'name': line['name'][:64],
            'date': date,
            'debit': line['price'] > 0 and line['price'],
            'credit': line['price'] < 0 and -line['price'],
            'account_id': line['account_id'],
            'analytic_lines': line.get('analytic_lines', []),
            'amount_currency': line['price'] > 0 and abs(
                line.get('amount_currency', False)) or -abs(
                    line.get('amount_currency', False)),
            'currency_id': line.get('currency_id', False),
            'tax_code_id': line.get('tax_code_id', False),
            'tax_amount': line.get('tax_amount', False),
            'ref': line.get('ref', False),
            'analytic_account_id': line.get('account_analytic_id', False),
            # 'tax_line_id': line.get('tax_line_id', False),
        }

    @api.model
    def wh_move_line_get(self):
        # /!\ TODO: Invoice to be ommited for Withholding
        # return []
        # /!\ TODO: Determine if withholding will proceed because of the
        # Withholding Agent Entitlement
        res = []
        for tax_brw in self.wh_tax_line:
            res.append(self.wh_move_line_get_item(tax_brw))
        return res

    @api.multi
    def action_move_create_withholding(self):
        """Creates Withholding for taxes in invoice"""
        account_move = self.env['account.move']
        aitw_obj = self.env['account.invoice.tax.wh']

        for invoice_brw in self:
            if invoice_brw.type not in ('out_invoice', 'out_refund'):
                continue
            if not invoice_brw.wh_agent_itbms:
                continue
            if invoice_brw.wh_move_id:
                continue
            if not invoice_brw.l10n_pa_wh_subject:
                raise except_orm(
                    _('Error!'),
                    _('Please define a Withholding Subject to this invoice.'))
            if invoice_brw.l10n_pa_wh_subject == 'na':
                continue
            wh_basis = aitw_obj.wh_subject_mapping(
                invoice_brw.l10n_pa_wh_subject).get('basis')

            # There is a precondition which states that a document will be
            # withheld depending on the type of withholding subject.
            # If the withholding concept is `5` or `6` the withholding is to
            # be applied based on invoice_total
            if not invoice_brw.tax_line and wh_basis != 'total':
                continue

            journal = invoice_brw.company_id.wh_sale_itbms_journal_id
            if not journal:
                raise except_orm(
                    _('Error!'),
                    _('Please Define a Journal to be used for withholding '
                      'ITBMS on Customer Invoice on Your Company.'))

            for aitw in aitw_obj.compute(invoice_brw).values():
                aitw_obj.create(aitw)

            if not invoice_brw.wh_tax_line:
                continue

            ctx = dict(self._context, lang=invoice_brw.partner_id.lang)
            date = invoice_brw.date_invoice

            ref = invoice_brw.reference or invoice_brw.name,
            company_currency = invoice_brw.company_id.currency_id
            ait = invoice_brw.wh_move_line_get()

            total, total_currency, ait = invoice_brw.with_context(
                ctx).compute_invoice_totals(company_currency, ref, ait)

            if total:
                company_currency = invoice_brw.company_id.currency_id
                diff_curr = invoice_brw.currency_id != company_currency
                ait.append({
                    'type': 'dest',
                    'name': _('ITBMS Withheld on Invoice'),
                    'price': total,
                    'account_id': invoice_brw.account_id.id,
                    'date_maturity': invoice_brw.date_due,
                    'amount_currency': diff_curr and total_currency,
                    'currency_id': diff_curr and invoice_brw.currency_id.id,
                    'ref': ref
                })

            part = self.env['res.partner']._find_accounting_partner(
                invoice_brw.partner_id)

            line = [
                (0, 0,
                 self.wh_line_get_convert(l, part.id, date)) for l in ait]

            move_vals = {
                'ref': invoice_brw.reference or invoice_brw.name,
                'line_id': line,
                'journal_id': journal.id,
                'date': date,
                'company_id': invoice_brw.company_id.id,
            }
            ctx['company_id'] = invoice_brw.company_id.id

            if invoice_brw.wh_move_name:
                move_vals['name'] = invoice_brw.wh_move_name

            move_vals['period_id'] = invoice_brw.period_id.id
            for i in line:
                i[2]['period_id'] = invoice_brw.period_id.id

            ctx_nolang = ctx.copy()
            ctx_nolang.pop('lang', None)
            move = account_move.with_context(ctx_nolang).create(move_vals)
            move.post()

            invoice_brw.write({
                'wh_move_id': move.id,
                'wh_move_name': move.name,
            })
        return True

    @api.multi
    def withholding_reconciliation(self):
        """Reconciles Journal Items from wh_move_id with those in move_id on
        Invoice"""

        for inv_brw in self:
            move_ids = [move.id or False
                        for move in (inv_brw.move_id, inv_brw.wh_move_id)]

            if not all(move_ids):
                continue

            line_ids = [line.id
                        for move2 in (inv_brw.move_id, inv_brw.wh_move_id)
                        for line in move2.line_id
                        if line.account_id.id == inv_brw.account_id.id]

            if len(line_ids) < 2:
                continue

            # /!\ NOTE: There could be some payments in the invoice let us
            # reconcile them too
            line_ids += [lin2.id for lin2 in inv_brw.payment_ids]
            line_ids = list(set(line_ids))

            line_ids = self.env['account.move.line'].browse(line_ids)
            line_ids.reconcile_partial()

        return True

    @api.multi
    def action_cancel(self):
        moves = self.env['account.move']
        for inv_brw in self:
            inv_brw.wh_tax_line.unlink()
            if not inv_brw.wh_move_id:
                continue

            if not inv_brw.payment_ids:
                moves += inv_brw.wh_move_id
                continue

            wh_line_ids = [line.id
                           for line in inv_brw.wh_move_id.line_id
                           if line.account_id.id == inv_brw.account_id.id]

            pay_line_ids = [line.id for line in inv_brw.payment_ids
                            if line.id not in wh_line_ids]

            if not pay_line_ids:
                moves += inv_brw.wh_move_id
                self._remove_move_reconcile(list(wh_line_ids))
                continue

        if moves:
            moves.button_cancel()
            moves.unlink()
        super(AccountInvoice, self).action_cancel()
        return True

    @api.model
    def _remove_move_reconcile(self, move_ids):
        aml_obj = self.env['account.move.line']
        amr_obj = self.env['account.move.reconcile']
        for aml_brw in aml_obj.browse(move_ids):
            rec_id = aml_brw.reconcile_id or aml_brw.reconcile_partial_id
            amr_obj += rec_id
        amr_obj.unlink()
        return True


class AccountInvoiceTaxWh(models.Model):
    """Invoice Tax Withholding"""
    _name = 'account.invoice.tax.wh'
    _inherit = 'account.invoice.tax'

    tax_id = fields.Many2one(
        'account.tax', 'Withheld Tax', help='Tax related to withholding')
    wh_amount = fields.Float(
        string='Withheld Amount', digits=dp.get_precision('Account'),
        help="Amount Withheld from the Tax")

    @api.multi
    def wh_subject_mapping(self, val):
        res = dict([
            ('1', {'rate': 100, 'basis': 'tax'}),
            ('2', {'rate': 50, 'basis': 'tax'}),
            ('3', {'rate': 100, 'basis': 'tax'}),
            ('4', {'rate': 50, 'basis': 'tax'}),
            ('5', {'rate': 2, 'basis': 'total'}),
            ('6', {'rate': 1, 'basis': 'total'}),
            ('7', {'rate': 50, 'basis': 'tax'}),
        ])
        return res.get(val, {})

    @api.model
    def wh_tax_account(self, invoice_id):
        account_id = invoice_id.company_id.wh_sale_itbms_account_id
        if not account_id:
            raise except_orm(
                _('Error!'),
                _('Please Define an Account to be used for withholding ITBMS '
                  'on Customer Invoice on Your Company.'))
        return account_id.id

    @api.multi
    def compute(self, invoice):
        at_obj = self.env['account.tax']
        tax_grouped = {}
        currency = invoice.currency_id.with_context(
            date=invoice.date_invoice or fields.Date.context_today(invoice))
        company_currency = invoice.company_id.currency_id
        account_id = self.wh_tax_account(invoice)
        wh_dict = self.wh_subject_mapping(invoice.l10n_pa_wh_subject)
        wh = wh_dict.get('rate')
        wh_basis = wh_dict.get('basis')
        if wh_basis == 'total':
            val = {
                'invoice_id': invoice.id,
                'name': _('Retencion por TDD/TDC'),
                'amount': currency.round(invoice.amount_total),
                'manual': False,
                'base': currency.round(invoice.amount_total),
                'base_amount': currency.round(invoice.amount_total),
                'tax_amount': currency.round(invoice.amount_total),
                'wh_amount': currency.round(invoice.amount_total) * wh / 100,
                'account_id': account_id,
            }
            return {(None,): val}

        for line in invoice.invoice_line:
            taxes = line.invoice_line_tax_id.compute_all(
                (line.price_unit * (1 - (line.discount or 0.0) / 100.0)),
                line.quantity, line.product_id, invoice.partner_id)['taxes']
            for tax in taxes:
                if not at_obj.browse(tax['id']).withholdable:
                    continue
                val = {
                    'invoice_id': invoice.id,
                    'name': tax['name'],
                    'amount': tax['amount'],
                    'manual': False,
                    'sequence': tax['sequence'],
                    'base': currency.round(
                        tax['price_unit'] * line['quantity']),
                    'tax_id': tax['id']
                }
                if invoice.type in ('out_invoice', 'in_invoice'):
                    val['base_code_id'] = tax['base_code_id']
                    val['tax_code_id'] = tax['tax_code_id']
                    val['base_amount'] = currency.compute(
                        val['base'] * tax['base_sign'],
                        company_currency, round=False)
                    val['tax_amount'] = currency.compute(
                        val['amount'] * tax['tax_sign'],
                        company_currency, round=False)
                    val['account_id'] = account_id
                    val['account_analytic_id'] = \
                        tax['account_analytic_collected_id']
                else:
                    val['base_code_id'] = tax['ref_base_code_id']
                    val['tax_code_id'] = tax['ref_tax_code_id']
                    val['base_amount'] = currency.compute(
                        val['base'] * tax['ref_base_sign'],
                        company_currency, round=False)
                    val['tax_amount'] = currency.compute(
                        val['amount'] * tax['ref_tax_sign'],
                        company_currency, round=False)
                    val['account_id'] = account_id
                    val['account_analytic_id'] = \
                        tax['account_analytic_paid_id']

                key = (val['tax_code_id'], val['base_code_id'],
                       val['account_id'], val['tax_id'])
                if key not in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['base'] += val['base']
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base_amount'] += val['base_amount']
                    tax_grouped[key]['tax_amount'] += val['tax_amount']

        for tax_val in tax_grouped.values():
            tax_val['base'] = currency.round(tax_val['base'])
            tax_val['amount'] = currency.round(tax_val['amount'])
            tax_val['base_amount'] = currency.round(tax_val['base_amount'])
            tax_val['tax_amount'] = currency.round(tax_val['tax_amount'])
            tax_val['wh_amount'] = tax_val['amount'] * wh / 100

        return tax_grouped

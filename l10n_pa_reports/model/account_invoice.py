# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
from __future__ import division
import time
from openerp import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def get_data(self):
        data_lines = []
        partner_ids = []
        invoice_ids = []
        for line in self:
            partner_brw = line.partner_id.commercial_partner_id
            vat = partner_brw.vat_alone
            entity = partner_brw.l10n_pa_entity
            dv = partner_brw.vat_dv
            args_part = [entity]
            concept = partner_brw.l10n_pa_concept
            prd_srv = partner_brw.l10n_pa_prd_srv
            if entity != 'E':
                args_part = [vat, dv, entity]
            else:
                dv = ''
                vat = ''
                if (concept != 6 or prd_srv != 2) and \
                        partner_brw.id not in partner_ids:
                    partner_ids.append(partner_brw.id)

            if not all(args_part) and partner_brw.id not in partner_ids:
                partner_ids.append(partner_brw.id)

            inv_number = line.supplier_invoice_number
            args_inv = [inv_number]
            if not all(args_inv) and line.id not in invoice_ids:
                invoice_ids.append(line.id)

            date = time.strftime(
                '%Y%m%d', time.strptime(line.date_invoice, '%Y-%m-%d'))

            data_lines.append({
                'entity': entity,
                'vat': vat,
                'dv': dv,
                'name': partner_brw.name,
                'supplier_invoice_number': inv_number,
                'date': date,
                'concept': concept,
                'type': prd_srv,
                'subtotal': line.amount_untaxed,
                'tax': line.amount_tax
            })
        return data_lines, partner_ids, invoice_ids


class AccountInvoiceTaxWh(models.Model):
    """Invoice Tax Withholding"""
    _inherit = 'account.invoice.tax.wh'

    @api.multi
    def get_data(self):
        data_lines = []
        for wh_line in self:
            line = wh_line.invoice_id
            partner_brw = line.partner_id.commercial_partner_id
            vat = partner_brw.vat_alone
            entity = partner_brw.l10n_pa_entity
            dv = partner_brw.vat_dv

            data_lines.append({
                'entity': entity,
                'vat': vat,
                'dv': dv,
                'name': partner_brw.name,
                'invoice_number': line.number,
                'wh_line': wh_line.base_amount,
                'tax_amount': wh_line.tax_amount,
                'subject': line.l10n_pa_wh_subject,
                'wh_amount': wh_line.wh_amount,
            })
        return data_lines

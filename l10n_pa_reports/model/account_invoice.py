# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
from __future__ import division

from openerp import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def get_dict_moves(self):
        data_lines = []
        for line in self:
            partner_brw = line.partner_id.commercial_partner_id
            data_lines.append({
                'entity': 'entity',
                'vat': partner_brw.vat_alone,
                'dv': partner_brw.vat_dv,
                'name': partner_brw.name,
                'supplier_invoice_number': line.supplier_invoice_number,
                'date': line.date_invoice,
                'concept': 'concept',
                'type': 'type',
                'subtotal': line.amount_untaxed,
                'tax': line.amount_tax
            })
        return data_lines

# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
from __future__ import division

from openerp import models, api, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    l10n_pa_concept = fields.Selection([
        (1, 'Compras o Adquisiciones de Bienes Muebles'),
        (2, 'Servicios Básicos'),
        (3, 'Honorarios y Comisiones por Servicios'),
        (4, 'Alquileres por Arrendamientos Comerciales'),
        (5, 'Cargos Bancarios, Intereses y Otros Gastos Financieros'),
        (6, 'Compras o Servicios del Exterior'),
        (7, 'Compras o Servicios Consolidados')],
        string='Supplier Invoice Concept',
        help='Indicates the Concept of the Supplier Invoice.')
    l10n_pa_prd_srv = fields.Selection([
        (1, 'Locales'),
        (2, 'Importaciones')],
        string='Purchase of Goods or Services',
        help='Indicates Source of Purchase of Goods or Services.')

    @api.multi
    def get_data(self):
        data_lines = []
        partner_ids = []
        for line in self:
            partner_brw = line.partner_id.commercial_partner_id
            vat = partner_brw.vat_alone
            entity = partner_brw.l10n_pa_entity
            dv = partner_brw.vat_dv
            args = [vat, dv, entity]
            if not all(args) and partner_brw.id not in partner_ids:
                partner_ids.append(partner_brw.id)
            data_lines.append({
                'entity': entity,
                'vat': vat,
                'dv': dv,
                'name': partner_brw.name,
                'supplier_invoice_number': line.supplier_invoice_number,
                'date': line.date_invoice,
                'concept': 'concept',
                'type': 'type',
                'subtotal': line.amount_untaxed,
                'tax': line.amount_tax
            })
        return data_lines, partner_ids

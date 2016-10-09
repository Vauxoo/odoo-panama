# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
from __future__ import division
import time
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
        invoice_ids = []
        for line in self:
            partner_brw = line.partner_id.commercial_partner_id
            vat = partner_brw.vat_alone
            entity = partner_brw.l10n_pa_entity
            dv = partner_brw.vat_dv
            args_part = [entity]
            if entity != 'E':
                args_part = [vat, dv, entity]
            else:
                dv = ''
                vat = ''
            if not all(args_part) and partner_brw.id not in partner_ids:
                partner_ids.append(partner_brw.id)

            inv_number = line.supplier_invoice_number
            concept = line.l10n_pa_concept
            prd_srv = line.l10n_pa_prd_srv
            args_inv = [inv_number, concept, prd_srv]
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

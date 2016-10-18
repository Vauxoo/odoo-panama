# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>

from openerp import models, fields


class ResPartner(models.Model):
    """Inherited to complete the attributes required to Panamanian Reports """
    _inherit = 'res.partner'

    l10n_pa_entity = fields.Selection([
        ('J', 'Juridico'),
        ('N', 'Natural'),
        ('E', 'Extranjero')],
        string='Entity Type',
        help='Indicates the nature of the Supplier Entity.')
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

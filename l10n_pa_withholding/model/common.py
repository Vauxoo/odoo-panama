# coding: utf-8

from openerp import models, fields


class CommonAbstract(models.AbstractModel):
    _name = 'l10n.pa.common.abstract'
    wh_agent_itbms = fields.Boolean(
        string='ITBMS Withholding Agent',
        help="Indicate if the Partner is a ITBMS Withholding Agent")
    # /!\ NOTE: This code will be regarded as duplicated
    l10n_pa_wh_subject = fields.Selection([
        ('na', 'No Aplica'),
        ('1', 'Pago por Servicio Profesional al Estado 100%'),
        ('2', 'Pago por Venta de Bienes/Servicios al Estado 50%'),
        ('3', 'Pago o Acreditacion a No Domiciliado o Empresa Constituida en'
         ' el Exterior 100%'),
        ('4', 'Pago o Acreditacion por Compra de Bienes/Servicios 50%'),
        ('5', 'Pago a Comercio Afiliado a Sistema de TC/TD 2%'),
        ('6', 'Pago a Comercio Afiliado a Sistema de TC/TD 1%'),
        ('7', 'Pago a Comercio Afiliado a Sistema de TC/TD 50%')],
        string='ITBMS Withholding Subject',
        help='If Apply. Indicates how much ITBMS to withholding on Payment')
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

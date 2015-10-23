# coding: utf-8
############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: hugo@vauxoo.com
#    planned by: Nhomar Hernandez <nhomar@vauxoo.com>
############################################################################
from openerp import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Barrio
    hood_id = fields.Many2one('res.country.state.district.township.hood',
                              'Neighborhood')
    # Corregimiento
    township_id = fields.Many2one('res.country.state.district.township',
                                  'Township')
    # Distrito
    district_id = fields.Many2one('res.country.state.district',
                                  'District')

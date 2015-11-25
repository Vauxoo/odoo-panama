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

    def _address_fields(self, cr, uid, context=None):
        """ Returns the list of address fields that are synced from the parent
        when the `use_parent_address` flag is set. """
        res = super(ResPartner, self)._address_fields(cr, uid, context=context)
        res = res + ['district_id', 'township_id', 'hood_id']
        return res

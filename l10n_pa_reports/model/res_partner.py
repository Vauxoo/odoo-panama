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

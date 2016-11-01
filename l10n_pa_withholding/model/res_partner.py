# coding: utf-8

from openerp import models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'l10n.pa.common.abstract']

# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>

from openerp import fields, models


class AccountTax(models.Model):
    _description = 'Tax'
    _inherit = 'account.tax'
    withholdable = fields.Boolean(
        string='Withholdable',
        help="Indicates if the tax must be withheld")

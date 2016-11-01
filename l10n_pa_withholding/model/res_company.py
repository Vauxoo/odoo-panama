# coding: utf-8

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"
    _description = 'Companies'

    wh_sale_itbms_account_id = fields.Many2one(
        'account.account', 'Wh Sale ITBMS Account',
        domain=('[("type", "!=", "view")]'), required=False,
        help='Account to be used for withholding ITBMS on Customer Invoice')
    wh_sale_itbms_journal_id = fields.Many2one(
        'account.journal', 'Wh Sale ITBMS Journal',
        domain=('[("type", "!=", "view")]'), required=False,
        help='Account to be used for withholding ITBMS on Customer Invoice')

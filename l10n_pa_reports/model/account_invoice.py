# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
from __future__ import division

from openerp import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def get_dict_moves(self):
        moves_amount_0 = []
        dict_lines = {}
        for line in self:
            continue
            matrix_row = []
            partner = line.partner_id.commercial_partner_id
            amount_0 = amount_16 = amount_exe = amount_11 = amount_ret = 0
            amount_imp16 = 0
            tax = line._get_tax()
            amount_base_tax = tax.amount and ((
                line.debit or line.credit) / (tax.amount / 100)) or 0
            if not tax.amount:
                amount_base_tax = line.amount_base
            if line.credit:
                amount_base_tax = amount_base_tax * -1
            category = tax.category_id.name or False
            amount_base = round(tax.amount or 0, 2)
            if category in ('IVA', 'IVA-PART') and amount_base == 16.0:
                amount_16 = amount_base_tax or 0
            elif category == 'IVA' and amount_base == 11.0:
                amount_11 = amount_base_tax or 0
            elif category == 'IVA' and amount_base == 0:
                amount_0 = amount_base_tax or 0
            elif category == 'IVA-EXENTO' and amount_base == 0:
                amount_exe = amount_base_tax or 0
            elif category == 'IVA-RET':
                amount_ret = line.credit or line.debit * -1 or 0
            elif category == 'IVA-IMP':
                amount_imp16 = amount_base_tax or 0
            if not sum([
                    amount_0, amount_16, amount_exe, amount_11, amount_ret,
                    amount_imp16]):
                moves_amount_0.append(line.id)
                continue
            key = partner.vat_split or partner.name.replace(' ', '')
            if key in dict_lines:
                line_move = dict_lines[key]
                line_move[7] = line_move[7] + amount_16
                line_move[8] = line_move[8] + amount_11
                line_move[9] = line_move[9] + amount_0
                line_move[10] = line_move[10] + amount_exe
                line_move[11] = line_move[11] + amount_ret
                line_move[12] = line_move[12] + amount_imp16
                dict_lines.update({key: line_move})
            else:
                matrix_row.append(partner.type_of_third)
                matrix_row.append(partner.type_of_operation)
                matrix_row.append(partner.vat_split)
                if all([partner.type_of_third == "05",
                        partner.number_fiscal_id]):
                    matrix_row.append(partner.number_fiscal_id)
                else:
                    matrix_row.append("")
                if partner.type_of_third != "04":
                    matrix_row.append(partner.name)
                    matrix_row.append(partner.country_id.code or '')
                    matrix_row.append(partner.nationality or "")
                else:
                    matrix_row.append("")
                    matrix_row.append("")
                    matrix_row.append("")
                matrix_row.append(amount_16)
                matrix_row.append(amount_11)
                matrix_row.append(amount_0)
                matrix_row.append(amount_exe)
                matrix_row.append(amount_ret)
                matrix_row.append(amount_imp16)
                dict_lines.update({key: matrix_row})
        return dict_lines, moves_amount_0



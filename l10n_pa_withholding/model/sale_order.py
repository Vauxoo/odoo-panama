# coding: utf-8

from openerp import models, api


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'l10n.pa.common.abstract']

    @api.multi
    def onchange_partner_id(self, part):
        res = super(SaleOrder, self).onchange_partner_id(part)
        if not part:
            res['value']['wh_agent_itbms'] = False
            res['value']['l10n_pa_wh_subject'] = False
            return res
        part = self.env['res.partner'].browse(part)
        part = part._find_accounting_partner(part)
        res['value']['wh_agent_itbms'] = part.wh_agent_itbms
        res['value']['l10n_pa_wh_subject'] = part.l10n_pa_wh_subject
        return res

    @api.model
    def _prepare_invoice(self, order, lines):
        invoice_vals = super(SaleOrder, self)._prepare_invoice(order, lines)
        return dict(invoice_vals,
                    wh_agent_itbms=order.wh_agent_itbms,
                    l10n_pa_wh_subject=order.l10n_pa_wh_subject)

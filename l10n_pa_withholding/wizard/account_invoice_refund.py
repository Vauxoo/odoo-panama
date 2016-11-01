# coding: utf-8

from openerp import api, models


class AccountInvoiceRefund(models.TransientModel):
    """Refunds invoice"""

    _inherit = "account.invoice.refund"

    @api.multi
    def compute_refund(self, mode):

        result = super(AccountInvoiceRefund, self).compute_refund(mode)
        refund_id = result.get('domain')[1][2]

        inv_obj = self.env['account.invoice']

        for inv_brw in inv_obj.browse(self._context.get('active_ids')):
            inv_obj.browse(refund_id).write(dict(
                wh_agent_itbms=inv_brw.wh_agent_itbms,
                l10n_pa_wh_subject=inv_brw.l10n_pa_wh_subject))
        return result

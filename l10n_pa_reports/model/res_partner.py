# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import models, fields, api


class ResPartner(models.Model):
    """Inherited to complete the attributes required to DIOT, Addenda and
    fiscal documents.

    **Toponyms**

    Added field city_id to allow have the catalog of cities as in the states,
    allowing only select the register when is set the address in partners,
    avoiding having inconsistency with city names.
    The city data is taken from `Correos de México <goo.gl/rwXvDg>`_

    Also are added 3 new fields in partner address to complete the Mexico
    toponyms and allow have all fields required in XML fiscal.
    The external and internal number are added to have normalized the address,
    and not all in street field, locality is added to set this value in the
    address.

    **Addenda**

    Added relation between partner and Addenda, this to indicate which addenda
    belongs to partner. The addenda will be taken from the customer in
    the invoices, and will be calculated on each one.

    **DIOT**

    Added required fields according with the provisions in the next SAT
    document `Document <goo.gl/THPLDk>`_. To allow generate the form A-29
    requested by this SAT.

    **Fiscal Regime**
    The fiscal regimen catalog is provided by the SAT `here <goo.gl/mwcbtx>`
    """
    _inherit = 'res.partner'

    @api.depends('vat', 'name', 'country_id')
    def _compute_base_vat_split(self):
        for partner in self:
            if partner.country_id != self.env.ref('base.mx'):
                # TODO: Fundament this generic RFC for int. Customers.
                partner.vat_split = 'XEXX010101000'
                continue
            partner.vat_split = partner.vat and partner.vat[2:] or False

    city_id = fields.Many2one(
        'res.country.state.city', 'City',
        help='AKA: Municipio. Provide the list of cities in Mexico taken '
        'from "Correos de Mexico". If you not found a city please report '
        'to update the data.')
    addenda_id = fields.Many2one(
        'account.addenda', 'Addendum', company_dependent=True,
        help='Addendum required by this partner in XML documents, used on '
        'invoice to assign data from this addendum in XML invoice.')
    vat_split = fields.Char(
        'VAT Split', compute='_compute_base_vat_split', store=True,
        help='Save the VAT without country prefix. Eg. If VAT is '
        'MXVXO100202FG5 only save VXO100202FG5.')
    type_of_third = fields.Selection([
        ('04', ' 04 - National Supplier'),
        ('05', ' 05 - Foreign Supplier'),
        ('15', ' 15 - Global Supplier')],
        help='Indicate the type of third that is the supplier. Is the first '
        'column in DIOT report.')
    type_of_operation = fields.Selection([
        ('03', ' 03 - Provision of Professional Services'),
        ('06', ' 06 - Renting of buildings'),
        ('85', ' 85 - Others')],
        help='Indicate the operations type that makes this supplier. Is the '
        'second column in DIOT report')
    number_fiscal_id = fields.Char(
        'Fiscal Identification Number (NIF)', size=40,
        help='NIF defined by this supplier. Is the fourth column in DIOT '
        'report.')
    nationality = fields.Char(
        size=40, help='Nationality based in the supplier country. Is the '
        'seventh column in DIOT report')
    payment_method_id = fields.Many2one(
        'oml.payment.method', 'Payment Method',
        help='Define a default value to payment method on invoices created to '
        'this customer. When you create a new invoice to this customer, the '
        'default value will be the assigned here.\n'
        'The payment method in the invoice is to indicate which method is '
        'used to pay the invoice, and are provided by the SAT.')
    regimen_fiscal_id = fields.Many2one(
        'regimen.fiscal', 'Fiscal Regime',
        help='According to article 29-A in CFF, the fiscal documents must '
        'contain the fiscal regime related to the customer according in the '
        'Law on Incoming Tax. Set here the fiscal regime to this customer.')
    l10n_mx_street3 = fields.Char(
        'External number', size=128,
        help='External number of the partner address')
    l10n_mx_street4 = fields.Char(
        'Internal number', size=128,
        help='Internal number of the partner address')
    l10n_mx_city2 = fields.Char(
        'Locality', size=128, help='Locality configured for this partner.')

    @api.onchange('city_id')
    def onchange_city(self):
        self.state_id = self.city_id.state_id.id or self.state_id.id
        self.country_id = self.city_id.country_id.id or self.country_id.id

    @api.multi
    def onchange_state(self, state_id, city_id=False):
        res = super(ResPartner, self).onchange_state(state_id)
        city_id = city_id or self.city_id.id
        if all([city_id, state_id, self.env[
                'res.country.state.city'].browse(
                    city_id).state_id.id != state_id]):
            res.get('value', {}).update({
                'city': False,
                'city_id': None})
        return res

    @api.multi
    def _get_emmiter_address(self):
        domicile = '%s %s, %s' % (
            self.city_id.name, self.state_id.name, self.country_id.name)
        return {
            'emitter_domicile': domicile,
            'emitter_rfc': self.vat_split,
            'emitter_street': self.street,
            'emitter_exterior_no': self.l10n_mx_street3,
            'emitter_interior_no': self.l10n_mx_street4,
            'emitter_colony': self.street2,
            'emitter_municipality': self.city_id.name,
            'emitter_zip': self.zip,
            'emitter_state': self.state_id.name,
            'emitter_locality': self.l10n_mx_city2,
            'emitter_country': self.country_id.name,
        }

    @api.multi
    def _get_emitter_issued_address(self):
        return {
            'emitter_issue_on_street': self.street,
            'emitter_issue_on_zip': self.zip,
            'emitter_issue_on_colony': self.street2,
            'emitter_issue_on_municipality': self.city_id.name,
            'emitter_issue_on_state': self.state_id.name,
            'emitter_issue_on_locality': self.l10n_mx_city2,
            'emitter_issue_on_exterior_no': self.l10n_mx_street3,
            'emitter_issue_on_interior_no': self.l10n_mx_street4,
            'emitter_issue_on_country': self.country_id.name,
        }

    @api.multi
    def _get_receiver_address(self):
        return {
            'receiver_name': self.name,
            'receiver_rfc': self.vat_split,
            'receiver_street': self.street,
            'receiver_colony': self.street2,
            'receiver_municipality': self.city_id.name,
            'receiver_state': self.state_id.name,
            'receiver_locality': self.l10n_mx_city2,
            'receiver_exterior_no': self.l10n_mx_street3,
            'receiver_interior_no': self.l10n_mx_street4,
            'receiver_zip': self.zip,
            'receiver_country': self.country_id.name,
        }

    @api.model
    def _verify_mexican_data(self):
        """Return partners that have all information to allow generate the
        XML to sign with the PAC."""
        partners = self.mapped('commercial_partner_id')
        return partners.filtered(lambda r: all([
            r.vat_split
        ]))

    @api.multi
    def _get_not_partners_form43(self):
        return self.mapped('commercial_partner_id')

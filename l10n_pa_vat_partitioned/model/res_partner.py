# -*- encoding: utf-8 -*-
#
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2014 Vauxoo - http://www.vauxoo.com/
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#
#    Coded by: vauxoo consultores (info@vauxoo.com)
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from openerp import models, fields, api
from openerp.tools.translate import _


class ResPartner(models.Model):

    """ This class is inherited to add three new fields to can edit
        VAT field value """

    # Will be part of res.partner model
    _inherit = "res.partner"

    # COMPUTES AND INVERSE
    @api.one
    @api.depends('vat')
    def _get_l10n_pa_ruc_country_id(self):
        """ Get the country object from the VAT field """
        if self.vat:
            country_code = None
            for country_id in self.env['res.country'].search(
                    [('code', '=', self.vat[:2])]):
                country_code = country_id
            self.l10n_pa_ruc_country_id = country_code
        else:
            self.l10n_pa_ruc_country_id = self.env['res.country'].\
                search([('code', '=', 'PA')])

    @api.one
    @api.depends('vat')
    def _get_l10n_pa_ruc(self):
        """ Get the RUC value from the VAT field """
        self.l10n_pa_ruc = ""
        if self.vat:
            self.l10n_pa_ruc = self.vat[2:len(self.vat)-4]

    @api.one
    @api.depends('vat')
    def _get_l10n_pa_ruc_dv(self):
        """ Get the DV value from the VAT field """
        self.l10n_pa_ruc_dv = ""
        if self.vat and 'DV' in self.vat:
            self.l10n_pa_ruc_dv = self.vat[-2:]

    @api.one
    @api.depends('l10n_pa_ruc_country_id', 'l10n_pa_ruc', 'l10n_pa_ruc_dv')
    def _get_new_vat(self):
        """ Get the value for VAT field through the 3 component fields """
        new_vat = ""
        if self.l10n_pa_ruc_country_id:
            new_vat += self.l10n_pa_ruc_country_id.code
        if self.l10n_pa_ruc:
            new_vat += self.l10n_pa_ruc
        if self.l10n_pa_ruc_dv:
            new_vat += "DV%s" % self.l10n_pa_ruc_dv
        self.vat = new_vat

    # COLUMNS (New fields)
    l10n_pa_ruc_country_id = fields.Many2one(
        'res.country', ondelete="set null",
        compute='_get_l10n_pa_ruc_country_id',
        inverse='_get_new_vat',
        help=_("Country to form the TIN field"))
    l10n_pa_ruc = fields.Char(
        string="RUC", size=25,
        compute='_get_l10n_pa_ruc',
        inverse='_get_new_vat',
        help=_("RUC value to form the TIN field"))
    l10n_pa_ruc_dv = fields.Char(
        string="DV", size=2,
        compute='_get_l10n_pa_ruc_dv',
        inverse='_get_new_vat',
        help=_("DV value to form the TIN field"))

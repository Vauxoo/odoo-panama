# coding: utf-8
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2013 Vauxoo - http://www.vauxoo.com/
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
############################################################################
#    Coded by: moylop260 (moylop260@vauxoo.com)
#              Isaac Lopez (isaac@vauxoo.com)
############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import fields, models


class ResDistrict(models.Model):
    _description = "Country Province District"
    _name = 'res.country.state.district'
    _order = 'name'
    # Distrito
    name = fields.Char('Name District', size=64, required=True, select=True,
                       help='Administrative divisions of a Province.')
    # Provincia
    state_id = fields.Many2one('res.country.state', 'Province', required=True)
    # Pais
    country_id = fields.Many2one(related='state_id.country_id',
                                 string='Country', readonly=True)
    code = fields.Char('District Code', size=5,
                       help='The District code in max. five chars.')


class ResTownship(models.Model):
    _description = "Country Province District Township"
    _name = 'res.country.state.district.township'
    _order = 'name'
    # Corregimiento
    name = fields.Char('Name Township', size=64, required=True, select=True,
                       help='Administrative divisions of a district.')
    # Distrito
    district_id = fields.Many2one('res.country.state.district', 'District',
                                  required=True)
    # Provincia
    state_id = fields.Many2one(related='district_id.state_id',
                               string='Country', readonly=True)
    # Pais
    country_id = fields.Many2one(related='district_id.state_id.country_id',
                                 string='Country', readonly=True)
    code = fields.Char('Township Code', size=5,
                       help='The District code in max. five chars.')


class ResNeighborhood(models.Model):
    _description = "Country province District Township Neighborhood"
    _name = 'res.country.state.district.township.hood'
    _order = 'name'
    # Barrio
    name = fields.Char('Name Neighborhood', size=64,
                       required=True, select=True,
                       help='Administrative divisions of a Township.')
    # Corregimiento
    township_id = fields.Many2one('res.country.state.district.township',
                                  'Township',
                                  required=True)
    # Distrito
    district_id = fields.Many2one(related='township_id.district_id',
                                  string='Country', readonly=True)
    # Provincia
    state_id = fields.Many2one(related='township_id.district_id.state_id',
                               string='Country', readonly=True)
    # Pais
    country_id = fields.Many2one(
        related='township_id.district_id.state_id.country_id',
        string='Country', readonly=True)
    code = fields.Char('Township Code', size=5,
                       help='The District code in max. five chars.')

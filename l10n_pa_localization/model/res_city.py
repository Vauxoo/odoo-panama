# coding: utf-8
############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: hugo@vauxoo.com
#    planned by: Nhomar Hernandez <nhomar@vauxoo.com>
############################################################################

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
                                 string='Country', readonly=True, store=True)
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
                               string='Province', readonly=True, store=True)
    # Pais
    country_id = fields.Many2one(related='district_id.state_id.country_id',
                                 string='Country', readonly=True, store=True)
    code = fields.Char('Township Code', size=5,
                       help='The Township code in max. five chars.')


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
                                  string='District', readonly=True,
                                  store=True)
    # Provincia
    state_id = fields.Many2one(related='township_id.district_id.state_id',
                               string='Province', readonly=True, store=True)
    # Pais
    country_id = fields.Many2one(
        related='township_id.district_id.state_id.country_id',
        string='Country', readonly=True, store=True)
    code = fields.Char('Neighborhood Code', size=5,
                       help='The Neighborhood code in max. five chars.')

    def _auto_init(self, cr, context=None):
        res = super(ResNeighborhood, self)._auto_init(
            cr, context=context)
        # index Hood name, country_id
        cr.execute(
            "SELECT indexname FROM pg_indexes "
            "WHERE indexname = 'res_hood_name_country_id'")
        if not cr.fetchone():
            cr.execute(
                "CREATE INDEX res_hood_name_country_id ON "
                "res_country_state_district_township_hood (name, country_id)")

        # index Hood name, country_id, state_id
        cr.execute(
            "SELECT indexname FROM pg_indexes "
            "WHERE indexname = 'res_hood_name_country_id_state_id'")
        if not cr.fetchone():
            cr.execute(
                "CREATE INDEX res_hood_name_country_id_state_id ON "
                "res_country_state_district_township_hood "
                "(name, country_id, state_id)")

        # index Hood name, country_id, state_id, district_id
        cr.execute(
            "SELECT indexname FROM pg_indexes "
            "WHERE indexname = "
            "'res_hood_name_country_id_state_id_district_id'")
        if not cr.fetchone():
            cr.execute(
                "CREATE INDEX "
                "res_hood_name_country_id_state_id_district_id ON "
                "res_country_state_district_township_hood "
                "(name, country_id, state_id)")

        # index Hood name, country_id, state_id, district_id, township_id
        cr.execute(
            "SELECT indexname FROM pg_indexes "
            "WHERE indexname = "
            "'res_hood_name_country_id_state_id_district_id_township_id'")
        if not cr.fetchone():
            cr.execute(
                "CREATE INDEX "
                "res_hood_name_country_id_state_id_district_id_township_id "
                "ON res_country_state_district_township_hood "
                "(name, country_id, state_id)")

        return res

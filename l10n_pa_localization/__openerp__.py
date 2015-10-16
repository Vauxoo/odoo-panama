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
{
    "name": "OpenERP Panama Location",
    "version": "1.0",
    "author": "Vauxoo",
    "category": "Localization/Panama",
    "website": "http://www.vauxoo.com/",
    "license": "AGPL-3",
    "depends": [
        "base"
    ],
    "demo": [],
    "data": [
        "data/res_country_states.xml",
        "data/res_country_states_district.xml",
        "data/res_country_states_district_township.xml",
        "data/res_country_states_district_township_hood.xml",
        "view/res_city_view.xml",
        "security/localization_security.xml",
        "security/ir.model.access.csv"
    ],
    "installable": True,
}

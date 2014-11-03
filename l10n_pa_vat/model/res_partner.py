#!/usr/bin/python
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
#
#

import re

import ruc as ruc_vat
from openerp.osv import osv


class res_partner(osv.Model):

    _inherit = 'res.partner'

    __check_vat_pa_re1 = re.compile(r'(PE|E)-\d{1,3}-\d{1,5}$')
    __check_vat_pa_re2 = re.\
        compile(r'((\d|1[0-2]|N)|(\d|1[0-2])-(PI|AV|NT|N))-\d{1,3}-\d{1,5}$')
    __check_vat_pa_re3 = re.compile(r'\d{1,7}-\d{1,4}-\d{1,6}$')
    __check_vat_pa_re4 = re.compile(r'PAS\d{1,27}$')
    __check_vat_pa_re5 = re.compile(r'(\d|1[0-2])-NT-\d{1,3}-\d{1,5}$')

    def check_vat_pa(self, vat):
        vat_split_dv = vat.split('DV')
        vat = vat_split_dv[0]
        ruc_vat.calculateDV(vat)
        if self.__check_vat_pa_re1.match(vat) or self.__check_vat_pa_re2.\
                match(vat) or self.__check_vat_pa_re3.match(vat) or self.\
                __check_vat_pa_re4.match(vat) or self.__check_vat_pa_re5.\
                match(vat):
            if len(vat_split_dv) == 2:
                return ruc_vat.calculateDV(vat) == vat_split_dv[-1]
            return True
        return False

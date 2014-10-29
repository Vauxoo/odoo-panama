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

from openerp.osv import osv
import re


class res_partner(osv.Model):

    _inherit = 'res.partner'

    __check_vat_pa_re1 = re.compile(r'0{2}(N0|PE|E0)-\d{4}-\d{5}$')
    __check_vat_pa_re2 = re.\
        compile(r'(0\d|1[0-2])(PI|AV|00)-\d{4}-\d{5}$')
    __check_vat_pa_re3 = re.compile(r'\d{16}$')
    __check_vat_pa_re4 = re.compile(r'PAS\d{1,27}$')
    __check_vat_pa_re5 = re.compile(r'(0\d|1[0-2])-NT-\d{4}-\d{5}$')

    def check_vat_pa(self, vat):
        if self.__check_vat_pa_re1.match(vat) or self.__check_vat_pa_re2.\
                match(vat) or self.__check_vat_pa_re3.match(vat) or self.\
                __check_vat_pa_re4.match(vat) or self.__check_vat_pa_re5.\
                match(vat):
            return True
        return False

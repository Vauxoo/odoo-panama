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

_arrval = {
    '00': '00',
    '10': '01',
    '11': '02',
    '12': '03',
    '13': '04',
    '14': '05',
    '15': '06',
    '16': '07',
    '17': '08',
    '18': '09',
    '19': '01',
    '20': '02',
    '21': '03',
    '22': '04',
    '23': '07',
    '24': '08',
    '25': '09',
    '26': '02',
    '27': '03',
    '28': '04',
    '29': '05',
    '30': '06',
    '31': '07',
    '32': '08',
    '33': '09',
    '34': '01',
    '35': '02',
    '36': '03',
    '37': '04',
    '38': '05',
    '39': '06',
    '40': '07',
    '41': '08',
    '42': '09',
    '43': '01',
    '44': '02',
    '45': '03',
    '46': '04',
    '47': '05',
    '48': '06',
    '49': '07'
    }


def calc_dv(ruc, sw):
    j = 2
    nsuma = 0
    divisor = 11
    for elem in reversed(ruc):
        if sw and j == 12:
            sw = False
            j -= 1
        nsuma += j*elem
        print elem, 'j----', j, 'suma-----', nsuma
        j += 1
    if nsuma > 0:
        result = nsuma % divisor
        if result == 0 or result == 1 and divisor == 11:
            print "DV es 0"
            return 0
        else:
            print "DV es :", divisor-int(result)
            return divisor-int(result)
    print sw, 'SWWWWWWWWWWW'
    return False


class res_partner(osv.Model):

    _inherit = 'res.partner'

    __check_vat_pa_re1 = re.compile(r'N0{2}(N0|PE|E0)-\d{3}-\d{5}$')
    __check_vat_pa_re2 = re.\
        compile(r'(N0\d|1[0-2])(PI|AV|00)-\d{4}-\d{5}$')  # 00 será el ultimo
    __check_vat_pa_re3 = re.compile(r'\d{16}$')
    __check_vat_pa_re4 = re.compile(r'PAS\d{1,27}$')
    __check_vat_pa_re5 = re.compile(r'(0\d|1[0-2])-NT-\d{4}-\d{5}$')

    def get_ructb(self, ruc_str):
        ructb = []
        vat_str = ruc_str.rjust(20, '0')
        if 'NT' in ruc_str:
            vat_str = vat_str.replace('NT', '43')
            print ructb, 'RUCTBBBBBBBBBBBBBBBBBBBB'
        if 'E' in ruc_str:
            print type(vat_str)
            vat_str = vat_str.replace('E', '5').replace('N', '5')
            print vat_str, 'vat_strvat_strvat_strvat_strvat_str'
        ructb = list(vat_str)
        ructb = map(int, ructb)
        return ructb

    def check_vat_pa(self, vat):
        vat_split_dv = vat.split('DV')
        vat = vat_split_dv[0]
        dv_cal = []
        if self.__check_vat_pa_re1.match(vat) or self.__check_vat_pa_re2.\
                match(vat) or self.__check_vat_pa_re3.match(vat) or self.\
                __check_vat_pa_re4.match(vat) or self.__check_vat_pa_re5.\
                match(vat):
            print vat
            ructb = []
            if len(vat_split_dv) == 2:
                dv = vat_split_dv[-1]
                vat_str = vat.replace('-', '')
                print vat_str
                ructb = self.get_ructb(vat_str)
                print ructb, 'RUCTBBBBBBBBBBBBBBBBBBBB'
                # import pdb;pdb.set_trace()
                dv_cal.append(calc_dv(ructb, False))
                ructb.append(dv_cal[0])
                dv_cal.append(calc_dv(ructb, False))
                return ''.join(map(str, dv_cal)) == dv
            return True
        return False

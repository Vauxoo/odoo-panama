# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2014 Vauxoo - http://www.vauxoo.com/
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#
#    Coded by: Luis Torres (luis_t@vauxoo.com)
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
'''
This file adds field to set perception type in employee
'''
from openerp import models, fields, api
from openerp.tools.translate import _


class hr_employee(models.Model):
    '''
    Inherit hr.employee to added field perception type of the employee
    '''
    _inherit = 'hr.employee'

    @api.model
    def _get_perception_types(self):
        types = [
            ('5_individual', _('5 Individual Declaration')),
            ('6_joint', _('6 Joint Declaration')),
            ]
        return types

    perception_type = fields.Selection(
        _get_perception_types, 'Perception Type',
        help='Perception type of the employee. Use: \n'
        '- 5 to individual declaration.\n- 6 to joint declaration, when the '
        'spouse not work.')

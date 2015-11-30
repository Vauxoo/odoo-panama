# coding: utf-8
############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2015 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: Luis Torres <luis_t@vauxoo.com>
############################################################################

from lxml import etree as ET
from openerp.tests.common import TransactionCase


class TestPartnerView(TransactionCase):

    def setUp(self):
        super(TestPartnerView, self).setUp()
        self.partner_id = self.env.ref('base.res_partner_2')
        self.company_id = self.env.ref('base.main_company')
        self.partner_pa_id = self.env.ref('base.pa')
        self.partner_mx_id = self.env.ref('base.mx')

    def test_10_fields_address_partner_panama(self):
        self.company_id.write({'country_id': self.partner_pa_id.id})
        view = self.partner_id.fields_view_get(view_id=False, view_type='form')
        self.assertEqual(view['type'], 'form')
        nodes = ET.XML(view['arch']).xpath("//field[@name='district_id']")
        self.assertTrue(len(nodes) > 0,
                        "'district_id' field is not found in view")
        nodes = ET.XML(view['arch']).xpath("//field[@name='township_id']")
        self.assertTrue(len(nodes) > 0,
                        "'township_id' field is not found in view")
        nodes = ET.XML(view['arch']).xpath("//field[@name='hood_id']")
        self.assertTrue(len(nodes) > 0,
                        "'hood_id' field is not found in view")

    def test_20_fields_address_contact_mexico(self):
        self.company_id.write({'country_id': self.partner_mx_id.id})
        view = self.partner_id.fields_view_get(view_id=False, view_type='form')
        self.assertEqual(view['type'], 'form')
        nodes = ET.XML(view['arch']).xpath("//field[@name='district_id']")
        self.assertTrue(len(nodes) == 0,
                        "'district_id' field is found in view")
        nodes = ET.XML(view['arch']).xpath("//field[@name='township_id']")
        self.assertTrue(len(nodes) == 0,
                        "'township_id' field is found in view")
        nodes = ET.XML(view['arch']).xpath("//field[@name='hood_id']")
        self.assertTrue(len(nodes) == 0,
                        "'hood_id' field is found in view")

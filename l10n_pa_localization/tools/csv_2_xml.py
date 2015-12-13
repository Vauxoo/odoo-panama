# -*- encoding: utf-8 -*-
############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: hugo@vauxoo.com
#    planned by: Nhomar Hernandez <nhomar@vauxoo.com>
############################################################################

import xml.dom.minidom
import csv
from add_node import add_node, remove_accents
data_path1 = '../data/res_country_states.xml'
data_path2 = '../data/res_country_states_district.xml'
data_path3 = '../data/res_country_states_district_township.xml'
data_path4 = '../data/res_country_states_district_township_hood.xml'
csv_file_path = '../source/proseced_csv.csv'

csvData = csv.reader(open(csv_file_path), delimiter=',')
cities = []

# XML_DOC para Provincias
xml_doc_provincias = xml.dom.minidom.Document()
openerp_node = xml_doc_provincias.createElement('openerp')
xml_doc_provincias.appendChild(openerp_node)
nodeopenerp_provincias = xml_doc_provincias.getElementsByTagName('openerp')[0]
main_node_provincias = add_node('data', {"noupdate": "True"},
                                nodeopenerp_provincias,
                                xml_doc_provincias,
                                attrs_types={"noupdate": "attribute"})
# XML_DOC para Distritos
xml_doc_distritos = xml.dom.minidom.Document()
openerp_node = xml_doc_distritos.createElement('openerp')
xml_doc_distritos.appendChild(openerp_node)
nodeopenerp_distritos = xml_doc_distritos.getElementsByTagName('openerp')[0]
main_node_distritos = add_node('data', {"noupdate": "True"},
                               nodeopenerp_distritos,
                               xml_doc_distritos,
                               attrs_types={"noupdate": "attribute"})
# XML_DOC para Corregimientos
xml_doc_corregimientos = xml.dom.minidom.Document()
openerp_node = xml_doc_corregimientos.createElement('openerp')
xml_doc_corregimientos.appendChild(openerp_node)
nodeopenerp_corregimiento = xml_doc_corregimientos.getElementsByTagName(
    'openerp')[0]
main_node_corregimiento = add_node('data', {"noupdate": "True"},
                                   nodeopenerp_corregimiento,
                                   xml_doc_corregimientos,
                                   attrs_types={"noupdate": "attribute"})

# XML_DOC para Barrios
xml_doc_barrios = xml.dom.minidom.Document()
openerp_node = xml_doc_barrios.createElement('openerp')
xml_doc_barrios.appendChild(openerp_node)
nodeopenerp_barrios = xml_doc_barrios.getElementsByTagName('openerp')[0]
main_node_barrio = add_node('data', {"noupdate": "True"},
                            nodeopenerp_barrios,
                            xml_doc_barrios,
                            attrs_types={"noupdate": "attribute"})
provincias = []
distritos = []
corregimientos = []
barrios = []
xml_id_hood = []
xml_id_township = []
xml_id_district = []
xml_id_state = []

def add_province(row):
    """ xml_id: res_country_state_pa_ + provincia_code"""
    if row[0].decode('utf-8') not in provincias:
        provincia = row[0].decode('utf-8')
        code = provincia[0:3].lower()
        xml_id = 'res_country_state_pa_' + code

        if xml_id in xml_id_state:
            xml_id = xml_id + str(len(xml_id_state)).decode('utf-8')
            xml_id_state.append(xml_id)
        else:
            xml_id_state.append(xml_id)

        provincias.append(provincia)
        node_record = add_node(
            'record',
            attrs={"id": xml_id, "model": "res.country.state", },
            parent_node=main_node_provincias,
            minidom_xml_obj=xml_doc_provincias,
            attrs_types={"id": "attribute", "model": "attribute"})
        main_node_provincias.appendChild(node_record)
        # Country
        order = ['name', 'ref', ]
        node_field_country = add_node(
            'field',
            {"name": "country_id", "ref": "base.pa", },
            node_record, xml_doc_provincias,
            {"name": 'attribute', "ref": 'attribute', },
            order)
        node_record.appendChild(node_field_country)
        # Nombre Provincia
        order = ['name']
        node_field_name = add_node(
            'field',
            {"name": provincia, },
            node_record, xml_doc_provincias,
            {"name": 'att_text', },
            order)
        node_record.appendChild(node_field_name)

        order = ['code']
        node_field_name = add_node(
            'field',
            {"code": code, },
            node_record, xml_doc_provincias,
            {"code": 'att_text', },
            order)
        node_record.appendChild(node_field_name)


def add_distric(row):
    """ xml_id: res_country_state_district_pa_ + provincia_code"""
    if row[1].decode('utf-8') not in distritos:
        distrito = row[1].decode('utf-8')
        # code = distrito[0:5].lower()
        id_district = remove_accents(distrito)
        id_district = id_district.replace(' ', '_').lower()
        xml_id = 'res_country_state_district_pa_' + id_district

        if xml_id in xml_id_district:
            xml_id = xml_id + str(len(xml_id_district)).decode('utf-8')
            xml_id_district.append(xml_id)
        else:
            xml_id_district.append(xml_id)

        distritos.append(distrito)
        node_record = add_node(
            'record',
            attrs={"id": xml_id, "model": "res.country.state.district"},
            parent_node=main_node_distritos,
            minidom_xml_obj=xml_doc_distritos,
            attrs_types={"id": "attribute", "model": "attribute"})
        main_node_distritos.appendChild(node_record)
        # Country
        order = ['name', 'ref', ]
        node_field_country = add_node(
            'field',
            {"name": "country_id", "ref": "base.pa", },
            node_record, xml_doc_distritos,
            {"name": 'attribute', "ref": 'attribute', },
            order)
        node_record.appendChild(node_field_country)
        # Provincia
        state = row[0].decode('utf-8')
        code = state[0:3].lower()
        state_id = 'l10n_pa_localization.res_country_state_pa_' + code
        order = ['name', 'ref', ]
        node_field_state = add_node(
            'field',
            {"name": "state_id", "ref": state_id, },
            node_record, xml_doc_distritos,
            {"name": 'attribute', "ref": 'attribute', },
            order)
        node_record.appendChild(node_field_state)
        # Nombre Distrito
        order = ['name']
        node_field_name = add_node(
            'field',
            {"name": distrito, },
            node_record, xml_doc_distritos,
            {"name": 'att_text', },
            order)
        node_record.appendChild(node_field_name)

        # order = ['code']
        # node_field_name = add_node(
        #     'field',
        #     {"code": code, },
        #     node_record, xml_doc_provincias,
        #     {"code": 'att_text', },
        #     order)
        # node_record.appendChild(node_field_name)


def add_township(row):
    """ xml_id: res_country_state_township_pa_ + provincia_code"""
    if row[2].decode('utf-8') not in corregimientos:
        corregimiento = row[2].decode('utf-8')
        # code = corregimiento[0:5].lower()
        id_township = remove_accents(corregimiento)
        id_township = id_township.replace(' ', '_').lower()
        xml_id = 'res_country_state_township_pa_' + id_township

        if xml_id in xml_id_township:
            xml_id = xml_id + str(len(xml_id_township)).decode('utf-8')
            xml_id_township.append(xml_id)
        else:
            xml_id_township.append(xml_id)
        corregimientos.append(corregimiento)
        node_record = add_node(
            'record',
            attrs={"id": xml_id,
                   "model": "res.country.state.district.township"},
            parent_node=main_node_corregimiento,
            minidom_xml_obj=xml_doc_corregimientos,
            attrs_types={"id": "attribute", "model": "attribute"})
        main_node_corregimiento.appendChild(node_record)
        # COUNTRY
        order = ['name', 'ref', ]
        node_field_country = add_node(
            'field',
            {"name": "country_id", "ref": "base.pa", },
            node_record, xml_doc_corregimientos,
            {"name": 'attribute', "ref": 'attribute', },
            order)
        node_record.appendChild(node_field_country)

        # PROVINCIA
        state = row[0].decode('utf-8')
        code = state[0:3].lower()
        state_id = 'l10n_pa_localization.res_country_state_pa_' + code
        order = ['name', 'ref', ]
        node_field_state = add_node(
            'field',
            {"name": "state_id", "ref": state_id, },
            node_record, xml_doc_corregimientos,
            {"name": 'attribute', "ref": 'attribute', },
            order)
        node_record.appendChild(node_field_state)

        # DISTRITO
        distrito = row[1].decode('utf-8')
        id_district = remove_accents(distrito)
        id_district = id_district.replace(' ', '_').lower()
        district_id = 'l10n_pa_localization.res_country_state_district_pa_'\
            + id_district
        order = ['name', 'ref', ]
        node_field_district = add_node(
            'field',
            {"name": "district_id", "ref": district_id, },
            node_record, xml_doc_corregimientos,
            {"name": 'attribute', "ref": 'attribute', },
            order)
        node_record.appendChild(node_field_district)

        # NOMBRE CORREGIMIENTO
        order = ['name']
        node_field_name = add_node(
            'field',
            {"name": corregimiento, },
            node_record, xml_doc_corregimientos,
            {"name": 'att_text', },
            order)
        node_record.appendChild(node_field_name)

        # order = ['code']
        # node_field_name = add_node(
        #     'field',
        #     {"code": code, },
        #     node_record, xml_doc_provincias,
        #     {"code": 'att_text', },
        #     order)
        # node_record.appendChild(node_field_name)


def add_hood(row):
    """ xml_id: res_country_state_township_pa_ + provincia_code"""
    if row[3].decode('utf-8') not in barrios:
        barrio = row[3].decode('utf-8')
        # code = corregimiento[0:5].lower()
        id_hood = remove_accents(barrio)
        id_hood = id_hood.replace(' ', '_').lower()
        xml_id = 'res_country_state_hood_pa_' + id_hood[0:15]

        if xml_id in xml_id_hood:
            xml_id = xml_id + str(len(xml_id_hood)).decode('utf-8')
            xml_id_hood.append(xml_id)
        else:
            xml_id_hood.append(xml_id)

        barrios.append(barrio)
        node_record = add_node(
            'record',
            attrs={"id": xml_id,
                   "model": "res.country.state.district.township.hood"},
            parent_node=main_node_barrio,
            minidom_xml_obj=xml_doc_barrios,
            attrs_types={"id": "attribute", "model": "attribute"})
        main_node_barrio.appendChild(node_record)
        # COUNTRY
        order = ['name', 'ref', ]
        node_field_country = add_node(
            'field',
            {"name": "country_id", "ref": "base.pa", },
            node_record, xml_doc_barrios,
            {"name": 'attribute', "ref": 'attribute', },
            order)
        node_record.appendChild(node_field_country)

        # PROVINCIA
        state = row[0].decode('utf-8')
        code = state[0:3].lower()
        state_id = 'l10n_pa_localization.res_country_state_pa_' + code
        order = ['name', 'ref', ]
        node_field_state = add_node(
            'field',
            {"name": "state_id", "ref": state_id, },
            node_record, xml_doc_barrios,
            {"name": 'attribute', "ref": 'attribute', },
            order)
        node_record.appendChild(node_field_state)

        # DISTRITO
        distrito = row[1].decode('utf-8')
        id_district = remove_accents(distrito)
        id_district = id_district.replace(' ', '_').lower()
        district_id = 'l10n_pa_localization.res_country_state_district_pa_'\
            + id_district
        order = ['name', 'ref', ]
        node_field_district = add_node(
            'field',
            {"name": "district_id", "ref": district_id, },
            node_record, xml_doc_barrios,
            {"name": 'attribute', "ref": 'attribute', },
            order)
        node_record.appendChild(node_field_district)

        # Corregimiento
        township = row[2].decode('utf-8')
        id_township = remove_accents(township)
        id_township = id_township.replace(' ', '_').lower()
        township_id = 'l10n_pa_localization.res_country_state_township_pa_'\
            + id_township
        order = ['name', 'ref', ]
        node_field_township = add_node(
            'field',
            {"name": "township_id", "ref": township_id, },
            node_record, xml_doc_barrios,
            {"name": 'attribute', "ref": 'attribute', },
            order)
        node_record.appendChild(node_field_township)

        # NOMBRE Barrio
        order = ['name']
        node_field_name = add_node(
            'field',
            {"name": barrio, },
            node_record, xml_doc_barrios,
            {"name": 'att_text', },
            order)
        node_record.appendChild(node_field_name)

        # order = ['code']
        # node_field_name = add_node(
        #     'field',
        #     {"code": code, },
        #     node_record, xml_doc_provincias,
        #     {"code": 'att_text', },
        #     order)
        # node_record.appendChild(node_field_name)


for row in csvData:
    add_province(row)
    add_distric(row)
    add_township(row)
    add_hood(row)
f = open(data_path1, 'wb')
f.write(xml_doc_provincias.toprettyxml(indent='    ', encoding='UTF-8'))
f.close()
f = open(data_path2, 'wb')
f.write(xml_doc_distritos.toprettyxml(indent='    ', encoding='UTF-8'))
f.close()
f = open(data_path3, 'wb')
f.write(xml_doc_corregimientos.toprettyxml(indent='    ', encoding='UTF-8'))
f.close()
f = open(data_path4, 'wb')
f.write(xml_doc_barrios.toprettyxml(indent='    ', encoding='UTF-8'))
f.close()

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

import os
import xml.dom.minidom
import csv
import unicodedata
import string
data_path = '../data/cities.xml'
csv_file_path = '../source/cities.csv'


def add_node(node_name, attrs, parent_node,
             minidom_xml_obj, attrs_types, order=False):
    if not order:
        order = attrs
    new_node = minidom_xml_obj.createElement(node_name)
    for key in order:
        if attrs_types[key] == 'attribute':
            new_node.setAttribute(key, attrs[key])
        elif attrs_types[key] == 'textNode':
            key_node = minidom_xml_obj.createElement(key)
            text_node = minidom_xml_obj.createTextNode(attrs[key])
            key_node.appendChild(text_node)
            new_node.appendChild(key_node)
        elif attrs_types[key] == 'att_text':
            new_node.setAttribute('name', key)
            text_node = minidom_xml_obj.createTextNode(attrs[key])
            new_node.appendChild(text_node)
    parent_node.appendChild(new_node)
    return new_node


def remove_accents(data):
    data_unacuate = [x for x in unicodedata.normalize('NFKD', data)
                     if (
                        x in string.ascii_letters) or (x in string.whitespace)]
    result = ''.join(data_unacuate).lower()

    return result
csvData = csv.reader(open(csv_file_path), delimiter=',')
cities = []
csvData.next()  # Headers
xml_doc = xml.dom.minidom.Document()
openerp_node = xml_doc.createElement('openerp')
xml_doc.appendChild(openerp_node)
nodeopenerp = xml_doc.getElementsByTagName('openerp')[0]
main_node = add_node('data', {"noupdate": "True"}, nodeopenerp,
                     xml_doc, attrs_types={"noupdate": "attribute"})
index = 0
for row in csvData:
    city = row[0].decode('utf-8')
    city_state = str(row[1]) + '_' + remove_accents(city)
    city_state = city_state.replace(' ', '_')
    city_state = city_state.lower()
    if city_state not in cities:
        cities.append(city_state)
        city_id = 'res_country_' + city_state
        node_record = add_node('record', {"id": city_id,
                               "model": "res.better.zip"}, main_node,
                               xml_doc, attrs_types={"id": "attribute",
                               "model": "attribute"})
        main_node.appendChild(node_record)
        node_record_attrs = {
            "name": "country_id",
            "ref": "base.pa",
        }
        node_record_attrs_types = {
            "name": 'attribute',
            "ref": 'attribute',
        }
        order = ['name', 'ref', ]

        node_field = add_node('field', node_record_attrs, node_record, xml_doc,
                              node_record_attrs_types, order)
        node_record.appendChild(node_field)

        node_city_attrs = {"city": city, }
        node_city_attrs_types = {"city": 'att_text', }
        order = ['city']
        node_field_city = add_node('field', node_city_attrs, node_record,
                                   xml_doc, node_city_attrs_types, order)
        node_record.appendChild(node_field_city)

f = open(data_path, 'wb')
f.write(xml_doc.toprettyxml(indent='    ', encoding='UTF-8'))
f.close()

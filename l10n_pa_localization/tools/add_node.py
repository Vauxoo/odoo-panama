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
import unicodedata
import string


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
    data_unacuate = [
        x for x in unicodedata.normalize('NFKD', data)
        if (x in string.ascii_letters) or (x in string.whitespace)]
    result = ''.join(data_unacuate).lower()
    return result

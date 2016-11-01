# coding: utf-8

{
    "name": "Panama Withholding",
    "version": "8.0.0.1.0",
    "author": "Vauxoo",
    "category": "Generic Modules",
    "website": "http://www.vauxoo.com/",
    "license": "AGPL-3",
    "depends": [
            "sale_stock",
            "vat_partitioned",
    ],
    "demo": [
        'demo/demo.xml',
    ],
    "data": [
        'view/account_view.xml',
        'view/invoice_view.xml',
        'view/partner_view.xml',
        'view/res_company.xml',
        'view/sale_order_view.xml',
        'workflow/wh_action_server.xml',
        'security/ir.model.access.csv',
    ],
    "test": [],
    "installable": True,
    "external_dependencies": {
        "python": []
    }
}

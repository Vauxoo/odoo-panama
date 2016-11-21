# coding: utf-8

{
    "name": "Panama Report Wizards",
    "version": "8.0.0.1.0",
    "author": "Vauxoo",
    "category": "Generic Modules",
    "website": "http://www.vauxoo.com/",
    "license": "AGPL-3",
    "depends": [
            "l10n_pa_withholding",
    ],
    "demo": [
        'demo/demo.xml',
    ],
    "data": [
        'wizard/form_43_view.xml',
        'wizard/annex_95_view.xml',
        'view/res_partner_view.xml',
        'view/invoice_view.xml',
    ],
    "test": [],
    "installable": True,
    "external_dependencies": {
        "python": []
    }
}

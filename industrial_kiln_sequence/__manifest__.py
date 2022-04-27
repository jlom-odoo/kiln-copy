# -*- coding: utf-8 -*-
{
    'name': "industrial_kiln_added_fields",

    'summary': """
        This module adds Job Number field to sales order when confirmed and quotation and adds plant code to partner info when a sales order
        is confirmed""",

    'description': """
        This module inherits sale order and res partner, adding sequences based in prefixes and suffixes sets from config.
    """,

    'author': "Odoo Inc",
    'website': "https://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations/Product',
    'version': '1.0',
    'license': 'OPL-1',
    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'views/res_config_settings.xml',
        'views/sale_views.xml',
        'views/res_partner_views.xml'   
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}

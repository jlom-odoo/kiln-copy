# -*- coding: utf-8 -*-
{
    'name': "industrial_kiln_added_fields",

    'summary': """
        This module adds job number to sales order and quotation and plant code and sequence to customer info and sales order
        On customer form adds field plant_code which is a sequence for every new customer o is shared by companies with 3 same first letters
        plant_code sequence is updated when a sales order for a new customer is created""",

    'description': """
        This module inherits sale order and res partner, adding two sequences based in prefixes set in config and partner view.
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

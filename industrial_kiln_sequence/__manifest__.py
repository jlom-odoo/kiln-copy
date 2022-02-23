# -*- coding: utf-8 -*-
{
    'name': "industrial_kiln_added_fields",

    'summary': """
        This module adds job number to sales order and quotation 
        On customer form adds field plant_code which is a sequence for every new customer
        plant_code sequence is created when a sales order for a new customer is created""",

    'description': """
        This module inherits product template and populate barcode based on sequence settings  
        modified by the admin user.
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
        'views/view_order_form.xml'    
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}

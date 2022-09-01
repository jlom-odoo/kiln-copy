# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Industrial Kiln & Dryer group : Price calculated based on Margin',
    'version': '1.0',
    'category': 'Customization',
    'description': """
Price calculated based on Margin
===========================================================================
    Task ID: 2886259
    Quadgram: dipa
    """,
    'summary': '',
    'author': 'Odoo Inc',
    'website': 'http://www.odoo.com',
    'license': 'OPL-1',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/res_config_setting_view.xml',
        'data/data.xml'
    ],
    'installable': True,
}

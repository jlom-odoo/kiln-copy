{
    'name': 'Industrialkiln : Total Cost on SO',
    'summary': 'Calculate Total Cost based on field services, parts costs and freight costs',
    'description': '''
    A new monetary calculation field was added to the Cost tab on the Sales Order
    Add new field 'Parts Margin' equal to ('Parts Material Cost'/'Total Cost')/100) %
    New field in settings 'Freight Profit Margin'
    Added new field with the next calculation Freight = (Freight In + Freight Out)/ Freight Profit Margin (from settings) and add this to the SO Total
    Added a new field called 'Total Cost' which is the a sum of the fields 'Material Cost' + 'Overhead Cost' + 'Labor Cost' + 'Parts Material Cost' + 'Freight'
    Add a new field 'Invoiced amount' which they will input manually
    Margin with total freight = (Invoiced amount - Total cost)/ Invoiced amount
    Margin w/o total Freight = (Untaxed amount-Parts Material cost)/untaxed amount
        Developer: [cmgv]
        Task ID: 3571031
    ''',
    'author': 'Odoo Inc',
    'maintainer': 'Odoo Inc',
    'website': 'https://www.odoo.com',
    'category': 'Custom Develpment',
    'version': '1.0.0',
    'depends': [
        'sale_management',
    ],
    'data': [
        'views/sale_order_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'license': 'OPL-1',
}

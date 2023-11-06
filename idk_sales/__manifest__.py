{
    'name': 'Industrialkiln : Total Cost on SO',
    'summary': 'Calculate Total Cost based on field service and parts costs',
    'description': '''
    A new monetary calculation field was added to the Cost tab on the Sales Order
    Added a new field called 'Total Cost' which is the a sum of the fields 'Material Cost' + 'Overhead Cost' + 'Labor Cost' + 'Parts Material Cost'
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
    ],
    'license': 'OPL-1',
}

{
    'name': 'Industrial Kiln : Weekly Report from Friday to Thursday',
    'summary': 'Change weekly report to start from Friday instead of Monday and ends in Thursday',
    'description': '''
        This model changes how Odoo groups the records of a model when choosing the groupby
        Week. User can choose between each day of the week, from which should the grouping should start
        
        Developer: [leml]
        Task ID: 3526468
    ''',
    'author': 'Odoo Inc',
    'maintainer': 'Odoo Inc',
    'website': 'https://www.odoo.com',
    'category': 'Custom Modules',
    'version': '1.0.0',
    'depends': [
        'base_setup',
    ],
    'data': [
        'views/res_config_settings_view_inherit_idk.xml',
    ],
    'license': 'OPL-1',
}

{
    'name': 'Industrial Kiln: Sale Order Mail Activity',
    'summary': 'Add sale order fields to activiy email from automated action',
    'description': """
        This module adds the sale_order_field_ids to both the mail.activity and ir.actions.server models 
        and it uses its values to populate the message_activity_assigned mail template.
        Task Id: 3571043
        Dev: jcsg
    """,
    'version': '1.0.0',
    'category': 'Custom Development',
    'author': 'Odoo Inc',
    'maintainer': 'Odoo Inc',
    'website': 'https://www.odoo.com',
    'license': 'OPL-1',
    'depends': [
        'base_automation',
        'sale',
    ],
    'data': [
        'data/mail_templates.xml',
        'views/base_automation_views.xml',
    ],
}

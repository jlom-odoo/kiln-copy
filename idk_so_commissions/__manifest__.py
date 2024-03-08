{
    "name": "Industrial Kiln: Commission calculation on SO",
    "description": 
    """
    The client pays out commissions to different departments on confirmed SO.
    Each person from a different department gets a different commission
    based on certain conditions (defined through a new model commission.rule).

    - Developer: JLOM
    - Task ID: 3708579
    """,
    "category": "Custom Development",
    "version": "1.0.0",
    "author": "Odoo Development Services",
    "maintainer": "Odoo Development Services",
    "website": "https://www.odoo.com/",
    "license": "OPL-1",
    "depends": [
        "idk_sales",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/commission_rule_views.xml",
        "views/partner_views.xml",
        "views/sale_views.xml",
    ],
}

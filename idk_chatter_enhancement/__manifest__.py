{
    "name": "Industrial Kiln: Chatter Enhancement",
    "summary": """
        Specifying contacts on logged activities
    """,
    "description": """
        Task ID: 3340051
        Chatter enhancement to specify contacts on logged activities
    """,
    "license": "OPL-1",
    "author": "Odoo, Inc.",
    "website": "https://www.odoo.com",
    "category": "Custom Development",
    "version": "1.1.0",
    "depends": ["mail"],
    "data": [
        "views/mail_activity_views.xml",
        "data/mail_templates.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "idk_chatter_enhancement/static/src/models/activity.js",
            "idk_chatter_enhancement/static/src/components/activity/activity.js",
            "idk_chatter_enhancement/static/src/components/activity/activity.scss"
        ],
        "web.assets_qweb": [
            "idk_chatter_enhancement/static/src/components/activity/activity.xml"
        ]
    },
    "installable": True,
    "application": False,
    "auto_install": False
}

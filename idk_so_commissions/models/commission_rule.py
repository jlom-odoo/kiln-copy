from odoo import api, fields, models


class CommissionRule(models.Model):
    _name = "commission.rule"
    _description = "Commission Rules"

    lower_rate = fields.Float(digits=[4,4], 
                              help="Minimum Margin without Freight for this commission to apply")
    higher_rate = fields.Float(default=1.0, 
                               digits=[4,4], 
                               help="Maximum Margin without Freight for this commission to apply")
    commission_percentage = fields.Float(digits=[4,4], 
                                         help="Percentage of 'Invoiced amount' or 'Margin Dollar' that will be provided as commission")
    commission_type = fields.Selection([
        ("kas_fs_in", "KAS FS In District"),
        ("kas_fs_out", "KAS FS Out of District"),
        ("kas_parts", "KAS Parts"),
        ("dm", "DM"),
        ("ts", "TS"),
    ], required=True)

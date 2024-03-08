from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    commission_district = fields.Selection([
        ("in_district", "In District"),
        ("out_district", "Out of District"),
    ], default="in_district")

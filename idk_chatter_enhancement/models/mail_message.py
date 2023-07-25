from odoo import fields, models

class Message(models.Model):
    _inherit = "mail.message"

    idk_contact = fields.Many2one(string="Contact", comodel_name="res.partner", help="Who was spoken to")
    idk_company = fields.Many2one(string="Company", comodel_name="res.partner")

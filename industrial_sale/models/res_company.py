from odoo import models, fields


class Company(models.Model):
    _inherit = 'res.company'

    overhead_margin = fields.Float(string='Overhead Margin')

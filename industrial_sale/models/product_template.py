from odoo import fields, models


class Product(models.Model):
    _inherit = 'product.template'

    job_type = fields.Many2one('job.type')

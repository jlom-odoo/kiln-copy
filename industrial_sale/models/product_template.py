from odoo import fields, models


class Product(models.Model):
    _inherit = 'product.template'

    margin_calculation = fields.Selection([('FS','FS'),('Parts','Parts')])

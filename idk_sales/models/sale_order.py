from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    material_cost = fields.Monetary(currency_field='currency_id', string='Material Cost')
    overhead_cost = fields.Monetary(currency_field='currency_id', string='Overhead Cost')
    labor_cost = fields.Monetary(currency_field='currency_id', string='Labor Cost')
    parts_material_cost = fields.Monetary(currency_field='currency_id', string='Parts Material Cost')
    total_cost = fields.Monetary(currency_field='currency_id', string='Total Cost', compute='_compute_total_cost')

    @api.depends('material_cost', 'overhead_cost', 'parts_material_cost', 'total_cost')
    def _compute_total_cost(self):
        for order in self:
            order.total_cost = order.material_cost + order.overhead_cost + order.labor_cost + order.parts_material_cost


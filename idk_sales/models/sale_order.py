from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    freight = fields.Monetary(currency_field='currency_id', compute="_compute_freight",string='Freight')
    freight_in = fields.Monetary(currency_field='currency_id', string='Freight In')
    freight_out = fields.Monetary(currency_field='currency_id', string='Freight Out')
    labor_cost = fields.Monetary(currency_field='currency_id', string='Labor Cost')
    material_cost = fields.Monetary(currency_field='currency_id', string='Material Cost')
    margin_with_freight = fields.Float(string='Margin with Freight', compute='_compute_margin_with_freight')
    margin_without_freight = fields.Float(string='Margin without Freight', compute='_compute_margin_without_freight')
    overhead_cost = fields.Monetary(currency_field='currency_id', string='Overhead Cost')
    parts_material_cost = fields.Monetary(currency_field='currency_id', string='Parts Material Cost')
    parts_margin = fields.Float(string='Parts Margin', compute="_compute_parts_margin", default=0.0)
    total_cost = fields.Monetary(currency_field='currency_id', string='Total Cost', compute='_compute_total_cost')
    invoiced_amount = fields.Monetary(currency_field='currency_id', string='Invoiced Amount', default=0.0)

    @api.depends('material_cost', 'overhead_cost', 'parts_material_cost', 'total_cost','freight')
    def _compute_total_cost(self):
        for order in self:
            order.total_cost = order.material_cost + order.overhead_cost + order.labor_cost + order.parts_material_cost + order.freight

    @api.depends('parts_material_cost','total_cost', 'parts_margin')
    def _compute_parts_margin(self):
        order_ids = self.filtered(lambda a: a.total_cost > 0)
        no_order_ids = self - order_ids
        no_order_ids.parts_margin= 0.0 
        margin_values = {order.id: ((order.parts_material_cost / order.total_cost)) for order in order_ids}
        for order in order_ids:
            order.parts_margin = margin_values.get(order.id)
    
    @api.depends('freight_in','freight_out','freight')
    def _compute_freight(self):
        freight_profit_margin = float(self.env['ir.config_parameter'].sudo().get_param('sale.freight_profit_margin'))
        if freight_profit_margin:
            for order in self:
                order.freight = (order.freight_in + order.freight_out) / freight_profit_margin
        else:
            self.freight = 0.0

    @api.depends('invoiced_amount','margin_with_freight')
    def _compute_margin_with_freight(self):
        invoiced_ids = self.filtered(lambda a: a.invoiced_amount > 0)
        no_invoiced_ids = self - invoiced_ids
        no_invoiced_ids.margin_with_freight = 0.0 
        for order in invoiced_ids:
            order.margin_with_freight = ((order.invoiced_amount - order.total_cost) / order.invoiced_amount)

    @api.depends('amount_untaxed','margin_without_freight')
    def _compute_margin_without_freight(self):
        untaxed_ids = self.filtered(lambda a: a.amount_untaxed > 0)
        no_untaxed_ids = self - untaxed_ids
        no_untaxed_ids.margin_without_freight = 0.0 
        for order in untaxed_ids:
            order.margin_without_freight = ((order.amount_untaxed - order.parts_material_cost) / order.amount_untaxed)

    @api.depends('order_line.price_total','freight')
    def _amount_all(self):
        super()._amount_all()
        for order in self.filtered(lambda a: a.freight > 0):
            order.update({
                'amount_total': order.amount_total + order.freight,
            })
            

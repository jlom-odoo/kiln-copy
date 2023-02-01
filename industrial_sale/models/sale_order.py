from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_cost = fields.Monetary('Total Cost', help='Total cost of the sale order', compute='_compute_total_cost')

    @api.depends('order_line')
    def _compute_total_cost(self): 
        for order in self: 
            order.total_cost = sum([line.product_uom_qty * line.editable_cost for line in order.order_line])


class SaleOrderline(models.Model):
    _inherit = 'sale.order.line'

    margin_calculation = fields.Selection(related='product_id.margin_calculation')

    fs_margin = fields.Float('FS Margin', help='fs margin', compute='_compute_fs_margin', store=True) 

    editable_cost = fields.Float('Cost', compute='_compute_default_cost', help='Defaults to the cost of the product but is meant to be editable aswell', readonly=False, store=True)
    line_margin = fields.Selection(string='Price Margin', selection=[(str(x), str(x)+'%') for x in range(30,71)], default='30')


    @api.depends('editable_cost', 'price_unit', 'line_margin')
    def _compute_fs_margin(self):
        for line in self:
            line.fs_margin = 0

            is_field_service = line.product_id.margin_calculation == 'FS'
            if line.price_unit and line.editable_cost and is_field_service:
                line.fs_margin = (line.price_unit - line.editable_cost)/line.price_unit

    @api.onchange('line_margin','price_unit')
    def _compute_fs_cost(self):
        for line in self:
            margin_calculation = line.product_id.margin_calculation == 'FS'
            line.editable_cost = line.price_unit - ((int(line.line_margin)/100) * line.price_unit) if margin_calculation else line.editable_cost
            
    @api.onchange('editable_cost','line_margin')
    def recompute_sales_price(self):
        for line in self.filtered(lambda l: l.product_id.margin_calculation == 'Parts'):
            overhead_margin = self.env.company.overhead_margin
            line.price_unit = line.editable_cost / ((100 - int(line.line_margin))/100) +((overhead_margin/100) * line.editable_cost)

    @api.depends('product_id')
    def _compute_default_cost(self):
        for line in self.filtered('id'):
            line.editable_cost = line.product_id.standard_price

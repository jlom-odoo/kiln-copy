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

    fs_margin = fields.Float('FS Margin', help='fs margin', compute='_compute_fs_margin') 
    editable_cost = fields.Float('Cost', compute='_compute_default_cost', help='Defaults to the cost of the product but is meant to be editable aswell', default=0, store=True)
    parts_margin = fields.Selection(string='Price Margin', selection=[(str(x), str(x)+'%') for x in range(30,71)], default='30')


    @api.depends('product_id')
    def _compute_fs_margin(self):
        for line in self:
            is_field_service = line.product_id.job_type == self.env.ref('industrial_sale.jt_field_service')

            line.fs_margin = (line.price_unit - line.editable_cost)/line.price_unit if is_field_service else 0

    @api.onchange('parts_margin')
    def recompute_sales_price(self):
        for line in self:
            if line.product_id.job_type == self.env.ref('industrial_sale.jt_parts'):
                overhead_margin = self.env.company.overhead_margin
                line.price_unit = (line.editable_cost / int(line.parts_margin)) +(overhead_margin * line.editable_cost)

    @api.depends('product_id', 'product_uom_qty')
    def _compute_default_cost(self):
        for line in self:
            line.editable_cost = line.editable_cost

            if line.product_id:
                line.editable_cost = line.product_id.standard_price

            if line.product_id.job_type == self.env.ref('industrial_sale.jt_parts'):
                overhead_margin = self.env.company.overhead_margin
                line.price_unit = (line.editable_cost * (1 + (100 - int(line.parts_margin)) / 100)) + ((100 - overhead_margin)/100 * line.editable_cost)

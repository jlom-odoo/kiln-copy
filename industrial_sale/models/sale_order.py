from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_cost = fields.Monetary('Total Cost', help='Total cost of the sale order', compute='_compute_total_cost')

    def _compute_total_cost(self): 
        for rec in self: 
            lines = rec.order_line

            sum = 0
            for line in lines: 
                sum += line.product_uom_qty * line.editable_cost

            rec.total_cost = sum


class SaleOrderline(models.Model):
    _inherit = 'sale.order.line'

    fs_margin = fields.Float('FS Margin', help='fs margin', compute='_compute_fs_margin')          #FS Margin = ((Sales price - cost)/Sales price) (Read-only field)
    editable_cost = fields.Float('Cost', compute='_compute_default_cost', help='Defaults to the cost of the product but is meant to be editable aswell', default=0, store=True)
    parts_margin = fields.Selection(string='Price Margin', selection=[(str(x), str(x)+'%') for x in range(30,71)], default='30')

    def _compute_fs_margin(self):
        for rec in self:
            rec.fs_margin = 0

            if rec.product_id and rec.product_id.job_type.name == 'Field Service':
                rec.fs_margin = (rec.price_unit - rec.editable_cost)/rec.price_unit

    @api.onchange('parts_margin')
    def recompute_sales_price(self):
        for rec in self:
            if rec.product_id.job_type.name == 'Parts':
                overhead_margin = self.env.company.overhead_margin
                rec.price_unit = (rec.editable_cost / int(rec.parts_margin)) +(overhead_margin * rec.editable_cost)

    @api.depends('product_id', 'product_uom_qty')
    def _compute_default_cost(self):
        for rec in self:
            if rec.product_id:
                rec.editable_cost = rec.product_id.standard_price

            if rec.product_id.job_type.name == 'Parts':
                overhead_margin = self.env.company.overhead_margin
                rec.price_unit = (rec.editable_cost * (1 + (100-int(rec.parts_margin))/100)) + ((100- overhead_margin)/100 * rec.editable_cost)

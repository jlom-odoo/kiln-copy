from odoo import api, fields, models


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    sale_order_field_ids = fields.Many2many(comodel_name='ir.model.fields', string='Sale Order Fields')
    sale_order_id = fields.Many2one(comodel_name='sale.order', ondelete='set null', string='Sale Order', compute='_compute_sale_order_id', compute_sudo=True, store=True)
    has_sale_order_info = fields.Boolean(string='Has Sale Order Information', compute='_compute_has_sale_order_info')

    @api.depends('res_model', 'res_id')
    def _compute_sale_order_id(self):
        sale_order_activities = self.filtered(lambda r: r.res_model == 'sale.order')
        activities = self - sale_order_activities
        activities.sale_order_id = False
        if sale_order_activities:
            record_values = {record.id: record for record in self.env[sale_order_activities[-1].res_model].browse(sale_order_activities.mapped('res_id'))}
            for activity in sale_order_activities:
                activity.sale_order_id = record_values.get(activity.res_id).id

    @api.depends('sale_order_id', 'sale_order_field_ids')
    def _compute_has_sale_order_info(self):
        for activity in self:
            activity.has_sale_order_info = activity.sale_order_id and activity.sale_order_field_ids

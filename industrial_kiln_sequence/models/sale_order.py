from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    job_number = fields.Char('Job Number', compute='set_job_number', store=True, copy=False)
    sequence_job_number = fields.Char(string='Sequence Job number', copy=False)
    prefix_job_number = fields.Selection(string='Prefix Job Number', selection="get_prefix_set", copy=False)
    suffix_job_number = fields.Selection(string='Suffix Job number', selection="get_suffix_set", copy=False)
    has_job_number = fields.Boolean('Has Job Number', copy=False)
    plant_code = fields.Char(string='Plant Code', related='partner_id.commercial_partner_id.plant_code', store=True, copy=False)
    # just to ensure, the error should not be present
    
    _sql_constraints = [
        ('job_number_uniq', 'unique(job_number)',
+         " Field job_number should be unique. Use valid Job Number")
    ]


    def set_next_job_number_sequence(self):
        for order in self:
            if self.env['ir.config_parameter'].sudo().get_param("sale.job_number_activate"):
                next_job_number = self.env['ir.sequence'].next_by_code('sale.order.job.number')
                if next_job_number:
                    order.sequence_job_number = next_job_number
                else:
                    order.sequence_job_number = False
            else:
                order.sequence_job_number = False

    def get_prefix_set(self):
        job_number_activated = self.env['ir.config_parameter'].sudo().get_param("sale.job_number_activate")
        prefix_job_number_set = self.env['ir.config_parameter'].sudo().get_param("sale.prefix_job_number_set")
        if job_number_activated and prefix_job_number_set:
            prefix_values = prefix_job_number_set.split(",")
            prefix_array = []
            for x in prefix_values:
                prefix_array.append((x.upper(), x.upper()))
            return prefix_array
        else:
            return [('select', 'Select')]

    def get_suffix_set(self):
        job_number_activated = self.env['ir.config_parameter'].sudo().get_param("sale.job_number_activate")
        suffix_job_number_set = self.env['ir.config_parameter'].sudo().get_param("sale.suffix_job_number_set")
        if job_number_activated and suffix_job_number_set:
            suffix_values = suffix_job_number_set.split(",")
            suffix_array = []
            for x in suffix_values:
                suffix_array.append((x.upper(), x.upper()))
            return suffix_array
        else:
            return [('select', 'Select')]

    @api.depends('prefix_job_number', 'suffix_job_number' ,'sequence_job_number')
    def set_job_number(self):
        for order in self:
            if order in self.filtered(lambda rec: (rec.prefix_job_number or rec.suffix_job_number) and rec.sequence_job_number):
                order.job_number = (order.prefix_job_number if order.prefix_job_number else '') + order.sequence_job_number + (order.suffix_job_number if order.suffix_job_number else '')
                if not order.has_job_number:
                    order.has_job_number = True
            else:
                order.job_number = False

                order.has_job_number = False

    def action_confirm(self):
        self.set_next_job_number_sequence()
        for order in self:
            if not order.plant_code:
                order.partner_id.commercial_partner_id.create_plant_code()
        super().action_confirm()

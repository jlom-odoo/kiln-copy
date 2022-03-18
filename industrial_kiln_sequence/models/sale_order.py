#-*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_next_job_number_sequence(self):
        if not self.env['ir.config_parameter'].sudo().get_param("sale.job_number_activate"):
            return False
        next_job_number=self.env['ir.sequence'].search([('code', '=', 'sale.order.job.number')]).number_next_actual 
        if next_job_number:
            return next_job_number
        else:
            return

    job_number = fields.Char('Job Number', compute='job_sequence_update', store=True)
    sequence_job_number = fields.Char(string='Sequence Job number', default=_get_next_job_number_sequence, store=True)
    prefix_job_number = fields.Selection(string='Prefix Job Number', selection="get_prefix_set")
    suffix_job_number = fields.Selection(string='Suffix Job number', selection="get_suffix_set")
    has_job_number = fields.Boolean('job number set al least once for this record', default=False, store=True)
    partner_parent_name = fields.Char(related='partner_id.parent_name')
    plant_code = fields.Char(string='Plant Code', related='partner_id.plant_code')
    plant_sequence = fields.Char(string='Plant code sequence')
    has_plant_code_sequence = fields.Boolean('plant number set al least once for this record', default=False, store=True)

    def get_prefix_set(self) :
        prefix_job_number_set = self.env['ir.config_parameter'].sudo().get_param("sale.prefix_job_number_set")
        if prefix_job_number_set:
            prefix_values = prefix_job_number_set.split(",")
            prefix_array = []
            for x in prefix_values:
                prefix_array.append((x.lower(), x.upper()))
            return prefix_array
        else:
            return

    def get_suffix_set(self):
        suffix_job_number_set = self.env['ir.config_parameter'].sudo().get_param("sale.suffix_job_number_set")
        if suffix_job_number_set:
            suffix_values = suffix_job_number_set.split(",")
            suffix_array = []
            for x in suffix_values:
                suffix_array.append((x.lower(), x.upper()))
            return suffix_array
        else:
            return

    @api.onchange('prefix_job_number', 'suffix_job_number')
    def set_job_number(self):
        for order in self.filtered(lambda rec: rec.prefix_job_number and rec.sequence_job_number and rec.suffix_job_number):
            order.job_number = order.prefix_job_number + order.sequence_job_number + order.suffix_job_number
            # job number can change but the sequence number will not increase
            if not order.has_job_number:
                self.env['ir.sequence'].next_by_code('sale.order.job.number')
                order.has_job_number = True

    @api.onchange('partner_id', 'plant_code')
    def update_plant_code(self):
        for order in self.filtered(lambda rec: rec.plant_code):
            plant_code_sequence = str(self.env['ir.sequence'].search([('code', '=', 'res.partner.' + self.plant_code)]).number_next_actual)
            plant_code_sequence = '0000' + plant_code_sequence
            plant_code_sequence = plant_code_sequence[len(plant_code_sequence)-5:]
            order.plant_sequence = order.plant_code + plant_code_sequence[0:3] + '-' + plant_code_sequence[3:]
            if not order.has_plant_code_sequence:
                order.has_plant_code_sequence = True
                self.env['ir.sequence'].next_by_code('res.partner.' + self.plant_code)
        for order in self.filtered(lambda rec: not rec.plant_code): 
            order.plant_sequence = False
     
        
               
         

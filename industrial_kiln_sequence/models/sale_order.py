#-*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
     _inherit = 'sale.order'

     def _get_next_job_number_sequence(self):
        next_job_number=self.env['ir.sequence'].search([('code', '=', 'sale.order.job.number')]).number_next_actual
        if next_job_number:
          return next_job_number
        else:
          return   

     def get_prefix_set(self) : 
        print('OOOOOOOOOOOOO  options prefix', self.env['ir.config_parameter'].sudo().get_param("sale.prefix_job_number_set"))
        prefix_job_number_set = self.env['ir.config_parameter'].sudo().get_param("sale.prefix_job_number_set")
        prefix_values = prefix_job_number_set.split(",")
        prefix_array = []
        for x in prefix_values:
          prefix_array.append((x.lower(),x.upper()))
        print('prefix array',prefix_array)  
        return prefix_array

     def get_suffix_set(self) : 
        print('OOOOOOOOOOOO options suffix', self.env['ir.config_parameter'].sudo().get_param("sale.suffix_job_number_set"))
        suffix_job_number_set = self.env['ir.config_parameter'].sudo().get_param("sale.suffix_job_number_set")
        suffix_values = suffix_job_number_set.split(",")
        suffix_array = []
        for x in suffix_values:
          suffix_array.append((x.lower(),x.upper()))
        return suffix_array

     prefix_job_number = fields.Selection(string='Prefix Job Number',selection="get_prefix_set",store=False)
     sequence_job_number = fields.Char(string='Sequence Job number',default=_get_next_job_number_sequence, store=False)
     suffix_job_number = fields.Selection(string='Suffix Job number',selection="get_suffix_set", store=False)
     job_number= fields.Char('Job Number', compute='compute_job_number')

     @api.depends('prefix_job_number','suffix_job_number')
     def compute_job_number(self):
        if self.sequence_job_number and self.sequence_job_number:  
          self.job_number = self.prefix_job_number + self.sequence_job_number + self.suffix_job_number

     def action_confirm(self):
        self.env['ir.sequence'].next_by_code('sale.order.job.number')  
        return super(SaleOrder, self).action_confirm()     

        
               
         

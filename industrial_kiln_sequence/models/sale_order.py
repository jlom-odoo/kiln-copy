#-*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
     _inherit = 'sale.order'

     def _get_next_job_number_sequence(self):      
        if not self.env['ir.config_parameter'].sudo().get_param("sale.job_number_activate"):
          return False
        next_job_number=self.env['ir.sequence'].search([('code', '=', 'sale.order.job.number')]).number_next_actual
        # next_job_number=self.env['ir.sequence'].next_by_code('sale.order.job.number') 
        if next_job_number:
          print('NNNNNNNNNNNNNN Next job number',next_job_number)
          return next_job_number
        else:
          return  

     job_number = fields.Char('Job Number',compute='job_sequence_update',store=True)
     sequence_job_number = fields.Char(string='Sequence Job number',default=_get_next_job_number_sequence, store=True)
     prefix_job_number = fields.Selection(string='Prefix Job Number',selection="get_prefix_set")
     suffix_job_number = fields.Selection(string='Suffix Job number',selection="get_suffix_set")
     has_job_number = fields.Boolean('job number set al least once for this record', default=False, store=True)
    #  partner_parent_name = fields.Char(related='partner_id.parent_name')
    #  plant_code = fields.Char(string='Plant Code', related='partner_id.plant_code')
    #  plant_sequence = fields.Char(string= 'Plant sequence', related='partner_id.plant_sequence')
    #  country_id = fields.Char(string= 'Country', related='partner_id.country_id')
    #  country_id = fields.One2many('res.partner', string='Country', inverse='country_id')

     def get_prefix_set(self) : 
        print('OOOOOOOOOOOOO  options prefix', self.env['ir.config_parameter'].sudo().get_param("sale.prefix_job_number_set"))
        prefix_job_number_set = self.env['ir.config_parameter'].sudo().get_param("sale.prefix_job_number_set")
        if prefix_job_number_set:
          prefix_values = prefix_job_number_set.split(",")
          prefix_array = []
          for x in prefix_values:
            prefix_array.append((x.lower(),x.upper())) 
          return prefix_array
        else: return  

     def get_suffix_set(self) : 
        print('OOOOOOOOOOOO options suffix', self.env['ir.config_parameter'].sudo().get_param("sale.suffix_job_number_set"))
        suffix_job_number_set = self.env['ir.config_parameter'].sudo().get_param("sale.suffix_job_number_set")
        if suffix_job_number_set:
          suffix_values = suffix_job_number_set.split(",")
          suffix_array = []
          for x in suffix_values:
            suffix_array.append((x.lower(),x.upper()))
          return suffix_array
        else: return  

    #  @api.depends('partner_parent_name','company_name', 'plant_code')
    #  def create_plant_code(self):  
    #    for order in self:
    #       if not order.plant_sequence:
    #         print('PPPPPPPPPP partner_parent_name', self.partner_parent_name)
    #         print('PPPPPPPPPP partner_company_id', self.company_id)
    #         company_name= order.company_id or order.partner_parent_name
    #         if company_name:
    #           if not order.plant_code:
    #             order.plant_code = self.first_letters(company_name)
    #             order.create_sequence('res.partner.'+ order.plant_code)
    #           else:
    #             order.plant_sequence = self.env['ir.sequence'].search([('code', '=', 'res.partner.'+ self.plant_code)]).number_next_actual 

     def first_letters(self, partner_name):
        alphanumeric = ""
        for character in partner_name:
          if character.isalnum():
            alphanumeric += character
        # alphanumeric += self.country_id[:3]    
        alphanumeric += 'XYZ'
        return alphanumeric[:3]

    #  def create_sequence(self,sequence_code): 
    #     current_sequence = self.env['ir.sequence'].search([('code', '=', sequence_code)])
    #     new_vals = {
    #                 'name': 'Plant sequence Industrial Kiln '+ sequence_code,
    #                 'code': sequence_code,
    #                 'implementation': 'standard',
    #                 'prefix': '',
    #                 'suffix': '',
    #                 'number_next_actual': 1,
    #                 'padding': 0,
    #                 'number_increment': 1
    #             }
    #     if not current_sequence:         
    #       self.env['ir.sequence'].create(new_vals)  
    #     else:
    #       self.plant_sequence=self.env['ir.sequence'].next_by_code('res.partner.'+ self.plant_code)    

     @api.onchange('prefix_job_number','suffix_job_number')
     def set_job_number(self):
        print('EEEEEEstamos hasta el loly')
        for order in self.filtered(lambda rec: rec.prefix_job_number and rec.sequence_job_number and rec.suffix_job_number):
        # for order in self:  
          print('CCCCCCCCC Compute job_number')
          order.job_number = order.prefix_job_number + order.sequence_job_number + order.suffix_job_number
          #job number can change but the sequence number will not increase
          if not order.has_job_number:
            self.env['ir.sequence'].next_by_code('sale.order.job.number')
            order.has_job_number = True

   
        
               
         

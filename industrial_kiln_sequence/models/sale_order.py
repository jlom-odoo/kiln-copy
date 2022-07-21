#-*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    job_number = fields.Char('Job Number', compute='set_job_number', store=True)
    sequence_job_number = fields.Char(string='Sequence Job number')
    prefix_job_number = fields.Selection(string='Prefix Job Number', selection="get_prefix_set")
    suffix_job_number = fields.Selection(string='Suffix Job number', selection="get_suffix_set")
    has_job_number = fields.Boolean('Has Job Number')
    plant_code = fields.Char(string='Plant Code', compute='_compute_plant_code', store=True, readonly=True)

    #just to ensure, the error should not be present
    _sql_constraints = [
        ('sequence_job_number_uniq', 'unique(sequence_job_number)', " Field sequence_job_number should be unique. Use valid Job Number settings")
    ]

    @api.depends('partner_id')
    def _compute_plant_code(self): 
        for order in self:
            order.plant_code = False
            partner = order.partner_id
            if partner.parent_id.plant_code:
                order.plant_code = partner.parent_id.plant_code
            elif partner.plant_code:
                order.plant_code = partner.plant_code   

    def _set_plant_code(self): 
        for order in self:
            partner = self.partner_id
            if not order.plant_code:
                if partner.is_company or partner.parent_id:
                    plant_initials = self.first_letters(partner,partner.display_name)
                    self.create_sequence('res.partner.' + plant_initials)
                    plant_code_sequence = self.env['ir.sequence'].next_by_code('res.partner.' + plant_initials)
                    plant_code_sequence = '00' + str(plant_code_sequence)
                    plant_code_sequence = plant_code_sequence[len(plant_code_sequence)-5:]
                    order.plant_code = plant_initials + plant_code_sequence[0:3] + '-' + plant_code_sequence[3:]
                    if partner.parent_id:
                        partner.sudo().parent_id.plant_code = order.plant_code
                    else:
                        partner.sudo().plant_code = order.plant_code    
                else:
                    order.plant_code = False                

    def first_letters(self, partner, partner_name):
        alphanumeric = ""
        for character in partner_name:
            if character.isalnum():
                alphanumeric += character.upper()    
        if partner.country_id:    
            alphanumeric += partner.country_id.name[:3].upper()
        return alphanumeric[:3]

    def create_sequence(self, sequence_name):
        current_sequence = self.env['ir.sequence'].search([('code', '=', sequence_name)])
        if not current_sequence:
            new_vals = {
                    'name': 'Industrial Kiln ' + sequence_name,
                    'code': sequence_name,
                    'implementation': 'standard',
                    'prefix': '',
                    'suffix': '',
                    'number_next': 100,
                    'padding': 0,
                    'number_increment': 1
                }
            self.env['ir.sequence'].create(new_vals)

    def set_next_job_number_sequence(self):
        for order in self:
            if self.env['ir.config_parameter'].sudo().get_param("sale.job_number_activate"):
                next_job_number = self.env['ir.sequence'].next_by_code('sale.order.job.number')
                if next_job_number: 
                    order.sequence_job_number=next_job_number
                else:   
                    order.sequence_job_number = False      
            else:
                order.sequence_job_number = False


    def get_prefix_set(self) :
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

    @api.depends('prefix_job_number', 'suffix_job_number')
    def set_job_number(self):  
        for order in self:
            if order in self.filtered(lambda rec: rec.prefix_job_number and rec.prefix_job_number != '' and rec.sequence_job_number and rec.suffix_job_number and rec.prefix_job_number != ''):
                order.job_number = order.prefix_job_number + order.sequence_job_number + order.suffix_job_number
                if not order.has_job_number:
                    order.has_job_number = True
            else:
                order.job_number = False   
                
                order.has_job_number = False 
           
    def action_confirm(self): 
        self.set_next_job_number_sequence()
        self._set_plant_code()
        super(SaleOrder, self).action_confirm()

#-*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
     _inherit = 'res.partner'

     plant_code = fields.Char(string='Plant Code',default=False)
     plant_sequence = fields.Char(string='Plant sequence', default=False)
     plant_code_sequence = fields.Char(string='Plant code and sequence', compute='_compute_plant_code_sequence')

     def _compute_plant_code_sequence(self):
         for partner in self: 
            if partner.plant_code and partner.plant_sequence:
               partner.plant_code_sequence = partner.plant_code + partner.plant_sequence
            else:
               partner.plant_code_sequence=False

   

        
               
         

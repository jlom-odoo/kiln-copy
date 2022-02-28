#-*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
     _inherit = 'res.partner'

     plant_code = fields.Char(string='Plant Code')
     plant_sequence = fields.Char(string='Plant sequence')


   

        
               
         

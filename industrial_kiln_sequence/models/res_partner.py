#-*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    plant_code = fields.Char(string='Plant Code', compute='_compute_plant_code' , store=True)

    @api.depends('customer_rank')
    def _compute_plant_code(self): 
        for partner in self:
            print('Partner name', partner.display_name or 'noName')
            if not partner.plant_code and partner.is_company:
                if partner.customer_rank == 1 and partner.display_name:
                    plant_initials = self.first_letters(partner, partner.display_name)
                    self.create_sequence('res.partner.' + plant_initials)
                    plant_code_sequence = self.env['ir.sequence'].next_by_code('res.partner.' + plant_initials)
                    plant_code_sequence = '00' + str(plant_code_sequence)
                    plant_code_sequence = plant_code_sequence[len(plant_code_sequence)-5:]
                    partner.plant_code = plant_initials + plant_code_sequence[0:3] + '-' + plant_code_sequence[3:]
                else:
                    partner.plant_code = False    
            else:
                partner.plant_code = False   
                    
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

    def _compute_plant_code_action(self): 
        for partner in self:
            print('Partner name', partner.display_name or 'noName')
            if  partner.display_name:
                plant_initials = self.first_letters(partner, partner.display_name)
                self.create_sequence('res.partner.' + plant_initials)
                plant_code_sequence = self.env['ir.sequence'].next_by_code('res.partner.' + plant_initials)
                plant_code_sequence = '00' + str(plant_code_sequence)
                plant_code_sequence = plant_code_sequence[len(plant_code_sequence)-5:]
                partner.plant_code = plant_initials + plant_code_sequence[0:3] + '-' + plant_code_sequence[3:]
            else:
                partner.plant_code = False    
            
    @api.model
    def action_set_plant_code(self):
        self.search([('plant_code', '=', False), ('customer_rank', '=', 1), ('is_company', '=', True)])._compute_plant_code_action()           
         

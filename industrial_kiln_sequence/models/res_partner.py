#-*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    plant_code = fields.Char(string='Plant Code', store=True)

    @api.depends('is_company', 'name', 'parent_id.display_name', 'type', 'company_name')
    def _compute_display_name(self):
        super(ResPartner, self)._compute_display_name()
        for partner in self:
            if partner.parent_name:
                partner.plant_code = self.first_letters(self.parent_name)
            else:
                if partner.display_name:
                    partner.plant_code = self.first_letters(self.display_name)
                else:
                    partner.plant_code = self.first_letters(self.name)
            partner.create_sequence('res.partner.' + partner.plant_code)

    def first_letters(self, partner_name):
        alphanumeric = ""
        for character in partner_name:
            if character.isalnum():
                alphanumeric += character.upper()
        if self.country_id:    
            alphanumeric += self.country_id.name[:3]
        return alphanumeric[:3]

    def create_sequence(self, sequence_code):
        current_sequence = self.env['ir.sequence'].search([('code', '=', sequence_code)])
        new_vals = {
                    'name': 'Plant sequence Industrial Kiln ' + sequence_code,
                    'code': sequence_code,
                    'implementation': 'standard',
                    'prefix': '',
                    'suffix': '',
                    'number_next_actual': 1,
                    'padding': 5,
                    'number_increment': 1
                }
        if not current_sequence:
            self.env['ir.sequence'].create(new_vals)
                    

   

        
               
         

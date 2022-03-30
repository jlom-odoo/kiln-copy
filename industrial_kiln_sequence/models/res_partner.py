#-*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    plant_code = fields.Char(string='Plant Code', store=True)
    parent_plant_code = fields.Char(related='parent_id.plant_code', string='Parent plant code',store=True)

    @api.depends('is_company', 'name', 'parent_id.display_name', 'type', 'company_name')
    def _compute_display_name(self):
        super(ResPartner, self)._compute_display_name()
        for partner in self:
            if partner.is_company:
                plant_initials = self.first_letters(partner.display_name)
                partner.create_sequence('res.partner.' + plant_initials)
                plant_code_sequence = self.env['ir.sequence'].next_by_code('res.partner.' + plant_initials)
                plant_code_sequence = '00' + str(plant_code_sequence)
                plant_code_sequence = plant_code_sequence[len(plant_code_sequence)-5:]
                partner.plant_code = plant_initials + plant_code_sequence[0:3] + '-' + plant_code_sequence[3:]
            else:
                if partner.parent_plant_code:
                    partner.plant_code=partner.parent_plant_code
                else:
                    partner.plant_code=False

    def first_letters(self, partner_name):
        alphanumeric = ""
        for character in partner_name:
            if character.isalnum():
                alphanumeric += character.upper()
        if self.country_id:    
            alphanumeric += self.country_id.name[:3]
        return alphanumeric[:3]

    def create_sequence(self, sequence_name):
        current_sequence = self.env['ir.sequence'].search([('code', '=', sequence_name)])
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
        if not current_sequence:
            self.env['ir.sequence'].create(new_vals)
          

   

        
               
         

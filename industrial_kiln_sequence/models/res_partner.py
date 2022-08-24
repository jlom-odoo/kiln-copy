# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    plant_code = fields.Char(string='Plant Code', store=True, copy=False)

    def get_plant_code(self, partner_name, country_id=False):
        plant_initials = self.first_letters(partner_name, country_id)
        self.create_sequence('res.partner.' + plant_initials)
        plant_code_sequence = self.env['ir.sequence'].next_by_code('res.partner.' + plant_initials)
        plant_code_sequence = '00' + str(plant_code_sequence)
        plant_code_sequence = plant_code_sequence[len(plant_code_sequence)-5:]
        return plant_initials + plant_code_sequence[0:3] + '-' + plant_code_sequence[3:]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_company'):
                if not vals.get('plant_code') and vals.get('customer_rank') == 1 and vals.get('name'):
                    vals['plant_code'] = self.get_plant_code(vals['name'], vals.get('country_id', False))
            else:
                vals['plant_code'] = False
        return super(Partner, self).create(vals_list)
    
    def first_letters(self, partner_name, country_id=False):
        alphanumeric = ""
        for character in partner_name:
            if character.isalnum():
                alphanumeric += character.upper()
        if country_id:
            alphanumeric += self.env['res.country'].browse(country_id).name[:3].upper()
        return alphanumeric[:3]
    
    def create_plant_code(self):
        for partner in self:
            partner.sudo().plant_code = partner.get_plant_code(partner.name, partner.country_id.id)

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
            self.env['ir.sequence'].sudo().create(new_vals)

    def action_set_plant_code(self):
        self.search([('is_company', '=', True), ('plant_code', '=', False),
                    ('customer_rank', '>=', 1)]).create_plant_code()

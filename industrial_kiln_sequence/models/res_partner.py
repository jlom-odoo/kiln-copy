# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    plant_code = fields.Char(string='Plant Code', store=True)


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_company'):
                if not vals.get('plant_code') and vals.get('customer_rank') == 1 and vals.get('name'):
                    plant_initials = self.first_letters(vals, vals.get('name'))
                    self.create_sequence('res.partner.' + plant_initials)
                    plant_code_sequence = self.env['ir.sequence'].next_by_code('res.partner.' + plant_initials)
                    plant_code_sequence = '00' + str(plant_code_sequence)
                    plant_code_sequence = plant_code_sequence[len(plant_code_sequence)-5:]
                    vals['plant_code'] = plant_initials + plant_code_sequence[0:3] + '-' + plant_code_sequence[3:]
            else:
                vals['plant_code'] = False   
        partners = super(Partner, self).create(vals_list)
        return partners
    
    def first_letters(self, partner, partner_name):
        alphanumeric = ""
        for character in partner_name:
            if character.isalnum():
                alphanumeric += character.upper()
        if partner.get('country_id'):
            alphanumeric += self.env['res.country'].browse(partner.get('country_id')).name[:3].upper()
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
            self.env['ir.sequence'].sudo().create(new_vals)

    def _compute_plant_code_action(self):
        for partner in self:
            if partner.display_name:
                plant_initials = self.first_letters(partner, partner.display_name)
                self.create_sequence('res.partner.' + plant_initials)
                plant_code_sequence = self.env['ir.sequence'].next_by_code('res.partner.' + plant_initials)
                plant_code_sequence = '00' + str(plant_code_sequence)
                plant_code_sequence = plant_code_sequence[len(plant_code_sequence)-5:]
                partner.plant_code = plant_initials + plant_code_sequence[0:3] + '-' + plant_code_sequence[3:]
            else:
                partner.plant_code = False

    def action_set_plant_code(self):
        self.search([('is_company', '=', True), ('plant_code', '=', False),
                    ('customer_rank', '=', 1)])._compute_plant_code_action()

# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class Partner(models.Model):
    _inherit = 'res.partner'

    plant_code = fields.Char(string='Plant Code', store=True, copy=False)

    @api.constrains('plant_code')
    def _constrain_plant_code(self):
        for partner in self:
            if len(self.search([('plant_code', '=', partner.plant_code)])) > 1:
                raise UserError('A contact already exists with this plant code')

    def create_plant_code(self):
        for partner in self.filtered(lambda p: not p.plant_code and p.is_company and p.customer_rank == 1 and p.name):
            plant_initials = ''.join([ch.upper() for ch in self.name if ch.isalnum()][:3])
            partner.plant_code = self.env['ir.sequence'].get_next_plant_code(plant_initials)

    def action_set_plant_code(self):
        self.search([('is_company', '=', True), ('plant_code', '=', False),
                    ('customer_rank', '>=', 1)]).create_plant_code()

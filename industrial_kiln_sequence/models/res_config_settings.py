# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _get_next_barcode(self):
        return self.env['ir.sequence'].search([('code', '=', 'sale.order.job.number')]).number_next_actual

    job_number_start_number = fields.Integer(string='Range from', config_parameter='sale.job_number_start_number')
    next_job_number = fields.Char(string='Next Job Number sequence', default=_get_next_barcode)
    prefix_job_number_set = fields.Char(string='Prefix Options', config_parameter='sale.prefix_job_number_set', help='Options separated by comma')
    suffix_job_number_set = fields.Char(string='Suffix Options', config_parameter='sale.suffix_job_number_set', help='Options separated by comma')
    job_number_activate = fields.Boolean("Job number activation", config_parameter='sale.job_number_activate')
            
    def set_values(self):
        super(ResConfigSettings, self).set_values()  
        if self.job_number_activate:
            self.create_sequence() 
            self.env['ir.config_parameter'].sudo().set_param("sale.job_number_activate", self.job_number_activate) 
            if self.prefix_job_number_set: 
                self.prefix_job_number_set.replace(" ", "")     
                self.env['ir.config_parameter'].sudo().set_param("sale.prefix_job_number_set", self.prefix_job_number_set)
            if self.suffix_job_number_set:  
                self.suffix_job_number_set.replace(" ", "")     
                self.env['ir.config_parameter'].sudo().set_param("sale.suffix_job_number_set", self.suffix_job_number_set)
            else:
                raise ValidationError(_('Empty prefix or suffix options for job number.'))

    def create_sequence(self):
        if self.job_number_start_number:  
            current_sequence = self.env['ir.sequence'].search([('code', '=', 'sale.order.job.number')])
            new_vals = {
                            'name': 'Job number Industrial Kiln',
                            'code': 'sale.order.job.number',
                            'implementation': 'standard',
                            'prefix': '',
                            'suffix': '',
                            'number_next_actual': self.job_number_start_number,
                            'padding': 5,
                            'number_increment': 1
                    }
            if current_sequence:                   
                current_sequence.write(new_vals)   
            else:         
                self.env['ir.sequence'].create(new_vals)         

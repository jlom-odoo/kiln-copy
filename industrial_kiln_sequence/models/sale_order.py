#-*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    job_number = fields.Char('Job Number', store=True)
    sequence_job_number = fields.Char(string='Sequence Job number')
    prefix_job_number = fields.Selection(string='Prefix Job Number', selection="get_prefix_set")
    suffix_job_number = fields.Selection(string='Suffix Job number', selection="get_suffix_set")
    has_job_number = fields.Boolean('job number set al least once for this record', default=False,store=True)
    plant_code = fields.Char(string='Plant Code', related='partner_id.plant_code')
    plant_code_sequence = fields.Char(string='Plant code sequence')
    has_passed_set_method = fields.Boolean('has been saved', default=False, store=True)
    _sql_constraints = [
        ('date_order_conditional_required', "CHECK( (state IN ('sale', 'done') AND date_order IS NOT NULL) OR state NOT IN ('sale', 'done') )", "A confirmed sales order requires a confirmation date."),
        # ('job_number_required', "CHECK( state IN ('sale', 'done') AND (job_number IS NULL OR job_number IS FALSE) )", "A confirmed sales order requires a job number."),
    ]

    # @api.depends('state')
    def set_next_job_number_sequence(self):
        for order in self:
            if self.env['ir.config_parameter'].sudo().get_param("sale.job_number_activate"):
                print('QQQQQQQue xuxa pasa aca')
                # if order in self.filtered(lambda rec: rec.state in ['sale']):  
                next_job_number=self.env['ir.sequence'].search([('code', '=', 'sale.order.job.number')]).number_next_actual     
                if next_job_number:
                    print('QQQQQQ set de sequence_job_number')  
                    order.sequence_job_number=next_job_number
                    self.set_job_number()
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
                prefix_array.append((x.lower(), x.upper()))
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
                suffix_array.append((x.lower(), x.upper()))
            return suffix_array
        else:
            return [('select', 'Select')]

    @api.onchange('prefix_job_number', 'suffix_job_number')
    def set_job_number(self):  
        # add rec.state in ['sale'] condition if they disregard of a reserved unique number
        print('SSSSSSSSSSSet job NUmber')
        for order in self:
            if order in self.filtered(lambda rec: rec.prefix_job_number and rec.prefix_job_number != '' and rec.sequence_job_number and rec.suffix_job_number and rec.prefix_job_number != ''):
                print('OOOOOOOOOrder state',order.state)
                print('OOOOOOOOOrder preix',order.prefix_job_number)
                print('OOOOOOOOOrder suffix',order.suffix_job_number)
                print('OOOOOOOOOrder invoice_status ',order.invoice_status)
                order.job_number = order.prefix_job_number + order.sequence_job_number + order.suffix_job_number
                # job number can change in a s.o but the sequence number will not increase
                if not order.has_job_number:
                    self.env['ir.sequence'].next_by_code('sale.order.job.number')
                    order.has_job_number = True
            else:
                order.job_number = False      
                order.has_job_number = False 

            # if order.sequence_job_number and not order.job_number:
            # #     self.action_confirm() 
            #     raise ValidationError(_('A job number must be set. Edit to select prefix and suffix'))

    @api.onchange('partner_id')
    def update_plant_code(self):
        for order in self.filtered(lambda rec: rec.plant_code):   
            order.plant_code_sequence = order.plant_code
        for order in self.filtered(lambda rec: not rec.plant_code): 
            order.plant_code_sequence = False

    # @api.onchange('sequence_job_number')
    # def validate_sequence_job_number(self):
    #     for order in self.filtered(lambda rec: not rec.prefix_job_number or rec.prefix_job_number == '' or not rec.suffix_job_number or rec.prefix_job_number == ''):
    #         print('IIIIIIIIIIIIIIIIII and here')
    #         raise ValidationError(_('A job number must be set. Edit to select prefix and suffix'))

    # def action_edit_when_quotation_passes_to_sales_order(self):
    #         view_form_id = self.env.ref('sale.view_order_form').id
    #         action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations")
    #         action.update({
    #             'views': [(view_form_id, 'form')],
    #             'view_mode': 'form',
    #             'context': {
    #                 'form_view_initial_mode': 'edit', 
    #             },
    #         })
    #         return action

    # def action_redirect_to_quotations(self):
    #     action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations_with_onboarding")
    #     action['domain'] = self._get_sale_utm_domain()
    #     action['context'] = {'create': False}
    #     return action   

    def action_confirm(self): 
        print('AAAAAAAAAAAAAction confirm should go here')
        for order in self:
            print('BBBBBefore action confirm order name', order.name)
        self.set_next_job_number_sequence()
        super(SaleOrder, self).action_confirm()  
        for order in self:
            print('AAAAAAAAAAAfter action confirm order name', order.name)
        # for order in self.filtered(lambda rec: not rec.job_number):
        #     print('EEEEEEEEEEEEElse order has passed set method')
        #     raise ValidationError(_('A job number must be set. Edit to select prefix and suffix'))

    @api.depends('state')
    def validation_error(self):
        for order in self.filtered(lambda rec: rec.state in [('sale')] and not rec.job_number ):
            raise ValidationError(_('A job number must be set. Edit to select prefix and suffix'))

    # @api.onchange('job_sequence_number')
    # def _check_job_number_in_sales_order(self):
    #     print("AAAAAAAAAAAAAqui esta la clave check number in sales order")
    #     if self.env['ir.config_parameter'].sudo().get_param("sale.job_number_activate"):
    #         for order in self:
    #             if order.state in [('sale')] and (not order.prefix_job_number or not order.suffix_job_number): 
    #                 raise ValidationError(_(
    #                     "A job number must be set. Edit to select prefix and suffix"
    #                 ))
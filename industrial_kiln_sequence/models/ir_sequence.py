# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    is_plant_code = fields.Boolean(string='Is Plant Code', default=False)

    @api.model
    def get_next_plant_code(self, plant_initials):
        '''
        Gets the next value for a plant code based off of the initials provided
        If a sequence does not already exist for these plant initials it will
        create a new sequence
        :param plant_initials: string with length 3
        :return: string in the format of XXX###-##, where X is a character and
        # is a number from 0-9. Note, the last 2 digits will never be 00. If the
        previous sequence ended with 99, the next sequence will end with 01.
        '''
        self.check_access_rights('read')
        sequence_code = 'Plant-Number-' + plant_initials
        company_id = self.env.company.id
        seq_id = self.search([
            ('is_plant_code', '=', True),
            ('code', '=', sequence_code),
            ('company_id', 'in', [company_id, False])
        ], order='company_id', limit=1)
        if not seq_id:
            seq_id = self.create({
                'is_plant_code': True,
                'name': sequence_code,
                'code': sequence_code,
                'implementation': 'standard',
                'prefix': plant_initials,
                'suffix': '',
                'number_next': 101,
                'padding': 5,
                'number_increment': 1,
            })

        next_sequence = seq_id.next_by_id()

        if next_sequence[-2:] == '00':
            next_sequence = seq_id.next_by_id()

        return next_sequence[:-2] + '-' + next_sequence[-2:]
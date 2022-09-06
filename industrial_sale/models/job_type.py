from odoo import fields, models


class JobType(models.Model):
    _name = 'job.type'
    _description = 'Job Type'

    name = fields.Char('Name')

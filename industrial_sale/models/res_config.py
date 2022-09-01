from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    overhead_margin = fields.Float(string='Overhead Margin', related='company_id.overhead_margin', readonly=False)

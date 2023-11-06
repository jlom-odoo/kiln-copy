from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    start_day_of_week = fields.Selection([('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')], 
                                         string="Start Day Of Week", config_parameter="idk_weekly_report.start_day_of_week", default='0', required=True,
                                         help="Defines the day of which grouping by week should start")

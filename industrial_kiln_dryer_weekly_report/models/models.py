from odoo import api, models

class BaseModel(models.BaseModel):
    _inherit = 'base'
    
    @api.model
    def _read_group_process_groupby(self, gb, query):
        result = super()._read_group_process_groupby(gb, query)     
        if result.get('granularity') == 'week':
            start_day_of_week = self.env['ir.config_parameter'].sudo().get_param('idk_weekly_report.start_day_of_week')
            qualified_field = result['qualified_field'].replace("date_trunc('%s', " % ('week'), '').replace('::timestamp)', '')
            result['qualified_field'] = "date_trunc('week', {0}::timestamp - interval '{1} day') + interval '{1} day'".format(qualified_field, int(start_day_of_week))
        return result

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    freight_profit_margin = fields.Float(string='Freight Profit Margin')
  
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            freight_profit_margin=float(params.get_param('sale.freight_profit_margin', default=0.0))
            )
        return res
    
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('sale.freight_profit_margin', self.freight_profit_margin)

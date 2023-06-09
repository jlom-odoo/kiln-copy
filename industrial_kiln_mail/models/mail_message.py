from odoo import models, api


class Message(models.Model):
    _inherit = 'mail.message'

    @api.model
    def _read_group_raw(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        return super(Message, self.sudo())._read_group_raw(domain, fields, groupby, offset=offset,
            limit=limit, orderby=orderby, lazy=lazy,
        )

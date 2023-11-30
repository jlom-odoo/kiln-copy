from odoo import fields, models


class ServerActions(models.Model):
    _inherit = 'ir.actions.server'

    sale_order_field_ids = fields.Many2many(comodel_name='ir.model.fields', string='Fields to add to the email')

    def _run_action_next_activity(self, eval_context=None):
        if not self.activity_type_id or not self._context.get('active_id') or self._is_recompute():
            return False

        records = self.env[self.model_name].browse(self._context.get('active_ids', self._context.get('active_id')))

        vals = {
            'summary': self.activity_summary or '',
            'note': self.activity_note or '',
            'activity_type_id': self.activity_type_id.id,
            # Start Patch
            'sale_order_field_ids': self.sale_order_field_ids.ids or False,
            # End Patch
        }
        if self.activity_date_deadline_range > 0:
            vals['date_deadline'] = fields.Date.context_today(self) + relativedelta(**{
                self.activity_date_deadline_range_type: self.activity_date_deadline_range})
        for record in records:
            user = False
            if self.activity_user_type == 'specific':
                user = self.activity_user_id
            elif self.activity_user_type == 'generic' and self.activity_user_field_name in record:
                user = record[self.activity_user_field_name]
            if user:
                vals['user_id'] = user.id
            record.activity_schedule(**vals)
        return False

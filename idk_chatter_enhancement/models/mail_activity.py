from odoo import fields, models, api

class MailActivity(models.Model):
    _inherit = "mail.activity"

    # idk_contact populates only with contacts who are associated with the current company
    idk_contact = fields.Many2one(string="Contact", comodel_name="res.partner", help="Who was spoken to", domain="[('parent_id', '=', res_id)]")
    company_type = fields.Char(string="Company Type", compute="_compute_company_type")

    @api.depends("res_model_id", "res_id")
    def _compute_company_type(self):
        for activity in self:
            if activity.res_model_id.model == "res.partner":
                # If the model is res.partner, assign the company_type to either person or company
                activity.company_type = self.env["res.partner"].browse(activity.res_id).company_type
            else:
                # Otherwise the model the chatter is attached to is not res.partner, do not set a company_type
                activity.company_type = None

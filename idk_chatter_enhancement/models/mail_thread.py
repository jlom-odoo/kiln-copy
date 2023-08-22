from odoo import fields, models

class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def message_post_with_view(self, views_or_xmlid, **kwargs):
        # OVERRIDE
        # Add `idk_contact` and `idk_company` to the context so the fields are set when the message is created
        activity = kwargs.get("values", {}).get("activity", False)
        idk_contact = activity.idk_contact.id if activity and activity.idk_contact else False
        idk_company = activity.idk_contact.parent_id.id if activity and activity.idk_contact and activity.idk_contact.parent_id else False
        return super(MailThread, self.with_context(idk_contact=idk_contact, idk_company=idk_company)).message_post_with_view(views_or_xmlid, **kwargs)

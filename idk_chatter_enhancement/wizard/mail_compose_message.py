from odoo import models

class MailComposer(models.TransientModel):
    _inherit = "mail.compose.message"

    def get_mail_values(self, res_ids):
        # OVERRIDE
        # Adds `idk_contact` and `idk_company` to the data used to construct the `mail.message` record
        results = super().get_mail_values(res_ids)
        if self.composition_mode != "comment": return

        for res_id in res_ids:
            results[res_id]["idk_contact"] = self.env.context.get("idk_contact", False)
            results[res_id]["idk_company"] = self.env.context.get("idk_company", False)
        return self._process_state(results)

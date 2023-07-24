from odoo.tests.common import TransactionCase, tagged

@tagged("idk", "post_install", "-at_install")
class TestContactUpdatesOnMessage(TransactionCase):
    def setUp(self):
        super(TestContactUpdatesOnMessage, self).setUp()
        self.idk_contact = self.env["res.partner"].create({"name": "A Partner"})
        self.activity_type = self.env["mail.activity.type"].create({
            "name": "Activitizing",
            "category": "default",
            "res_model": "res.partner"
        })
        self.activity_id = self.env["mail.activity"].create({
            "summary": "The activity of all time",
            "activity_type_id": self.activity_type.id,
            "res_model_id": self.env["ir.model"]._get_id("res.partner"),
            "res_id": self.idk_contact.id,
            "idk_contact": self.idk_contact.id
        })
    
    def test_idk_contact_updates(self):
        self.assertEqual(self.idk_contact.name, "A Partner", "idk_contact.name is not set on the activity: {self.idk_contact}")
        message_id = self.activity_id.action_feedback() # Post message and unlink activity
        message = self.env["mail.message"].browse(message_id)
        self.assertEqual(message.idk_contact.name, "A Partner", f"idk_contact.name not set on message: {message}")
        self.assertEqual(self.idk_contact, message.idk_contact, "idk_contact specified on the activity: {self.idk_contact} is not the same record as the one on the message: {message.idk_contact}")

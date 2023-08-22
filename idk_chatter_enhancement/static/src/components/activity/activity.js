/** @odoo-module **/

import { Activity } from "@mail/components/activity/activity";

import { patch } from "web.utils";

patch(Activity.prototype, "idk_chatter_enhancement/static/src/components/activity/activity.js", {
    _onClickIdkContact(ev) {
         // Opens the profile of the contact when they are clicked
        this.messaging.openProfile({
            id: this.activity.idk_contact.id,
            model: "res.partner"
        })
    }
});

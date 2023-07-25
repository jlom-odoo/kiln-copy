/** @odoo-module **/

import {
    registerClassPatchModel,
    registerFieldPatchModel
} from "@mail/model/model_core";
import { attr } from "@mail/model/model_field";

registerFieldPatchModel("mail.activity", "idk_chatter_enhancement/static/src/models/activity/activity.js", {
    // Makes the front-end activity model aware of the `idk_contact` field
    idk_contact: attr({ default: false }),
});

registerClassPatchModel("mail.activity", "idk_chatter_enhancement/static/src/models/activity/activity.js", {
    convertData(data) {
        /** 
         * @override
         * Adds `idk_contact` to the data output by `convertData` so it is accessible from 
         * the front end after rpc calls are made
         */
        const res = this._super(data);
        if ("idk_contact" in data) {
            res.idk_contact = {
                id: data.idk_contact[0],
                display_name: data.idk_contact[1]
            }
        }
        return res;
    },
});

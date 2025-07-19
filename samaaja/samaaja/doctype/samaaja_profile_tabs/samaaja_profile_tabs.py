# Copyright (c) 2023, Impactyaan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SamaajaProfileTabs(Document):
    def before_save(self):
        default_tabs_hidden = frappe.db.get_single_value(
            "Samaaja Settings", "hide_default_tabs"
        )
        if not self.active and default_tabs_hidden:
            all_tabs = frappe.get_all(
                "Samaaja Profile Tabs", filters={"disable": 0, "active": 0}
            )
            if len(all_tabs) > 0:
                self.active = 1
                frappe.msgprint("Atleast one active tabs needs to be present, marking this tab as an active tab.")

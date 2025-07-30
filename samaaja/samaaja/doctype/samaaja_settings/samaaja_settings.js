// Copyright (c) 2023, Impactyaan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Samaaja Settings', {
	refresh: function (frm) {
        frm.add_custom_button(__('Setup Samaaja'), function () {
            frappe.call({
                method: "samaaja.setup.samaaja_setup.setup_samaaja",
                callback: function (r) {
                    if (r.message === "ok") {
                        frappe.msgprint("Samaaja setup completed successfully!");
                    }
                }
            });
        });
    }
});

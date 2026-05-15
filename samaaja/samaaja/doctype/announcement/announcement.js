frappe.ui.form.on('Announcement', {
	onload: function(frm) {
		// Automatically add "App Notification" as default if it's a new record and table is empty
		if (frm.is_new() && (!frm.doc.delivery_channels || frm.doc.delivery_channels.length === 0)) {
			frm.add_child('delivery_channels', {
				channel_name: 'App Notification',
				enabled: 1
			});
			frm.refresh_field('delivery_channels');
		}
	}
});

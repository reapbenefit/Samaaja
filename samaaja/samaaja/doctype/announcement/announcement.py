import frappe
from frappe.model.document import Document

class Announcement(Document):
	def before_insert(self):
		# Fallback for API-created records: ensure at least one default channel exists if none provided
		if not self.delivery_channels:
			self.append("delivery_channels", {
				"channel_name": "App Notification",
				"enabled": 1
			})

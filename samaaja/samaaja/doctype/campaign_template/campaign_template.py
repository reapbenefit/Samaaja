# Copyright (c) 2025, Impactyaan and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe import _

class CampaignTemplate(WebsiteGenerator):
	def validate(self):
		self.set_route()
		self.validate_recipients()
		self.make_all_files_public()
		if self.send_thank_you_email:
			self._upsert_thank_you_notification()

	def get_route(self):
		frappe.logger().info(f"Called get_route for {self.name}")

		return f"/campaign/{self.route}"

	def validate_recipients(self):
		if not self.get("recipients", {"is_selected_by_default": 1}):
			frappe.throw(
				_("At least one recipient must be selected by default for the campaign template.")
			)

	def make_all_files_public(self):
		# Make header_logo public
		make_file_public_and_update_field(self, "header_logo")

		# Make all partner logos public (if child table is named partners)
		if self.partners:
			for partner in self.partners:
				make_file_public_and_update_field(partner, "logo")
	
	def _upsert_thank_you_notification(self):
		filters = {
			"document_type": "Campaign Petition",
			"channel": "Email",
			"name": self.name
		}

		if frappe.db.exists("Notification", filters):
			notification = frappe.get_doc("Notification", filters)
		else:
			notification = frappe.new_doc("Notification")

		notification.update({
			"document_type":    "Campaign Petition",
			"channel":          "Email",
			"name":             self.name,
			"event":            "New",
			"message_type":     "HTML",
			"enabled":          self.published,
			"recipients":       [{"receiver_by_document_field": "email"}],
			"subject":          self.thank_you_email_subject,
			"message":          self.thank_you_email_body,
			"condition":        f"doc.campaign == '{self.name}'",
		})

		notification.save(ignore_permissions=True)

def make_file_public_and_update_field(doc, fieldname):
    file_url = getattr(doc, fieldname)
    if file_url and file_url.startswith("/private/"):
        file_doc = frappe.get_all("File", filters={"file_url": file_url}, fields=["name", "is_private", "file_url"])
        if file_doc:
            file = frappe.get_doc("File", file_doc[0].name)
            if file.is_private:
                file.is_private = 0
                file.save(ignore_permissions=True)
                # After save, file.file_url will be updated to /files/...
                # So update the doc field too
                setattr(doc, fieldname, file.file_url)


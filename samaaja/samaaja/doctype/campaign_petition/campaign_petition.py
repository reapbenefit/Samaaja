# Copyright (c) 2025, FOSS United and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CampaignPetition(Document):
	def validate(self):
		campaign = frappe.get_doc("Campaign Template", self.campaign)
		if not campaign.published:
			frappe.throw("Campaign Template must be published before creating a petition.")

	def after_insert(self):
		# send the email as soon as the doc is created
		self.send_to_recipients()

	def send_to_recipients(self):
		# collect all recipient emails from the child table
		recipients = [r.email for r in self.recipients]
		if not recipients:
			return

		full_message = self.message_body

		frappe.sendmail(
			recipients=recipients,
			subject=self.subject,
			message=full_message,
			sender=f"{self.first_name} {self.last_name}<{self.email}>",
			reference_doctype=self.doctype,
			reference_name=self.name,
		)
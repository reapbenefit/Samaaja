# Copyright (c) 2025, FOSS United and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class UserMetadata(Document):
	def validate(self):
		self.set_full_name()

	def set_full_name(self):
		if self.user:
			self.full_name = frappe.get_value("User", self.user, "full_name")

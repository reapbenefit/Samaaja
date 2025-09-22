# Copyright (c) 2025, FOSS United and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Microskill(Document):
	def validate(self):
		if self.level and self.badge:
			exists = frappe.db.exists(
				"Microskill",
				{
					"level": self.level,
					"badge": self.badge,
					"name": ["!=", self.name]
				}
			)
			if exists:
				frappe.throw(f"A Microskill with Level {self.level} and Badge {self.badge} already exists.")

def after_doctype_update():
	"""Ensure composite unique key on (level, badge)."""
	# Create/replace index on DB level
	frappe.db.add_index("Microskill", ["level", "badge"], index_name="unique_level_badge", unique=True)

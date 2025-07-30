import frappe
from frappe import _

sitemap = 1
no_cache = 1

def get_context(context):
	route = frappe.form_dict.route
	campaign = frappe.db.exists("Campaign Template", {"route": f"campaign/{route}", "accept_petitions": 1})
	if not campaign:
		frappe.redirect_to_message(
			_("Invalid Campaign"),
			_("Campaign not found for the given route or not accepting petitions."),
			http_status_code=404,
			indicator_color="red",
		)
		raise frappe.Redirect
	
	campaign = frappe.get_doc("Campaign Template", campaign)
	context.campaign = campaign
	context.recipients = campaign.recipients or []
	context.updates = campaign.updates or []
	context.partners = campaign.partners or []
	return context

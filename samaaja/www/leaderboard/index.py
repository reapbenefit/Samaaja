import frappe
from frappe.utils import cint
from samaaja.api.user import get_change_makers
from samaaja.api.leaderboard import  get_active_cm_count, get_total_invested_hours, get_city_wise_action_count_user_based, get_campaigns


sitemap = 1
no_cache = 1

def get_context(context):
	context.orgs = frappe.get_all("User Organization", pluck="name")
	context.cities = frappe.get_all("Samaaja Cities", pluck="name", order_by="name")
	context.total_actions = frappe.db.count("Events")
	context.total_invested_hours = cint(get_total_invested_hours())
	context.active_cm_count = get_active_cm_count()
	context.verified_users = get_change_makers(verified=True, page_length=10, start=0)
	context.campaigns = get_campaigns(page_length=10, start=0)
	context.city_wise_data = get_city_wise_action_count_user_based(page_length=10)
	context.samaaja_settings = frappe.get_doc("Samaaja Settings")
import frappe
from frappe.utils import cint
from samaaja.api.leaderboard import  get_total_invested_hours, get_campaigns,get_opportunities
from samaaja.api.user import get_active_cm_count

sitemap = 1
no_cache = 1

def get_context(context):
	context.cities = frappe.get_all("District", pluck="district_name", order_by="district_name")
	context.total_actions = frappe.db.count("Events")
	context.total_invested_hours = cint(get_total_invested_hours())
	context.active_cm_count = get_active_cm_count()
	context.campaigns = get_campaigns(page_length=10, start=0)
	context.opportunities = get_opportunities(page_length=10, start=0)
	context.samaaja_settings = frappe.get_doc("Samaaja Settings")
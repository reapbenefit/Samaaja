import frappe

from samaaja.api.leaderboard import get_active_cm_count, get_total_invested_hours
from samaaja.utils import human_format


sitemap = 1
no_cache = 1

def get_context(context):
	context.total_invested_hours = human_format(12)
	context.active_cm_count = human_format(get_active_cm_count())
	context.users = []
import frappe
import json
from frappe.utils import cint, flt, now_datetime
from frappe import qb
from frappe.query_builder import DocType, Order
from frappe.query_builder.functions import Coalesce, Sum, Count, Lower
from datetime import timedelta



states_of_india = [
	"Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
	"Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
	"Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
	"Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
	"Uttar Pradesh", "Uttarakhand", "West Bengal", ""
]

def get_active_ninja_count():
	return frappe.db.count("User", {"enabled": 1})

def get_action_count():
	return frappe.db.count("Events")

def get_total_invested_hours():
	Events = frappe.qb.DocType("Events")
	query = (
		frappe.qb.from_(Events)
		.select(
			Sum(Events.hours_invested).as_("hours_invested"),
		)
	)
	result = query.run(as_dict=True)
	if not result:
		return 0

	return result[0]["hours_invested"]

@frappe.whitelist(allow_guest=True)
def get_city_wise_action_count(page_length=10):
	Events = frappe.qb.DocType("Events")
	Location = frappe.qb.DocType("Location")

	query = (
		frappe.qb.from_(Events)
		.join(Location)
		.on(Events.location == Location.name)
		.select(
			Count(Events.name).as_("action_count"),
			Location.city.as_("city")
		)
		.where(
			(Location.city.isnotnull()) & (Location.city.notin(["NULL"]))
		)
		.groupby(
			Location.city
		).orderby(
			Count(Events.name), order=frappe.qb.desc
		).limit(page_length)
	)

	# Run the query with debug enabled
	result = query.run(as_dict=True)
	all_actions = get_action_count()

	total_actions = [row.action_count for row in result]
	total_actions = sum(total_actions)
	for row in result:
		row.percentage = frappe.utils.cint((row.action_count/total_actions) * 100)

	return result

@frappe.whitelist(allow_guest=True)
def get_city_wise_action_count_user_based(page_length=10, recent_rank_based_on=None):
	Events = frappe.qb.DocType("Events")
	UserMetadata = frappe.qb.DocType("User Metadata")

	# Base Query
	user_with_events = (
		frappe.qb.from_(UserMetadata)
		.join(Events).on(Events.user == UserMetadata.name)  # Ensure 'user' field in Events points to User's 'name'
		.select(UserMetadata.name)
		.where(
			(UserMetadata.city.isnotnull()) &  # Ensure city is not null
			(UserMetadata.city.notin(states_of_india)) &  # Exclude cities in the list
			(Events.name.isnotnull())  # Ensure events exist for the user
		)
	)

	# Apply filters if present
	if recent_rank_based_on:
		if recent_rank_based_on == "Last 15 Days":
			user_with_events = user_with_events.where(Events.creation >= frappe.utils.add_days(frappe.utils.nowdate(), -15))
		elif recent_rank_based_on == "Last Month":
			user_with_events = user_with_events.where(Events.creation >= frappe.utils.add_days(frappe.utils.nowdate(), -30))

	# Execute Query
	user_with_events = user_with_events.run(as_dict=True)
	users = list(set([user.name for user in user_with_events]))
	result = []
	if users:
		# Query to get the number of users grouped by city, with conditions on a list of usernames
		user_count_by_city = (
			qb.from_(UserMetadata)
			.select(UserMetadata.city, Count(UserMetadata.name).as_("action_count"))  # count users per city
			.where(
				UserMetadata.name.isin(users)  # filter by a list of usernames
			)
			.groupby(UserMetadata.city)  # group by user city
			.orderby(
				Count(UserMetadata.name), order=frappe.qb.desc  # Order cities alphabetically
			)
			.limit(page_length)  # limit to 10 results
		)

		# Execute the query and fetch the results
		result = user_count_by_city.run(as_dict=True)

		total_actions = [row.action_count for row in result]
		total_actions = sum(total_actions)
		for row in result:
			row.percentage = frappe.utils.cint((row.action_count/total_actions) * 100)

	return result

@frappe.whitelist(allow_guest=True)
def get_state_wise_user_count(page_length=10):
	# Events = frappe.qb.DocType("Events")
	# Location = frappe.qb.DocType("Location")

	result = frappe.db.get_all('User',
		filters={
			'enabled': 1,
			'state': ('is', 'set')
		},
		fields=['count(name) as user_count', 'state'],
		group_by='state',
		order_by='count(name) desc',
		page_length=page_length
	)
	# query = (
	# 	frappe.qb.from_(Events)
	# 	.join(Location)
	# 	.on(Events.location == Location.name)
	# 	.select(
	# 		Count(Events.name).as_("action_count"),
	# 		Location.city.as_("city")
	# 	)
	# 	.where(
	# 		Location.city.isnotnull()
	# 	)
	# 	.groupby(
	# 		Location.city
	# 	).orderby(
	# 		Count(Events.name), order=frappe.qb.desc
	# 	).limit(page_length)
	# )

	# Run the query with debug enabled
	# result = query.run(as_dict=True)
	# all_actions = get_action_count()

	total_users = [row.user_count for row in result]
	total_users = sum(total_users)
	for row in result:
		row.percentage = frappe.utils.cint((row.user_count/total_users) * 100)

	return result

def update_user_rank():
    """
    Fetch all Ninja Profile records with hours_invested > 0.0,
    ordered by hours_invested descending, and update each record's rank.
    """
    profiles = frappe.get_all(
        "Ninja Profile",
        fields=["name", "hours_invested"],
        filters={"hours_invested": [">", 0.0]},
        order_by="hours_invested desc"
    )

    for rank, p in enumerate(profiles, start=1):
        frappe.db.set_value(
            "Ninja Profile",
            p.name,
            "rank",
            rank,
            update_modified=False
        )

@frappe.whitelist(allow_guest=True)
def search_users_(filters=None, raw=False, page_length=10, start=0):
	start = cint(start)
	page_length = cint(page_length)
	
	filters = json.loads(filters) if filters else {}

	# if filters.get("hr_range") or filters.get("city") or filters.get("organization") or filters.get("ninja"):
	# 	raw = True
	# 	start = 0

	# Define Doctypes
	User = DocType("User")
	Events = DocType("Events")
	NinjaProfile = DocType("Ninja Profile")

	# Check if recent rank filtering is needed
	recent_rank_based_on = filters.get("recent_rank_based_on")

	# Define Query Time Range (If Needed)
	time_condition = None
	if recent_rank_based_on == "Last 15 Days":
		time_condition = now_datetime() - timedelta(days=15)
	elif recent_rank_based_on == "Last Month":
		time_condition = now_datetime() - timedelta(days=30)

	# Base Query: Always Fetch Rank from `Ninja Profile`
	user_count = frappe.db.count("User", {"enabled": 1})
	query = (
		frappe.qb.from_(User)
		.join(NinjaProfile).on(User.name == NinjaProfile.name)
		.select(
			User.name,
			User.username,
			User.city,
			Coalesce(NinjaProfile.rank, user_count).as_("rank"),  # Always get rank from Ninja Profile
			User.org_id,
			User.user_image,
			User.location,
			User.full_name,
		)
	)

	# If `recent_rank_based_on` is set, use Events table for contribution data
	if recent_rank_based_on:
		query = (
			query.join(Events).on(User.name == Events.user)
			.select(
				Coalesce(Sum(Events.hours_invested), 0).as_("hours_invested"),
				Coalesce(Count(Events.user), 0).as_("contribution_count"),
				Sum(Events.hours_invested).as_("recent_rank")  # ✅ FIXED: Use rank() as a window function
			)
			.groupby(
				User.name, User.username, User.city, User.org_id, User.user_image, 
				User.location, User.full_name, NinjaProfile.rank
			)
			.orderby(Sum(Events.hours_invested), order=Order.desc)
			.orderby(User.full_name, order=Order.asc)
		)
		
		if time_condition:
			query = query.where(Events.creation >= frappe.utils.format_datetime(time_condition, "yyyy-MM-dd HH:mm:ss"))
		
		# Apply `hr_range` Filter in Python (If Needed)
		if filters.get("hr_range"):
			if "-" in filters.get("hr_range"):
				min_hr, max_hr = map(flt, filters.get("hr_range").split("-"))
				query = query.having(Coalesce(Sum(Events.hours_invested), 0).between(min_hr, max_hr))
			
			elif "+" in filters.get("hr_range"):
				min_hr = flt(filters.get("hr_range").replace("+", ""))
				query = query.having(Coalesce(Sum(Events.hours_invested), 0) > min_hr)

	else:
		# When `recent_rank_based_on` is not set, use Ninja Profile
		query = (
			query.select(
				Coalesce(NinjaProfile.hours_invested, 0).as_("hours_invested"),
				Coalesce(NinjaProfile.contributions, 0).as_("contribution_count"),
			)
			.orderby(Coalesce(NinjaProfile.rank, 99999).as_("rank"), order=Order.asc)
			.orderby(User.full_name, order=Order.asc)
		)
		# Apply `hr_range` Filter in Python (If Needed)
		if filters.get("hr_range"):
			if "-" in filters.get("hr_range"):
				min_hr, max_hr = map(flt, filters.get("hr_range").split("-"))
				query = query.where(NinjaProfile.hours_invested.between(min_hr, max_hr))
			
			elif "+" in filters.get("hr_range"):
				min_hr = flt(filters.get("hr_range").replace("+", ""))
				query = query.where(NinjaProfile.hours_invested > min_hr)

	query = query.where(User.enabled == 1)
	query = query.where(NinjaProfile.rank != 0)
	
	# Apply Filters Dynamically
	if filters.get("organization"):
		query = query.where(User.org_id == filters["organization"])
	
	if filters.get("city"):
		query = query.where(User.city == filters["city"])

	if filters.get("ninja"):
		full_name_filter = f"%{filters['ninja'].lower()}%"
		query = query.where(Lower(User.full_name).like(full_name_filter))
	# Apply Pagination
	if not raw:
		query = query.limit(page_length).offset(start)

	# Execute Query
	users = query.run(as_dict=True)

	# Assign Serial Numbers (Pagination)
	if recent_rank_based_on:
		for count, data in enumerate(users, start + 1):
			data["recent_rank"] = count

	# Apply `hr_range` Filter in Python (If Needed)
	# if filters.get("hr_range"):
	# 	users = filter_by_hour_range(users, filters["hr_range"])

	# Apply Additional Text-Based Filters in Python
	# users = filter_users(users, filters)
	# frappe.errprint(users)
	return users


### **🔹 Filter Users by `hr_range`**
def filter_by_hour_range(users, hr_range):
	filtered_users = []
	
	if "-" in hr_range:
		min_hr, max_hr = map(flt, hr_range.split("-"))
		filtered_users = [user for user in users if min_hr < flt(user["hours_invested"]) <= max_hr]
	
	elif "+" in hr_range:
		min_hr = flt(hr_range.replace("+", ""))
		filtered_users = [user for user in users if flt(user["hours_invested"]) > min_hr]

	return filtered_users


### **🔹 Apply Filters on Users**
def filter_users(users, filters):
	filtered_users = []
	
	for user in users:
		add_user = True

		if filters.get("ninja") and filters["ninja"].lower() not in user["full_name"].lower():
			add_user = False

		if filters.get("organization") and user["org_id"] != filters["organization"]:
			add_user = False

		if filters.get("city") and user["city"] != filters["city"]:
			add_user = False

		if add_user:
			filtered_users.append(user)

	return filtered_users

def get_campaigns(page_length=10, start=0):
	start = cint(start)
	page_length = cint(page_length)

	CampaignTemplate = DocType("Campaign Template")
	User = DocType("User")
	CampaignPetition = DocType("Campaign Petition")
	
	query = (
		frappe.qb.from_(User)
		.join(CampaignTemplate)
		.on(CampaignTemplate.owner == User.name)
		.left_join(CampaignPetition)
		.on(CampaignPetition.campaign == CampaignTemplate.name)
		.select(
			User.full_name,
			CampaignTemplate.title,
			CampaignTemplate.route,
			CampaignTemplate.published,
			CampaignTemplate.accept_petitions,
			CampaignTemplate.header_logo,
			Count(CampaignPetition.name).as_("petition_count"),
		)
		.where(CampaignTemplate.published == 1)
		.groupby(User.full_name, CampaignTemplate.name)
	)
	results = query.run(as_dict=True)
	return results

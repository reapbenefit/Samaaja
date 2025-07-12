import frappe
import json
from samaaja.api.common import custom_response
from frappe.query_builder.functions import Count, Sum


@frappe.whitelist()
def new():
	user_data = json.loads(frappe.request.data)
	try:
		mobile_no = user_data.get("mobile_no")
		email = user_data.get("email")
		if not mobile_no:
			frappe.throw("mobile_no field is mandatory")

		if not email:
			frappe.throw("email field is mandatory")

		existing = frappe.db.exists(
			"User", {
				"mobile_no": mobile_no
			}
		)

		if existing:
			frappe.throw("User already exists with mobile no")

		existing = frappe.db.exists(
			"User", {
				"name": email
			}
		)

		if existing:
			frappe.throw("User already exists with email")

		user = frappe.get_doc(
			{
				"doctype": "User",
				**user_data,
			}
		)
		user.insert(ignore_permissions=True)
		user = user.as_dict()
		return user
	except Exception as e:
		frappe.db.rollback()
		return custom_response(str(e), None, 500, True)


@frappe.whitelist(allow_guest=True)
def submit_user_review(review):
	# frappe.errprint(action)
	review_update = json.loads(review)
	frappe.errprint(review)
	if not frappe.db.exists("User Review", review_update.get("review")):
		frappe.throw("Invalid Review.")
	
	review = frappe.get_doc("User Review", review_update.get("review"))
	review.update(review_update)
	review.flags.ignore_permissions = 1
	review.save()
	return review

@frappe.whitelist(allow_guest=True)
def get_ninjas(verified=False, page_length=None, start=0):
	Events = frappe.qb.DocType("Events")
	User = frappe.qb.DocType("User")

	query = (
		frappe.qb.from_(User)
		.select(
			User.full_name.as_("full_name"),
			User.name.as_("name"),
			#User.city.as_("city"),
			User.user_image.as_("user_image"),
			#User.verified_by.as_("verified_by"),
			User.username.as_("username"),
			#User.headline.as_("focus_area"),
		)
		.where(
			User.name.notin(["solveninja@reapbenefit.org", "gautamp@reapbenefit.org"])
		)
		.orderby(
			User.creation, order=frappe.qb.asc
		)
	)
	#if verified:
	#	query = query.where((User.verified_by.isnotnull()) & (User.verified_by != ''))
	
	if page_length:
		query = query.limit(page_length)
	
	if start:
		query = query.offset(start)
	# Run the query with debug enabled
	result = query.run(as_dict=True)
	
	for row in result:
		row.user_profile = frappe.utils.get_url(f"/user-profile/{row.username}")
	return result

def get_user_badges(user, badge_type=None):
	badges = frappe.get_all("Badge", filters=[["_user_tags", "like", f"%{badge_type}%"]], pluck="name")
	UserBadge = frappe.qb.DocType("User badge")
	Badge = frappe.qb.DocType("Badge")

	query = (
		frappe.qb.from_(Badge)
		.join(UserBadge)
		.on(UserBadge.badge == Badge.name)
		.select(
			Badge.title.as_("title")
		)
		.where(
			UserBadge.user == user
		)
		.where(
			Badge.name.isin(badges)
		)

	)
	
	result = query.run(as_dict=True)
	result = [d['title'] for d in result]

	return result

def user_interested_in(user):
	user_event_details_category = frappe.db.sql("""SELECT 
			e.category AS category, 
			COUNT(*) 
		FROM 
			`tabEvents` e 
		WHERE 
			e.user = %s 
			AND e.category IS NOT NULL 
		GROUP BY 
			e.category 
		ORDER BY 
			COUNT(*) DESC 
		LIMIT 3""", user,as_dict=True)

	return [d['category'] for d in user_event_details_category]

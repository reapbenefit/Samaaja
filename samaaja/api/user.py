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
def get_change_makers(verified='false', page_length=None, start=0):
	"""
	Get list of user names (for pagination/listing).
	Returns only user names, not full profile data.
	
	Args:
		verified: 'true' or 'false' to filter verified users
		page_length: Number of records per page
		start: Offset for pagination
		
	Returns:
		Dict with 'users' (list of user names) and 'total_count'
	"""
	UserReview = frappe.qb.DocType("User Review")
	User = frappe.qb.DocType("User")
	UserMetadata = frappe.qb.DocType("User Metadata")
	
	# Build base query for counting total records
	if verified == 'true':
		# For verified users, count distinct users with accepted reviews
		total_count = frappe.db.sql("""
			SELECT COUNT(DISTINCT ur.user) as count
			FROM `tabUser Review` ur
			INNER JOIN `tabUser` u ON ur.user = u.name
			INNER JOIN `tabUser Metadata` um ON um.user = u.name
			WHERE ur.status = 'Accepted'
			AND u.enabled = 1
			AND u.full_name != 'Administrator'
			AND u.full_name != 'Guest'
		""", as_dict=True)[0]['count']
	else:
		# For all users, count all users
		total_count = (
			frappe.qb.from_(User)
			.left_join(UserMetadata)
			.on(UserMetadata.user == User.name)
			.select(Count(User.name))
			.where(User.enabled == 1)
			.where(User.full_name != "Administrator")
			.where(User.full_name != "Guest")
			.run()[0][0]
		)

	# Build query for fetching user names only
	if verified == 'true':
		query = (
			frappe.qb.from_(UserReview)
			.join(User)
			.on(UserReview.user == User.name)
			.join(UserMetadata)
			.on(UserMetadata.user == User.name)
			.select(User.name)
			.where(UserReview.status == "Accepted")
			.where(User.enabled == 1)
			.where(User.full_name != "Administrator")
			.where(User.full_name != "Guest")
			.orderby(User.creation, order=frappe.qb.asc)
		)
	else:
		query = (
			frappe.qb.from_(User)
			.left_join(UserMetadata)
			.on(UserMetadata.user == User.name)
			.select(User.name)
			.where(User.enabled == 1)
			.where(User.full_name != "Administrator")
			.where(User.full_name != "Guest")
			.orderby(User.creation, order=frappe.qb.asc)
		)

	if page_length:
		query = query.limit(page_length)
	
	if start:
		query = query.offset(start)
	
	# Run the query - returns list of dicts with 'name' key
	result = query.run(as_dict=True)
	
	# Extract just the names
	user_names = [row['name'] for row in result]
	users = []
	for user_name in user_names:
		user = get_user_profile(user_name)
		users.append(user)

	return {
		"users": users,
		"total_count": total_count
	}


@frappe.whitelist(allow_guest=True)
def get_user_profile(user_name):
	"""
	Get complete user profile data for a given user name.
	Aggregates data from User, User Metadata, Location, District, etc.
	
	Args:
		user_name: User name
		
	Returns:
		Dict with complete user profile data
	"""
	if not user_name:
		frappe.throw("user_name is required")
	
	
	# Get User document
	if not frappe.db.exists("User", user_name):
		frappe.throw(f"User '{user_name}' not found")
	
	user = frappe.get_doc("User", user_name)
	
	# Get User Metadata (may not exist for all users)
	user_metadata = None
	if frappe.db.exists("User Metadata", user_name):
		user_metadata = frappe.get_doc("User Metadata", user_name)
	
	# Resolve display location safely (some users may not have a location yet)
	location = ""
	location_field_name = frappe.db.get_single_value("Samaaja Settings", "location_field_name") or "city"
	if user_metadata and user_metadata.location:
		# Use db lookups to avoid permission errors for Guest on public pages
		if location_field_name == "district":
			district = frappe.db.get_value("Location", user_metadata.location, "district")
			location = frappe.db.get_value("District", district, "district_name") if district else ""
			location = location or ""
		else:
			location = frappe.db.get_value("Location", user_metadata.location, location_field_name) or ""
	
	# Get verification status
	verified_by = None
	is_verified = False
	user_review = frappe.db.get_value(
		"User Review",
		{"user": user_name, "status": "Accepted"},
		"name"
	)
	if user_review:
		is_verified = True
		review_doc = frappe.get_doc("User Review", user_review)
		verified_by = review_doc.reviewer_name
	
	# Build profile data
	profile = {
		"name": user.name,
		"full_name": user.full_name or "",
		"first_name": user.first_name or "",
		"last_name": user.last_name or "",
		"email": user.email or "",
		"mobile_no": user.mobile_no or "",
		"gender": user.gender or "",
		"user_image": user.user_image,
		"focus_area": user.interest,
		"location": location,
		"is_verified": is_verified,
		"verified_by": verified_by,
		"user_profile": frappe.utils.get_url(f"/user-profile/{user.username}") if user.username else None,
		"contributions": (user_metadata.contributions or 0) if user_metadata else 0,
		"hours_invested": (user_metadata.hours_invested or 0) if user_metadata else 0,
	}
	
	return profile

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

@frappe.whitelist(allow_guest=True)
def get_genders():
	return frappe.get_all("Gender", fields=["gender"], order_by="gender asc")

def get_active_cm_count():
	User = frappe.qb.DocType("User")
	return (
		frappe.qb.from_(User)
		.select(Count(User.name))
		.where(User.enabled == 1)
		.where(User.full_name != "Administrator")
		.where(User.full_name != "Guest")
		.run()[0][0]
	)

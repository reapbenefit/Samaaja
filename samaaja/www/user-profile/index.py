import frappe
from frappe.utils import logger
from frappe.query_builder import DocType

sitemap = 1
no_cache = 1

logger.set_log_level("DEBUG")
logger = frappe.logger("api", allow_site=True, file_count=50)

def get_context(context):
	logger.info("🔄 user-profile started")
	context.no_cache = 1
	context.current_user = None

	username = frappe.form_dict.username or frappe.local.form_dict.get("username")

	try:
		if username == "me" or not username:
			context.current_user = frappe.get_doc("User", frappe.session.user)
		else:
			context.current_user = frappe.get_doc("User", {"username": username})
		
		# Disallow Administrator and Guest
		if context.current_user.name in ["Administrator", "Guest"]:
			raise frappe.DoesNotExistError("User not found or not allowed")

	except Exception as e:
		frappe.log_error(f"Failed to load profile for username={username}", e)
		raise frappe.DoesNotExistError("User not found or not allowed")

	if not context.current_user:
		context.template = "www/404.html"
		return context

	context.title = f"{context.current_user.full_name.title()} Profile"

	# Login check
	user = frappe.session.user
	context.current_user.is_logged_in = user == context.current_user.name
	context.current_user.is_system_manager = frappe.db.exists(
		"Has Role", {"parent": user, "role": "System Manager"}
	)

	UserReview = DocType("User Review")
	query = (
		frappe.qb.from_(UserReview)
		.select("*")
		.where(UserReview.user == context.current_user.name)
		.limit(1)
	)
	result = query.run(as_dict=True)
	user_profile_review = result[0] if result else None

	if user_profile_review:
		context.current_user_is_profile_verified = True
	context.user_metadata = frappe.get_doc("User Metadata", context.current_user.name) if frappe.db.exists("User Metadata", context.current_user.name) else None

	# All actions
	context.current_user.actions = frappe.db.sql("""
		SELECT e.name AS event_id, e.title, e.type, e.category, e.description, e.location,
		       e.creation, e.highlight, e.verified_by, e.hours_invested,
		       l.district AS location_name
		FROM `tabEvents` e
		LEFT JOIN `tabLocation` l ON l.name = e.location
		WHERE e.user = %s
		ORDER BY e.creation DESC
	""", context.current_user.name, as_dict=True)

	# Process actions
	context.current_user.highlighted_action = {'title': '', 'description': ''}
	for action in context.current_user.actions:
		action.creation = frappe.utils.pretty_date(action.creation)
		action.review_exists = frappe.db.exists("Events Review", {"events": action.event_id, "status": "Accepted"})
		if action.review_exists:
			action.review = frappe.get_doc("Events Review", action.review_exists)
		logger.info(f'highlight status {action.highlight}')
		if action.highlight == 1:
			context.current_user.highlighted_action = {
				'title': action.title,
				'description': action.description
			}
	# Badges
	user_badges = frappe.db.get_all('User badge',
		filters={'user': context.current_user.name, 'active': 1},
		fields=['badge', 'badge_count']
	)

	context.current_user.skills = []
	context.current_user.partners = []

	for user_badge in user_badges:
		badge_doc = frappe.get_doc('Badge', user_badge.badge)
		tags = badge_doc.get_tags()

		if badge_doc.badge_type == "Skill":
			context.current_user.skills.append({
				"name": badge_doc.title,
				"image": badge_doc.icon,
				"badge_count": user_badge.badge_count
			})
		if 'Partners' in tags:
			context.current_user.partners.append({
				"name": badge_doc.title,
				"image": badge_doc.icon,
				"badge_count": user_badge.badge_count
			})

	# Reviews
	context.current_user.reviews = frappe.get_all(
		"User Review",
		filters={"user": context.current_user.name, "status": "Accepted"},
		fields=["review_title", "reviewer_name", "designation", "comment", "organisation"]
	)

	# Superheroes (top categories)
	superheroes = []
	if context.current_user.interest:
		interests = [i.strip() for i in context.current_user.interest.split(",")]

		for interest in interests:
			cat_doc = frappe.get_doc('Event Category', interest)
			if cat_doc:
				superheroes.append({
					'name': interest,
					'image': cat_doc.icon
				})
			else:
				superheroes.append({
						'name': interest,
					})

		context.current_user.superheroes = superheroes

	# return context

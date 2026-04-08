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

	user_profile_location_field = frappe.db.get_single_value("Samaaja Settings", "user_profile_location_field") or "city"
	
	if context.user_metadata and context.user_metadata.location:
		# Use db lookups to avoid permission errors for Guest on public pages
		if user_profile_location_field == "district":
			district = frappe.db.get_value("Location", context.user_metadata.location, "district")
			context.current_user.location = frappe.db.get_value("District", district, "district_name") if district else ""
		else:
			context.current_user.location = frappe.db.get_value(
				"Location",
				context.user_metadata.location,
				user_profile_location_field,
			)
		context.current_user.location = context.current_user.location or ""

	# All actions
	context.current_user.actions = frappe.db.sql("""
		SELECT e.name AS event_id, e.title, e.type, e.category, e.description, e.location,
		       e.creation, e.highlight, e.verified_by, e.hours_invested,
			   e.attachment1, e.attachment2,
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

	samaaja_settings = frappe.get_single("Samaaja Settings")
	
	context.current_user.verified_change_maker_label = samaaja_settings.verified_change_maker_label
	context.current_user.last_activity_label = samaaja_settings.last_activity_label
	context.current_user.hours_label = samaaja_settings.hours_label
	context.current_user.actions_label = samaaja_settings.actions_label
	context.current_user.bio_label = samaaja_settings.bio_label
	context.current_user.skill_badges_label = samaaja_settings.skill_badges_label
	context.current_user.overview_label = samaaja_settings.overview_label
	context.current_user.highlight_label = samaaja_settings.highlight_label
	context.current_user.interested_in_label = samaaja_settings.interested_in_label
	context.current_user.expert_review_label = samaaja_settings.expert_review_label
	context.current_user.action_label = samaaja_settings.action_label
	context.current_user.no_bio_text = samaaja_settings.no_bio_text
	context.current_user.location_absent_text = samaaja_settings.location_absent_text
	context.current_user.highlight_absent_text = samaaja_settings.highlight_absent_text
	context.current_user.verified_by_label = samaaja_settings.verified_by_label
	context.current_user.skill_badges_absent_text = samaaja_settings.skill_badges_absent_text
	context.current_user.action_absent_text = samaaja_settings.actions_absent_text
	context.current_user.profile_label = samaaja_settings.profile_label
	
	# Button labels
	context.current_user.add_action_label = samaaja_settings.add_action_label
	context.current_user.ask_for_help_label = samaaja_settings.ask_for_help_label
	context.current_user.request_review_label = samaaja_settings.request_review_label
	context.current_user.download_profile_label = samaaja_settings.download_profile_label
	context.current_user.highlight_label_menu = samaaja_settings.highlight_label_menu
	context.current_user.edit_label = samaaja_settings.edit_label
	context.current_user.delete_label = samaaja_settings.delete_label
	context.current_user.delete_confirm_text = samaaja_settings.delete_confirm_text
	
	# Review and partner labels
	context.current_user.no_reviews_text = samaaja_settings.no_reviews_text
	context.current_user.partners_supporters_label = samaaja_settings.partners_supporters_label
	context.current_user.no_partners_text = samaaja_settings.no_partners_text
	context.current_user.attachment_label = samaaja_settings.attachment_label
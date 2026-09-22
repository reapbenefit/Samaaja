import frappe


def check_app_permission():
	"""Show Samaaja on the desk apps screen for Desk users only."""
	if frappe.session.user == "Administrator":
		return True
	return frappe.db.get_value("User", frappe.session.user, "user_type") != "Website User"

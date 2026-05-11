import frappe
from samaaja.services.community_post import CommunityPostManager
from samaaja.utils.custom_response import custom_response
from samaaja.utils.result import Result

@frappe.whitelist(allow_guest=True)
def get():
    try:
        return CommunityPostManager.get().to_custom_response()
    except Exception as e:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to fetch community posts"
        )
        return custom_response(
            message="Failed to fetch community posts",
            status_code=500
            )
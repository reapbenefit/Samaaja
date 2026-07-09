import frappe
from samaaja.services.community_post import CommunityPostManager
from samaaja.services.action import ActionManager
from samaaja.utils.custom_response import custom_response


@frappe.whitelist(allow_guest=True)
def get_posts(user, limit=10, offset=0):
    try:
        return CommunityPostManager.get_posts(
            user=user,
            limit=limit,
            offset=offset
        ).to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to fetch user community posts"
        )

        return custom_response(
            message="Failed to fetch user community posts",
            status_code=500
        )

@frappe.whitelist(allow_guest=True)
def get_actions(user, limit=10, offset=0):
    try:
        return ActionManager.get_actions(
            user=user,
            limit=limit,
            offset=offset
        ).to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to fetch user actions"
        )

        return custom_response(
            message="Failed to fetch user actions",
            status_code=500
        ) 
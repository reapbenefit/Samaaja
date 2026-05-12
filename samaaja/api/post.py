from samaaja.services.community_post import CommunityPostManager
from samaaja.utils.custom_response import custom_response
import frappe

@frappe.whitelist()
def add():
    try:
        title = frappe.form_dict.get("title")
        description = frappe.form_dict.get("description")
        category = frappe.form_dict.get("category")
        media = frappe.request.files.get("attachments")

        return CommunityPostManager.create(
                                    title=title,
                                    description=description,
                                    media=media,
                                    user=frappe.session.user,
                                    action_doc=None,
                                    tag=category
                                ).to_custom_response()
    except Exception as e:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to create community post"
        )
        return custom_response("Failed to create community post", status_code=500)
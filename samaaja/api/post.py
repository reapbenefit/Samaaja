from samaaja.services.community_post import CommunityPostManager
from samaaja.utils.custom_response import custom_response
import frappe

@frappe.whitelist(methods=["POST"])
def like():
    try:
        post_id = frappe.form_dict.get("post_id")
        if not post_id:
            return custom_response("Post ID is required", status_code=400)
        return CommunityPostManager.like(
                                    post_id=post_id,
                                    user_id=frappe.session.user
                                ).to_custom_response()
    except Exception as e:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to like community post"
        )
        return custom_response("Failed to like community post", status_code=500)


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
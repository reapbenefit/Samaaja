# samaaja/api/comment.py

import frappe
from samaaja.services.comment import CommentManager
from samaaja.utils.custom_response import custom_response



@frappe.whitelist(methods=["POST"])
def create():
    try:
        post_id = frappe.form_dict.get("post_id")
        comment_text = frappe.form_dict.get("comment_text")

        if not post_id:
            return custom_response("Post ID is required", status_code=400)

        if not comment_text:
            return custom_response("Comment text is required", status_code=400)

        return CommentManager.create(
            post_id=post_id,
            comment_text=comment_text,
            user_id=frappe.session.user
        ).to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to create comment"
        )
        return custom_response(
            "Failed to create comment",
            status_code=500
        )


@frappe.whitelist()
def get(post_id, limit=10, offset=0):
    try:
        return CommentManager.get(
            post_id=post_id,
            limit=limit,
            offset=offset
        ).to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to get comments"
        )

        return custom_response(
            "Failed to get comments",
            status_code=500
        )
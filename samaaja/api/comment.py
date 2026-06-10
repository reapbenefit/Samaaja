# samaaja/api/comment.py

import frappe


@frappe.whitelist()
def create_comment(post_id, comment_text, user_id):
    """Create a comment."""
    pass


@frappe.whitelist()
def get_comments(post_id):
    """Get comments for a post."""
    pass


def verify_post_id(post_id):
    """Verify if the post ID exists."""
    pass


def verify_user_id(user_id):
    """Verify if the user ID exists."""
    pass








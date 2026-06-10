import frappe
from samaaja.services.community_post import CommunityPostManager
from samaaja.utils.custom_response import custom_response


@frappe.whitelist()
def create_comment(post_id, user_id, comment):
    """Create a comment for a post."""
    pass


@frappe.whitelist()
def get_comments(post_id):
    """Fetch comments for a post."""
    pass


def validate_post(post_id):
    """Validate that the post exists."""
    pass


def validate_user(user_id):
    """Validate that the user exists."""
    pass
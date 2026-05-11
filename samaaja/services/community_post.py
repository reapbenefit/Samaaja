from samaaja.utils.result import Result
import frappe
from samaaja.services.user import UserManager
from frappe.utils import get_url


class CommunityPostManager:
    def __init__(self):
        pass

    @staticmethod
    def get() -> Result:
        try:
            posts = frappe.db.sql("""
                SELECT 
                    `name`,
                    `title`,
                    `description`,
                    `media`,
                    `creation`,
                    `like_count`,
                    `user`,
                    `tag`
                FROM `tabCommunity Post`
                ORDER BY `creation` DESC
            """, as_dict=True)

            for post in posts:
                user_profile = UserManager.get_profile(post["user"])
                post["user_profile"] = user_profile.data
                post["id"]=post["name"]
                
                if post["media"]:
                    post["media"]=get_url(post["media"])
            return Result.success(
                "Community posts fetched successfully",
                data=posts
            )
        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to fetch community posts"
            )

            return Result.failure(
                "Failed to fetch community posts",
                error_data=str(e)
            )
        
    @staticmethod
    def create(title: str, description: str, media: str, user: str, action_doc:str, tag:str) -> Result:
        try:
            post = frappe.new_doc("Community Post")
            post.title = title
            post.description = description
            post.media = media
            post.user = user
            post.action=action_doc
            post.tag = tag
            post.save(ignore_permissions=True)
            return Result.success(
                "Community post created successfully",
                data=post
            )
        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to create community post"
            )

            return Result.failure(
                "Failed to create community post",
                error_data=str(e)
            )

def create(doc_name:str):
    """Module-level wrapper for frappe.enqueue dotted-path imports."""
    action_doc = frappe.db.get_value(
        "Action",
        doc_name,
        [
            "title",
            "description",
            "attachment_1",
            "user",
            "category"
        ],
        as_dict=True
    )
    CommunityPostManager.create(action_doc["title"], action_doc["description"], action_doc["attachment_1"], action_doc["user"], doc_name, action_doc["category"])
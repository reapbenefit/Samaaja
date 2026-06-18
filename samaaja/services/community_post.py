from samaaja.utils.result import Result
import frappe
from samaaja.services.user import UserManager
from io import BytesIO
from werkzeug.datastructures import FileStorage
from frappe.utils.image import optimize_image
from frappe.utils.file_manager import save_file
from frappe.model.naming import set_new_name

class CommunityPostManager:
    def __init__(self):
        pass
    
    @staticmethod
    def like(post_id:str, user_id:str) -> Result:
        try:
            post = frappe.get_doc("Community Post",post_id)
            if not post:
                return Result.bad_request("Community post not found")

            if post.user == user_id:
                return Result.bad_request("You cannot like your own post")

            if(post.like_count is None):
                post.like_count = 0
            post.like_count += 1
            post.save(ignore_permissions=True)
            return Result.success("Community post liked successfully")

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to like community post"
            )

            return Result.failure(
                "Failed to like community post",
                error_data=str(e)
            )

    @staticmethod
    def unlike(post_id:str, user_id:str) -> Result:
        try:
            post = frappe.get_doc("Community Post", post_id)
            if not post:
                return Result.bad_request("Community post not found")

            if post.user == user_id:
                return Result.bad_request("You cannot unlike your own post")

            # Ensure like_count doesn't go below 0
            if post.like_count is None or post.like_count <= 0:
                post.like_count = 0
            else:
                post.like_count -= 1
                
            post.save(ignore_permissions=True)
            return Result.success("Community post unliked successfully")

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to unlike community post"
            )

            return Result.failure(
                "Failed to unlike community post",
                error_data=str(e)
            )

    @staticmethod
    def get(limit=10, offset=0) -> Result:
        try:
            limit = int(limit)
            offset = int(offset)

            posts = frappe.db.sql("""
                SELECT 
                    `name`,
                    `title`,
                    `description`,
                    `media`,
                    `creation`,
                    `like_count`,
                    `comment_count`,
                    `user`,
                    `tag`
                FROM `tabCommunity Post`
                ORDER BY `creation` DESC
                LIMIT %s OFFSET %s
            """, (limit, offset), as_dict=True)

            media_base_url = frappe.conf.media_base_url

            for post in posts:
                user_profile = UserManager.get_profile(post["user"])

                post["user_profile"] = user_profile.data
                post["id"] = post["name"]

                if post["media"]:
                    post["media"] = f"{media_base_url}{post['media']}"

            return Result.success(
                "Community posts fetched successfully",
                data={
                    "posts": posts,
                    "limit": limit,
                    "offset": offset,
                    "has_more": len(posts) == limit
                }
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
    def create(description: str, media: str, user: str, action_doc:str, tag:str, title:str=None) -> Result:
        try:
            post = frappe.new_doc("Community Post")
            if title:
                post.title = title
            post.description = description
            set_new_name(post)
            if isinstance (media,str):
                post.media = media
            elif isinstance(media,FileStorage):
                file_content = media.stream.read()

                # optimize image
                optimized_content = optimize_image(
                    BytesIO(file_content),
                    content_type=media.content_type
                )   
                saved_file = save_file(
                        fname=media.filename,
                        content=optimized_content.getvalue(),
                        is_private=0,
                        dt="Community Post",
                        dn=post.name
                    )
                post.media = saved_file.file_url
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
            "description",
            "attachment_1",
            "user",
            "category",
            "type"
        ],
        as_dict=True
    )
    tag = action_doc["category"] + ", " + action_doc["type"]
    CommunityPostManager.create(action_doc["description"], action_doc["attachment_1"], action_doc["user"], doc_name, tag)
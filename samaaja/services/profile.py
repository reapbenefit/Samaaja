import frappe
from samaaja.utils.result import Result
from samaaja.model.action import Action
from samaaja.services.user import UserManager


class ProfileManager:

    @staticmethod
    def get_posts(user, limit=10, offset=0) -> Result:
        try:
            limit = int(limit)
            offset = int(offset)

            # Check if user exists
            if not frappe.db.exists("User", user):
                return Result.failure(
                    "No user found",
                    error_data=f"User '{user}' does not exist.",
                )

            posts = frappe.db.sql(
                """
                SELECT
                    name,
                    title,
                    description,
                    media,
                    creation,
                    like_count,
                    user,
                    tag
                FROM `tabCommunity Post`
                WHERE user = %s
                ORDER BY creation DESC
                LIMIT %s OFFSET %s
                """,
                (user, limit, offset),
                as_dict=True,
            )

            media_base_url = frappe.conf.get("media_base_url", "")

            user_profile = UserManager.get_profile(user)
            profile_data = user_profile.data if user_profile.success else {}

            for post in posts:
                post["id"] = post["name"]
                post["user_profile"] = profile_data

                if post.get("media"):
                    post["media"] = f"{media_base_url}{post['media']}"

            return Result.success(
                "User community posts fetched successfully",
                data={
                    "posts": posts,
                    "limit": limit,
                    "offset": offset,
                    "has_more": len(posts) == limit,
                },
            )

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to fetch user community posts",
            )

            return Result.failure(
                "Failed to fetch user community posts",
                error_data=str(e),
            )

    @staticmethod
    def get_actions(
        user: str,
        limit: int = 10,
        offset: int = 0,
    ) -> Result:
        try:
            limit = int(limit)
            offset = int(offset)

            actions = frappe.db.sql(
                """
                SELECT
                    name,
                    category,
                    type,
                    user,
                    hours_invested,
                    description,
                    attachment_1,
                    attachment_2,
                    creation,
                    modified
                FROM `tabAction`
                WHERE user = %s
                ORDER BY creation DESC
                LIMIT %s OFFSET %s
                """,
                (user, limit, offset),
                as_dict=True,
            )

            media_base_url = frappe.conf.get("media_base_url", "")

            def build_media_urls(action):
                urls = []
                for field in ("attachment_1", "attachment_2"):
                    val = action.get(field)
                    if val:
                        urls.append(f"{media_base_url}{val}")
                return urls

            action_list = [
               {
        "action_id": action.name,
        "action_category": action.category,
        "action_type": action.type,
        "user_id": action.user,
        "hours_invested": action.hours_invested,
        "description": action.description,
        "media": build_media_urls(action),
        "created_at": action.creation,
        "updated_at": action.modified,
    }
    for action in actions
            ]

            return Result.success(
                "User actions fetched successfully",
                data={
                    "actions": action_list,
                    "limit": limit,
                    "offset": offset,
                    "has_more": len(action_list) == limit,
                },
            )

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to get user actions",
            )

            return Result.failure(
                "Failed to get user actions",
                error_data=str(e),
            )
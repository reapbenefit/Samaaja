from samaaja.utils.result import Result
import frappe


class CommunityPostCommentManager:
    def __init__(self):
        pass

    @staticmethod
    def create(post_id: str, comment_text: str, user_id: str) -> Result:
        try:
            if not frappe.db.exists("Community Post", post_id):
                return Result.bad_request("Community post not found")

            comment = frappe.new_doc("Community Post Comment")
            comment.post = post_id
            comment.comment_text = comment_text
            comment.user = user_id
            comment.save(ignore_permissions=True)

            # Increment comment count on the post
            frappe.db.sql(
                """
                UPDATE `tabCommunity Post`
                SET comment_count = COALESCE(comment_count, 0) + 1
                WHERE name = %s
                """,
                (post_id,)
            )

            frappe.db.commit()

            return Result.success(
                "Comment created successfully",
                data=comment
            )

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to create comment"
            )

            return Result.failure(
                "Failed to create comment",
                error_data=str(e)
            )

    @staticmethod
    def get(post_id: str, limit=10, offset=0) -> Result:
        try:
            if not frappe.db.exists("Community Post", post_id):
                return Result.bad_request("Community post not found")

            limit = int(limit)
            offset = int(offset)

            comments = frappe.db.sql(
                """
                SELECT
                    c.name,
                    c.comment_text,
                    c.user,
                    c.creation,
                    u.full_name,
                    u.user_image
                FROM `tabCommunity Post Comment` c
                LEFT JOIN `tabUser` u
                    ON c.user = u.name
                WHERE c.post = %s
                ORDER BY c.creation DESC
                LIMIT %s OFFSET %s
                """,
                (post_id, limit, offset),
                as_dict=True
            )

            return Result.success(
                "Comments retrieved successfully",
                data={
                    "comments": comments,
                    "limit": limit,
                    "offset": offset,
                    "has_more": len(comments) == limit
                }
            )

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to fetch comments"
            )

            return Result.failure(
                "Failed to fetch comments",
                error_data=str(e)
            )
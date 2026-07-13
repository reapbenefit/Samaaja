from samaaja.utils.result import Result
import frappe


class CommentManager:
    def __init__(self):
        pass

    @staticmethod
    def create(post_id: str, comment_text: str, user_id: str) -> Result:
        try:
            if not frappe.db.exists("Community Post", post_id): 
                return Result.bad_request("Community post not found")

            comment = frappe.new_doc("User Comment")
            comment.post_id = post_id
            comment.comment_text = comment_text
            comment.user_id = user_id
            comment.save(ignore_permissions=True)

            # Increment comment count on the post via ORM
            post = frappe.get_doc("Community Post", post_id)
            post.comment_count = frappe.db.count(
    "User Comment",
    {"post_id": post_id}
)
            post.save(ignore_permissions=True)

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
    def get_list(post_id: str, limit=10, offset=0) -> Result:
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
                    c.user_id,
                    c.creation,
                    u.full_name,
                    u.user_image
                FROM `tabUser Comment` c
                LEFT JOIN `tabUser` u
                    ON c.user_id = u.name
                WHERE c.post_id = %s
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
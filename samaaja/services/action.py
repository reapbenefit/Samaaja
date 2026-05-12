import frappe
from frappe.utils import cint
from frappe.utils import flt
from samaaja.utils.result import Result
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count 
from frappe.utils import logger
from pypika.terms import Order
from frappe.utils.file_manager import save_file
from werkzeug.datastructures import FileStorage
from frappe.utils.image import optimize_image
from io import BytesIO
from frappe.model.naming import set_new_name
from typing import Optional

logger.set_log_level("DEBUG")
logger = frappe.logger("samaaja", allow_site=True, file_count=50)

class ActionManager:
    @staticmethod
    def update_action_details_in_user_metadata(doc_name: str):
        try:
            doc = frappe.get_doc("Action", doc_name)
            if not doc or not doc.user:
                return

            total_actions = ActionManager.calculate_total_actions(doc.user)
            hours_invested = ActionManager.calculate_hours_invested(doc.user)

            frappe.db.set_value(
                "User Metadata",
                doc.user,
                {
                    "last_action": doc.name,
                    "last_action_date": doc.creation,
                    "last_action_type": doc.type,
                    "last_action_category": doc.category,
                    "action_count": total_actions,
                    "hours_invested":hours_invested
                },
                update_modified=True
            )

        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to update user metadata"
            )
    
    @staticmethod
    def calculate_total_actions(user_name: str) -> int:
        try:
            count = frappe.db.sql("""
                SELECT COUNT(*) AS count
                FROM `tabAction`
                WHERE `user` = %s
            """, (user_name,), as_dict=True)

            if count:
                return cint(count[0].count)

            return 0

        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to calculate action count"
            )
            return 0

    @staticmethod
    def calculate_hours_invested(user_name: str) -> int:
        try:
            count = frappe.db.sql("""
                SELECT SUM(hours_invested) AS count
                FROM `tabAction`
                WHERE `user` = %s
            """, (user_name,), as_dict=True)

            if count:
                return flt(count[0].count)

            return 0

        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to calculate hours invested"
            )
            return 0

    @staticmethod
    def get_top_user_action_categories(user: str, limit: int = 3) -> str:
        """
        Returns a comma-separated string of top action categories for the given user
        """
        Action = DocType("Action")

        # Alias for COUNT(*) to use in select and order by
        count_alias = Count("*").as_("count")

        # Step 1: Query top N categories where category is not null for the given user
        category_data = (
            frappe.qb.from_(Action)
            .select(Action.category.as_("category"), count_alias)
            .where((Action.user == user) & Action.category.isnotnull())
            .groupby(Action.category)
            .orderby(count_alias, order=Order.desc)
            .limit(limit)
        ).run(as_dict=True)
        # Step 2: Extract category names from the result
        category_list = [row["category"] for row in category_data]

        # Step 3: Convert the list to a comma-separated string
        return ", ".join(category_list)

    @staticmethod
    def create(
    description: str,
    hours_invested: float,
    category: str,
    user: str,
    media=None,
    title: Optional[str] = None
    ) -> Result:
        try:
            action = frappe.new_doc("Action")
            set_new_name(action)
            if title:
                action.title = title
            elif description and len(description) > 100:
                action.title = f"{description[:100]}..."
            else:
                action.title = description
            action.description = description
            action.hours_invested = hours_invested
            action_category = frappe.db.get_value("Action Category", {"category": category}, "name")
            if action_category:
                action.category = action_category
            action.user = user

            if media:
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
                        dt="Action",
                        dn=action.name
                    )
                action.attachment_1 = saved_file.file_url
            
            action.insert(ignore_permissions=True)
            return Result.success("Action created successfully")
        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to create action"
            )
            return Result.failure(str(e))
            
    @staticmethod
    def create_from_dashboard(title: str, description: str, hours_invested: float, category: str):
        if not frappe.session.user == "Guest":
            ActionManager.create(title, description, hours_invested, category, frappe.session.user)

def update_action_details_in_user_metadata(doc_name: str):
    """Module-level wrapper for frappe.enqueue dotted-path imports."""
    ActionManager.update_action_details_in_user_metadata(doc_name)
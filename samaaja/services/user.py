from samaaja.utils.result import Result
import frappe
from frappe.utils import get_url
from samaaja.services.action import ActionManager
from frappe.utils import logger
from samaaja.utils.utils import validate_mobile_no
from datetime import datetime

logger.set_log_level("DEBUG")
logger = frappe.logger("samaaja", allow_site=True, file_count=50)
class UserManager:
    
    @staticmethod
    def create(full_name:str,dob:str,gender:str,category:str,mobile_no:str,bio:str)->Result:
        
        try:
            user = frappe.new_doc("User")
            user.first_name = full_name
            formatted_dob = datetime.strptime(dob, "%Y-%m-%d").date()
            user.birth_date = formatted_dob
            user.gender = gender
            user.mobile_no = mobile_no
            user.email=mobile_no+"@samaaja.com"
            user.flags.no_welcome_mail = True
            user.send_welcome_email = 0
            user.save(ignore_permissions=True)
        
            user_metadata = frappe.get_doc(
                            "User Metadata",
                            {"user": user.email}
                            )
            user_category_name = frappe.db.get_value("User Category", {"category_name": category}, "name")
            user_metadata.user_category = user_category_name
            user_metadata.save(ignore_permissions=True)
            return Result.success(
                "User created successfully",
                data={
                    "user": user,
                    "user_metadata": user_metadata
                }
            )
        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to create user"
            )
            return Result.failure(
                "Failed to create user",
                error_data=str(e)
            )
    
    @staticmethod
    def get_profile(user_email: str) -> Result:
        try:

            user = frappe.db.get_value(
                    "User",
                    user_email,
                    [
                        "name",
                        "full_name",
                        "email",
                        "mobile_no",
                        "gender",
                        "user_image",
                        "interest",
                        "bio",
                        "birth_date"
                    ],
                    as_dict=True
                )

            if not user:
                return Result.not_found("User not found")

            user_metadata = frappe.db.get_value(
                "User Metadata",
                {"user": user_email},
                [
                    "action_count",
                    "last_action",
                    "last_action_date",
                    "last_action_type",
                    "last_action_category",
                    "user_category",
                    "hours_invested"
                ],
                as_dict=True
            )
            user["user_image"]=get_url(user["user_image"])
            if user_metadata:
                if user_metadata["user_category"]:
                    user_category_name = frappe.db.get_value("User Category", user_metadata["user_category"], "category_name")
                    user_metadata["user_category"] = user_category_name
                result = {**user, **user_metadata}
            else:
                result = user
            
            if user["interest"]:
                interest_array = user["interest"].split(",")
                interests = []
                for interest in interest_array:
                    icon = frappe.db.get_value("Action Category", interest, "icon")
                    interests.append(
                        {
                            "action_category": interest,
                            "icon": get_url(icon) if icon else ""
                        }
                    )
                result["interests"] = interests

            return Result.success(
                "User profile fetched successfully",
                data=result
            )

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to fetch user profile"
            )

            return Result.failure(
                "Failed to fetch user profile",
                error_data=str(e)
            )
    
    @staticmethod
    def update_user_interest_from_top_categories(user: str):
        if not user or not frappe.db.exists("User", user):
            return

        top_categories = ActionManager.get_top_user_action_categories(user)
        frappe.db.set_value(
            "User", 
            user, 
            {
                "interest":top_categories
            },
            update_modified=True
        )

    @staticmethod
    def complete_user_profile(user_email:str, user_mobile_no:str, user_gender:str,user_category:str,user_bio:str,user_dob:str)-> Result:
        try:
            if not validate_mobile_no(user_mobile_no):
                return Result.bad_request(
                    "Invalid mobile number"
                )

            user_category = frappe.db.get_value("User Category", {"category_name": user_category}, "name")

            if not user_category :
                return Result.bad_request(
                    "Invalid user category"
                )
            if not frappe.db.exists("User Metadata", user_email):
                frappe.log_error(
                    f"No user metadata found for this user {user_email}",
                    "No user metadata found for this user"
                )
                return Result.not_found(
                    "No user metadata found for this user"
                )
            user = frappe.get_doc("User", user_email)
            user.gender = user_gender
            user.bio = user_bio
            user.mobile_no = user_mobile_no
            user.birth_date = user_dob
            user.save(ignore_permissions=True)

            user_metadata = frappe.get_doc("User Metadata", user_email)
            user_metadata.user_category = user_category
            user_metadata.save(ignore_permissions=True)
            
            return Result.success(
                "User profile completed successfully"
            )
        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to complete user profile"
            )
            return Result.failure(
                "Failed to complete user profile",
                error_data=str(e)
            )

def update_user_interest_from_top_categories(doc_name: str):
    """Module-level wrapper for frappe.enqueue dotted-path imports."""
    user_dict = frappe.db.get_value(
                "Action",
                doc_name,
                [
                    "user"
                ],
                as_dict=True
            )
    UserManager.update_user_interest_from_top_categories(user_dict["user"])
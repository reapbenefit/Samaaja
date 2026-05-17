from samaaja.utils.result import Result
import frappe
from samaaja.services.action import ActionManager
from frappe.utils import logger
from samaaja.utils.utils import validate_mobile_no
from datetime import datetime
from frappe.auth import LoginManager


logger.set_log_level("DEBUG")
logger = frappe.logger("samaaja", allow_site=True, file_count=50)
media_base_url = frappe.conf.media_base_url

class UserManager:
    
    #mobile number should be unique...to do

    @staticmethod
    def create(full_name:str,dob:str,gender:str,category:str,mobile_no:str,bio:str)->Result:
        
        try:
            if frappe.db.exists("User", {"mobile_no": mobile_no}):
                return Result.bad_request("User already exists with this mobile number")
            user = frappe.new_doc("User")
            user.first_name = full_name
            formatted_dob = datetime.strptime(dob, "%Y-%m-%d").date()
            user.birth_date = formatted_dob
            user.gender = gender
            user.bio=bio
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


            frappe.local.login_manager = LoginManager()
            frappe.local.login_manager.user = user.email
            frappe.local.login_manager.post_login()
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
            
            if user["user_image"] and user["user_image"].startswith("http"):
                pass
            else:
                user["user_image"]= f"{media_base_url}{user['user_image']}" if user["user_image"] else ""
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
                    icon = frappe.db.get_value("Action Category", interest.strip(), "icon")
                    interests.append(
                        {
                            "action_category": interest.strip(),
                            "icon": f"{media_base_url}{icon}" if icon else ""
                        }
                    )
                result["interests"] = interests

            community_count = frappe.db.count(
                "Community Post",
                filters={
                    "user": user_email
                }
                )
            result["posts"] = community_count
            

            badges = frappe.get_list(
                "User Badge",
                filters={
                    "user": user_email
                },
                fields=[
                    "badge",
                    "badge_count"
                ]
            )

            badges_list = []
            for badge in badges:
                badge_doc = frappe.get_doc("Badge", badge.badge)
                badges_list.append(
                    {
                        "badge": badge.badge,
                        "badge_name": badge_doc.title,
                        "badge_icon": f"{media_base_url}{badge_doc.icon}" if badge_doc.icon else "",
                        "badge_count":badge.badge_count
                    }
                )
            result["badges"] = badges_list

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
            if frappe.db.exists("User", {"mobile_no": user_mobile_no}):
                return Result.bad_request("User with this mobile number already exists")

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
    
    @staticmethod
    def login_using_OTP(mobile_no: str, otp:str):
        try:
            if not otp == '1111':
                return Result.bad_request(
                    "Invalid OTP"
                )
            
            user = frappe.get_value(
                "User",
                {"mobile_no":mobile_no},
                [
                    "name",
                ]
            )
            if not user:
                return Result.not_found(
                    "User not found"
                )

            login_manager = LoginManager()
            login_manager.login_as(user)

            user_doc = frappe.get_doc("User", user)
            if not user_doc.api_key:
                user_doc.api_key = frappe.generate_hash(length=15)

            api_secret = frappe.generate_hash(length=15)

            user_doc.api_secret = api_secret
            user_doc.save(ignore_permissions=True)

            return Result.success(
                "User logged in successfully",
                data={
                    "user": user,
                    "api_key": user_doc.api_key,
                    "api_secret": api_secret
                }
            )
        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to log in user"
            )
            return Result.failure(
                "Failed to log in user",
                error_data=str(e)
            )

    @staticmethod
    def update_user_metadata(user_id:str):
        try:
            last_action = ActionManager.get_last_action(user_id)
            user_metadata = frappe.get_doc("User Metadata", user_id)

            if not last_action:
                user_metadata.last_action = None
                user_metadata.last_action_date = None
                user_metadata.last_action_type = None
                user_metadata.last_action_category = None
            else:
                user_metadata.last_action = last_action.action_id
                user_metadata.last_action_date = last_action.action_date
                user_metadata.last_action_type = last_action.action_type
                user_metadata.last_action_category = last_action.action_category
            user_metadata.action_count = ActionManager.calculate_total_actions(user_id)
            user_metadata.hours_invested = ActionManager.calculate_hours_invested(user_id)
            user_metadata.save(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to update user metadata"
            )
            return Result.failure(
                "Failed to update user metadata",
                error_data=str(e)
            )

def update_user_interest_from_top_categories(doc_name: str):
    """Module-level wrapper for frappe.enqueue dotted-path imports."""
    user = frappe.db.get_value("Action", doc_name, "user")

    if user:
        UserManager.update_user_interest_from_top_categories(user)

def update_user_metadata(doc_name: str):
    """Module-level wrapper for frappe.enqueue dotted-path imports."""
    user_dict = frappe.db.get_value(
                "Action",
                doc_name,
                [
                    "user"
                ],
                as_dict=True
            )
    UserManager.update_user_metadata(user_dict["user"])
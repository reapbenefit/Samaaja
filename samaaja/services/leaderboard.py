from samaaja.utils.result import Result
import frappe
from samaaja.services.user import UserManager

class LeaderboardManager:
    @staticmethod
    def get_leaderboard(org_name: str = None) -> Result:
        try:
            leaderboard_data = []
            if org_name:
                leaderboard_data = frappe.db.get_list("User", fields=["name", "full_name", "email", "mobile_no", "gender", "user_image", "interest"], order_by="name", filters={"org_name": org_name})
            else:
                result = frappe.db.sql("""
                                            SELECT
                                                um.user,
                                                u.name
                                            FROM `tabUser Metadata` um
                                            LEFT JOIN `tabUser` u
                                                ON um.user = u.name
                                            WHERE um.action_count > 0
                                            ORDER BY um.action_count DESC
                                            LIMIT 10
                                        """, as_dict=True)
                for row in result:
                    user = UserManager.get_profile(row["user"]).data
                    leaderboard_data.append(user)
            return Result.success("Leaderboard fetched successfully", data=leaderboard_data)
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Failed to fetch leaderboard")
            return Result.failure("Failed to fetch leaderboard", error_data=str(e))
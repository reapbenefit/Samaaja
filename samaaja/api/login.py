import frappe
from frappe.utils.oauth import get_oauth2_authorize_url
from samaaja.services.user import UserManager
from samaaja.utils.custom_response import custom_response

@frappe.whitelist(allow_guest=True)
def get_google_auth_url():
    """
    Directly uses the 'google' ID to generate the secure login URL.
    """
    # We use 'google' lowercase because that is the ID in your screenshot
    provider = "google" 
    
    try:
        # Generate the secure URL with CSRF token and the homepage redirect
        return get_oauth2_authorize_url(provider, redirect_to="/homepage")
    except Exception:
        # Logs the error in Frappe Desk if something goes wrong with the database
        frappe.log_error(frappe.get_traceback(), "Google Auth URL Generation Failed")
        frappe.throw("Could not generate login URL. Please check your Social Login Key settings.")

@frappe.whitelist(allow_guest=True)
def login_using_otp(mobile_no:str,otp:str):
    try:
        return UserManager.login_using_OTP(mobile_no, otp).to_custom_response()
    except Exception as e:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to log in user"
        )
        return custom_response(status_code=500, message="Internal Server Error")
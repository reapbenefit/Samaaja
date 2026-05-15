import frappe
from samaaja.services.announcement import AnnouncementManager
from samaaja.api.common import custom_response
from http import HTTPStatus

@frappe.whitelist(allow_guest=True)
def get_active_announcements():
    try:
        announcements = AnnouncementManager.get_active_announcements()
        return custom_response("Announcements fetched successfully", data=announcements, status_code=HTTPStatus.OK)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Failed to fetch announcements")
        return custom_response("Failed to fetch announcements", error_data=str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

@frappe.whitelist(allow_guest=True)
def get_unread_count():
    try:
        count = AnnouncementManager.get_unread_count()
        return custom_response("Unread count fetched successfully", data=count, status_code=HTTPStatus.OK)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Failed to fetch unread count")
        return custom_response("Failed to fetch unread count", error_data=str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

@frappe.whitelist(allow_guest=True)
def record_interaction(announcement, interaction_type, contact_id=None):
    try:
        if not announcement or not interaction_type:
            return custom_response("Missing mandatory fields", status_code=HTTPStatus.BAD_REQUEST)
        
        result = AnnouncementManager.record_interaction(announcement, interaction_type, contact_id)
        return custom_response("Interaction recorded successfully", data=result, status_code=HTTPStatus.OK)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Failed to record interaction")
        return custom_response("Failed to record interaction", error_data=str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

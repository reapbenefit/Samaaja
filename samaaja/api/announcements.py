import frappe
from samaaja.services.announcement import AnnouncementManager
from samaaja.utils.result import Result


@frappe.whitelist()
def get_active_announcements():
    return AnnouncementManager.get_active_announcements().to_custom_response()


@frappe.whitelist()
def record_interaction(announcement, interaction_type, contact_id=None):
    if not announcement or not interaction_type:
        return Result.bad_request("announcement and interaction_type are mandatory").to_custom_response()

    return AnnouncementManager.record_interaction(announcement, interaction_type, contact_id).to_custom_response()

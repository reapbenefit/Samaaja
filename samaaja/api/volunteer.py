import frappe

from samaaja.services.volunteer import VolunteerManager
from samaaja.utils.custom_response import custom_response
from samaaja.utils.result import Result


@frappe.whitelist()
def get_list(
    limit=10,
    offset=0,
    location=None,
    category=None,
    skills_needed=None
):
    try:
        return VolunteerManager.get_list(
            limit=limit,
            offset=offset,
            location=location,
            category=category,
            skills_needed=skills_needed
        ).to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to fetch volunteer opportunities"
        )
        return custom_response(
            message="Failed to fetch volunteer opportunities",
            status_code=500
        )


@frappe.whitelist()
def get_by_id(volunteer_id):
    try:
        return VolunteerManager.get_by_id(
            volunteer_id
        ).to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to fetch volunteer opportunity"
        )
        return custom_response(
            message="Failed to fetch volunteer opportunity",
            status_code=500
        )
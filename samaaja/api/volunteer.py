import json
import frappe

from samaaja.services.volunteer import VolunteerManager
from samaaja.utils.custom_response import custom_response
 from samaaja.utils.result import Result


@frappe.whitelist()
def get_list(filters=None, limit=10, offset=0):
    try:
        filters = json.loads(filters) if filters else {}

        return VolunteerManager.get_list(
            filters=filters,
            limit=limit,
            offset=offset
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
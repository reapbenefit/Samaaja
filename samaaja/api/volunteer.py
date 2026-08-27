import json

import frappe

from samaaja.services.volunteer import VolunteerManager
from samaaja.utils.custom_response import custom_response


@frappe.whitelist()
def get_list(filters=None, limit=10, offset=0):
    try:
        if isinstance(filters, str):
            filters = json.loads(filters)

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

@frappe.whitelist()
def apply(
    volunteer_opportunity,
    full_name,
    email,
    phone_number,
    age=None,
    gender=None,
    preferred_available_days=None,
    why_do_you_want_to_volunteer=None,
    privacy_consent=False,
):
    try:

        # Pseudocode:
        # 1. Get the currently logged-in user.
        #
        # 2. Call VolunteerManager.apply() with:
        #    - logged-in user
        #    - volunteer opportunity
        #    - full name
        #    - email
        #    - phone number
        #    - age
        #    - gender
        #    - preferred available days
        #    - reason for volunteering
        #    - privacy consent
        #
        # 3. Convert the returned Result into the standard
        #    custom API response.

        pass

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to submit volunteer application"
        )

        return custom_response(
            message="Failed to submit volunteer application",
            status_code=500
        )
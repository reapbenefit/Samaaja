import json

import frappe

from samaaja.services.volunteer import VolunteerManager
from samaaja.utils.custom_response import custom_response


@frappe.whitelist(methods=["GET"])
def get_list(filters=None, limit=10, offset=0):
    try:
        if frappe.session.user == "Guest":
            return custom_response(
                message="Authentication required",
                status_code=401
            )

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


@frappe.whitelist(methods=["GET"])
def get(volunteer_id):
    try:
        if frappe.session.user == "Guest":
            return custom_response(
                message="Authentication required",
                status_code=401
            )

        return VolunteerManager.get(
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


@frappe.whitelist(methods=["POST"])
def apply(
    volunteer_opportunity,
    age=None,
    preferred_available_days=None,
    why_do_you_want_to_volunteer=None,
    privacy_consent=False,
):
    try:
        if frappe.session.user == "Guest":
            return custom_response(
                message="Authentication required",
                status_code=401
            )

        return VolunteerManager.apply(
            user=frappe.session.user,
            volunteer_opportunity=volunteer_opportunity,
            age=age,
            preferred_available_days=preferred_available_days,
            why_do_you_want_to_volunteer=why_do_you_want_to_volunteer,
            privacy_consent=privacy_consent,
        ).to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to submit volunteer application"
        )

        return custom_response(
            message="Failed to submit volunteer application",
            status_code=500
        )
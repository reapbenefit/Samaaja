import frappe

from samaaja.services.metadata import DropdownManager
from samaaja.utils.custom_response import custom_response


@frappe.whitelist(methods=["GET"])
def get_list(doctype, lang="en"):
    try:
        if frappe.session.user == "Guest":
            return custom_response(
                message="Authentication required",
                status_code=401
            )

        return DropdownManager.get_list(
            doctype=doctype,
            lang=lang
        ).to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to fetch dropdown options"
        )

        return custom_response(
            message="Failed to fetch dropdown options",
            status_code=500
        )
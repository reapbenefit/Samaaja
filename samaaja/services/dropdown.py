import frappe

from samaaja.utils.result import Result


OPTIONS = {
    "Gender": {
        "doctype": "Gender",
        "field": "gender",
        "defaults": {},
    },
    "User Category": {
        "doctype": "User Category",
        "field": "category_name",
        "defaults": {"is_active": 1},
    },
    "Action Type": {
        "doctype": "Action Type",
        "field": "type",
        "defaults": {},
    },
    "Action Category": {
        "doctype": "Action Category",
        "field": "category_name",
        "defaults": {},
    },
}


class DropdownManager:

    @staticmethod
    def get_list(
        doctype: str,
        lang: str = "en",
    ) -> Result:
        try:
            if not doctype:
                return Result.bad_request(
                    "Doctype is required"
                )

            if doctype not in OPTIONS:
                return Result.not_found(
                    "Dropdown options not found for the requested doctype"
                )

            config = OPTIONS[doctype]

            values = frappe.get_all(
                config["doctype"],
                filters=config["defaults"],
                fields=[config["field"]],
                pluck=config["field"],
            )

            data = {
                doctype: [
                    frappe._(value, lang=lang)
                    for value in values
                    if value
                ]
            }

            return Result.success(
                "Dropdown options fetched successfully",
                data=data,
            )

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to fetch dropdown options"
            )

            return Result.failure(
                "Failed to fetch dropdown options",
                error_data=str(e),
            )
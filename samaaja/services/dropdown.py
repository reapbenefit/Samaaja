import frappe

from samaaja.utils.result import Result


DROPDOWN_CONFIG = {
    "Gender": {
        "doctype": "Gender",
        "field": "gender",
        "filters": {},
    },
    "User Category": {
        "doctype": "User Category",
        "field": "category_name",
        "filters": {"is_active": 1},
    },
    "Action Type": {
        "doctype": "Action Type",
        "field": "type",
        "filters": {},
    },
    "Action Category": {
        "doctype": "Action Category",
        "field": "category",
        "filters": {},
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

            if doctype not in DROPDOWN_CONFIG:
                return Result.not_found(
                    "Dropdown options not found for the requested doctype"
                )

            config = DROPDOWN_CONFIG[doctype]

            values = frappe.get_all(
                config["doctype"],
                filters=config["filters"],
                fields=[config["field"]],
                pluck=config["field"],
            )

            data = [
                frappe._(value, lang=lang)
                for value in values
                if value
            ]

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
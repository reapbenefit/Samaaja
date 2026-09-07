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
    "Location": {
        "doctype": "Samaaja Location",
        "field": "city",
        "filters": {},
    },
    "Category": {
        "doctype": "Action Category",
        "field": "category",
        "filters": {},
    },
    "Skill": {
        "doctype": "Skills",
        "field": "skill_name",
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

            # Return only categories used in active volunteer opportunities.
            if doctype == "Category":
                values = frappe.get_all(
                    "Volunteer Opportunity",
                    filters={"status": "Active"},
                    fields=["category"],
                    pluck="category",
                )

                data = list(dict.fromkeys(
                    value for value in values if value
                ))

                return Result.success(
                    "Dropdown options fetched successfully",
                    data=data,
                )

            # Volunteer Opportunity stores a link to Samaaja Location.
            # Return only cities from locations used in active opportunities.
            if doctype == "Location":
                locations = frappe.get_all(
                    "Volunteer Opportunity",
                    filters={"status": "Active"},
                    fields=["location"],
                    pluck="location",
                )

                locations = [
                    location for location in locations
                    if location
                ]

                if not locations:
                    return Result.success(
                        "Dropdown options fetched successfully",
                        data=[],
                    )

                values = frappe.get_all(
                    "Samaaja Location",
                    filters={
                        "name": ["in", locations],
                    },
                    fields=["city"],
                    pluck="city",
                )

                data = list(dict.fromkeys(
                    value for value in values if value
                ))

                return Result.success(
                    "Dropdown options fetched successfully",
                    data=data,
                )

            # Skills are stored in Skill Child Table.
            # Return only skills used in active volunteer opportunities.
            if doctype == "Skill":
                opportunities = frappe.get_all(
                    "Volunteer Opportunity",
                    filters={"status": "Active"},
                    fields=["name"],
                    pluck="name",
                )

                if not opportunities:
                    return Result.success(
                        "Dropdown options fetched successfully",
                        data=[],
                    )

                values = frappe.get_all(
                    "Skill Child Table",
                    filters={
                        "parent": ["in", opportunities],
                        "parenttype": "Volunteer Opportunity",
                    },
                    fields=["skill"],
                    pluck="skill",
                )

                data = list(dict.fromkeys(
                    value for value in values if value
                ))

                return Result.success(
                    "Dropdown options fetched successfully",
                    data=data,
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
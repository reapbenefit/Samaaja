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
VOLUNTEER_FILTER_CONFIG = {
    "Category": {
        "handler": "_get_active_categories",
    },
    "Location": {
        "handler": "_get_active_locations",
    },
    "Skill": {
        "handler": "_get_active_skills",
    },
}


class MetadataManager:

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

            if (
                doctype not in VOLUNTEER_FILTER_CONFIG
                and doctype not in DROPDOWN_CONFIG
            ):
                return Result.not_found(
                    "Dropdown options not found for the requested doctype"
                )

            if doctype in VOLUNTEER_FILTER_CONFIG:
                handler_name = VOLUNTEER_FILTER_CONFIG[doctype]["handler"]
                values = getattr(MetadataManager, handler_name)()

                return Result.success(
                    "Dropdown options fetched successfully",
                    data=values,
                )

            values = MetadataManager._get_direct_options(
                DROPDOWN_CONFIG[doctype],
                lang=lang,
            )

            return Result.success(
                "Dropdown options fetched successfully",
                data=values,
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

    @staticmethod
    def _get_active_categories():
        values = frappe.get_all(
            "Volunteer Opportunity",
            filters={"status": "Active"},
            fields=["category"],
            pluck="category",
            order_by="category asc",
        )

        return list(dict.fromkeys(
            value for value in values if value
        ))

    @staticmethod
    def _get_active_locations():
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
            return []

        values = frappe.get_all(
            "Samaaja Location",
            filters={
                "name": ["in", locations],
            },
            fields=["city"],
            pluck="city",
            order_by="city asc",
        )

        return list(dict.fromkeys(
            value for value in values if value
        ))

    @staticmethod
    def _get_active_skills():
        opportunities = frappe.get_all(
            "Volunteer Opportunity",
            filters={"status": "Active"},
            fields=["name"],
            pluck="name",
        )

        if not opportunities:
            return []

        values = frappe.get_all(
            "Skill Child Table",
            filters={
                "parent": ["in", opportunities],
                "parenttype": "Volunteer Opportunity",
            },
            fields=["skill"],
            pluck="skill",
            order_by="skill asc",
        )

        return list(dict.fromkeys(
            value for value in values if value
        ))

    @staticmethod
    def _get_direct_options(config, lang="en"):
        values = frappe.get_all(
            config["doctype"],
            filters=config["filters"],
            fields=[config["field"]],
            pluck=config["field"],
        )

        return [
            frappe._(value, lang=lang)
            for value in values
            if value
        ]

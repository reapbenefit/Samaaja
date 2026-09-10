import json

import frappe
from frappe.query_builder import DocType

from samaaja.utils.result import Result


class VolunteerManager:

    @staticmethod
    def get_list(
        filters=None,
        limit: int = 10,
        offset: int = 0,
    ) -> Result:
        try:
            filters = (
                json.loads(filters)
                if isinstance(filters, str)
                else (filters or {})
            )

            limit = int(limit)
            offset = int(offset)

            VolunteerOpportunity = DocType("Volunteer Opportunity")
            SamaajaLocation = DocType("Samaaja Location")

            query = (
                frappe.qb.from_(VolunteerOpportunity)
                .left_join(SamaajaLocation)
                .on(
                    SamaajaLocation.name == VolunteerOpportunity.location
                )
                .select(
                    VolunteerOpportunity.name,
                    VolunteerOpportunity.title,
                    VolunteerOpportunity.description,
                    VolunteerOpportunity.category,
                    SamaajaLocation.city.as_("location"),
                    VolunteerOpportunity.type,
                    VolunteerOpportunity.start_date,
                    VolunteerOpportunity.end_date,
                    VolunteerOpportunity.volunteer_format,
                    VolunteerOpportunity.expected_time_commitment,
                    VolunteerOpportunity.compensation_type,
                    VolunteerOpportunity.status,
                )
                .where(VolunteerOpportunity.status == "Active")
            )

            categories = filters.get("categories") or []
            locations = filters.get("locations") or []
            skills = filters.get("skills") or []

            if categories:
                query = query.where(
                    VolunteerOpportunity.category.isin(categories)
                )

            if locations:
                query = query.where(
                    SamaajaLocation.city.isin(locations)
                )

            if skills:
                SkillChildTable = DocType("Skill Child Table")

                query = (
                    query
                    .join(SkillChildTable)
                    .on(
                        SkillChildTable.parent == VolunteerOpportunity.name
                    )
                    .where(
                        SkillChildTable.skill.isin(skills)
                    )
                )

            query = (
                query
                .distinct()
                .orderby(
                    VolunteerOpportunity.creation,
                    order=frappe.qb.desc
                )
                .limit(limit)
                .offset(offset)
            )

            opportunities = query.run(as_dict=True)

            opportunity_names = [opportunity["name"] for opportunity in opportunities]

            if opportunity_names:
                skill_rows = frappe.get_all(
                    "Skill Child Table",
                    filters={
                        "parent": ["in", opportunity_names],
                        "parenttype": "Volunteer Opportunity",
                    },
                    fields=["parent", "skill"],
                )
            else:
                skill_rows = []

            skills_by_opportunity = {}

            for row in skill_rows:
                skills_by_opportunity.setdefault(
                    row["parent"],
                    []
                ).append(row["skill"])

            for opportunity in opportunities:
                opportunity["skills_needed"] = skills_by_opportunity.get(
                    opportunity["name"],
                    []
                )

            return Result.success(
                "Volunteer opportunities fetched successfully",
                data={
                    "opportunities": opportunities,
                    "limit": limit,
                    "offset": offset,
                    "has_more": len(opportunities) == limit,
                },
            )

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to fetch volunteer opportunities"
            )

            return Result.failure(
                "Failed to fetch volunteer opportunities",
                error_data=str(e),
            )

    @staticmethod
    def get(volunteer_id: str) -> Result:
        try:
            VolunteerOpportunity = DocType("Volunteer Opportunity")
            SamaajaLocation = DocType("Samaaja Location")

            opportunity = (
                frappe.qb.from_(VolunteerOpportunity)
                .left_join(SamaajaLocation)
                .on(
                    SamaajaLocation.name == VolunteerOpportunity.location
                )
                .select(
                    VolunteerOpportunity.name,
                    VolunteerOpportunity.title,
                    VolunteerOpportunity.description,
                    VolunteerOpportunity.category,
                    SamaajaLocation.city.as_("location"),
                    VolunteerOpportunity.type,
                    VolunteerOpportunity.start_date,
                    VolunteerOpportunity.end_date,
                    VolunteerOpportunity.volunteer_format,
                    VolunteerOpportunity.expected_time_commitment,
                    VolunteerOpportunity.compensation_type,
                    VolunteerOpportunity.status,
                )
                .where(
                    (VolunteerOpportunity.name == volunteer_id)
                    & (VolunteerOpportunity.status == "Active")
                )
            )

            opportunity = opportunity.run(as_dict=True)

            if not opportunity:
                return Result.not_found(
                    "Volunteer opportunity not found"
                )

            opportunity = opportunity[0]

            opportunity["skills_needed"] = frappe.get_all(
                "Skill Child Table",
                filters={
                    "parent": volunteer_id,
                    "parenttype": "Volunteer Opportunity",
                },
                fields=["skill"],
                pluck="skill",
            )

            return Result.success(
                "Volunteer opportunity fetched successfully",
                data={
                    "opportunity": opportunity,
                },
            )

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to fetch volunteer opportunity"
            )

            return Result.failure(
                "Failed to fetch volunteer opportunity",
                error_data=str(e),
            )

    @staticmethod
    def check_application(user, volunteer_opportunity) -> Result:
        try:
            if not volunteer_opportunity:
                return Result.bad_request(
                    "Volunteer opportunity is required"
                )

            if not frappe.db.exists(
                "Volunteer Opportunity",
                {
                    "name": volunteer_opportunity,
                    "status": "Active",
                },
            ):
                return Result.not_found(
                    "Volunteer opportunity not found"
                )

            already_applied = frappe.db.exists(
                "Volunteer Application",
                {
                    "user": user,
                    "volunteer_opportunity": volunteer_opportunity,
                },
            )

            return Result.success(
                "Application status fetched successfully",
                data={
                    "already_applied": bool(already_applied),
                },
            )

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to check volunteer application"
            )

            return Result.failure(
                "Failed to check volunteer application",
                error_data=str(e),
            )

    @staticmethod
    def apply(
        user,
        volunteer_opportunity,
        age=None,
        gender=None,
        preferred_available_days=None,
        why_do_you_want_to_volunteer=None,
        privacy_consent=False,
    ) -> Result:
        try:
            if not volunteer_opportunity:
                return Result.bad_request(
                    "Volunteer opportunity is required"
                )

            if not frappe.db.exists(
                "Volunteer Opportunity",
                {
                    "name": volunteer_opportunity,
                    "status": "Active",
                },
            ):
                return Result.not_found(
                    "Volunteer opportunity not found"
                )

            # Prevent duplicate applications from the same user
            # for the same volunteer opportunity.
            if frappe.db.exists(
                "Volunteer Application",
                {
                    "user": user,
                    "volunteer_opportunity": volunteer_opportunity,
                },
            ):
                return Result.bad_request(
                    "You have already applied for this volunteer opportunity"
                )

            # Normalize privacy consent before validation.
            privacy_consent = frappe.utils.cint(privacy_consent)

            if not privacy_consent:
                return Result.bad_request(
                    "Privacy consent is required"
                )

            allowed_available_days = [
                "Daily",
                "Few times a week",
                "Only on Weekends",
                "Flexible",
            ]

            if (
                preferred_available_days
                and preferred_available_days not in allowed_available_days
            ):
                return Result.bad_request(
                    "Invalid preferred available days"
                )

            application = frappe.new_doc("Volunteer Application")

            application.user = user
            application.volunteer_opportunity = volunteer_opportunity
            application.age = age
            application.gender = gender
            application.preferred_available_days = (
                preferred_available_days
            )
            application.why_do_you_want_to_volunteer = (
                why_do_you_want_to_volunteer
            )
            application.privacy_consent = privacy_consent

            application.insert(ignore_permissions=True)

            return Result.success(
                "Volunteer application submitted successfully",
                data=application,
            )

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to submit volunteer application"
            )

            return Result.failure(
                "Failed to submit volunteer application",
                error_data=str(e),
            )
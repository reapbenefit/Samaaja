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
        filters = (
            json.loads(filters)
            if isinstance(filters, str)
            else (filters or {})
        )

        limit = int(limit)
        offset = int(offset)

        VolunteerOpportunity = DocType("Volunteer Opportunity")
        SkillChildTable = DocType("Skill Child Table")
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

        # Multiple categories use OR.
        # Different filter types use AND.
        if categories:
            query = query.where(
                VolunteerOpportunity.category.isin(categories)
            )

        # Match requested city names against
        # the City field of Samaaja Location.
        if locations:
            query = query.where(
                SamaajaLocation.city.isin(locations)
            )

        # Multiple skills use OR.
        # An opportunity matches if it needs any selected skill.
        if skills:
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

        return Result.success(
            "Volunteer opportunities fetched successfully",
            data={
                "opportunities": opportunities,
                "limit": limit,
                "offset": offset,
                "has_more": len(opportunities) == limit,
            },
        )

    @staticmethod
    def get_by_id(volunteer_id: str) -> Result:
        opportunity = frappe.db.get_value(
            "Volunteer Opportunity",
            {
                "name": volunteer_id,
                "status": "Active",
            },
            [
                "name",
                "title",
                "description",
                "category",
                "location",
                "type",
                "start_date",
                "end_date",
                "volunteer_format",
                "expected_time_commitment",
                "compensation_type",
                "status",
            ],
            as_dict=True,
        )

        if not opportunity:
            return Result.not_found(
                "Volunteer opportunity not found"
            )

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
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

    @staticmethod
    def apply(
        user,
        volunteer_opportunity,
        full_name,
        email,
        phone_number,
        age=None,
        gender=None,
        preferred_available_days=None,
        why_do_you_want_to_volunteer=None,
        privacy_consent=False,
    ) -> Result:

        # Pseudocode:

        # 1. Validate that the user is authenticated.
        #    - Do not allow Guest users to submit an application.

        # 2. Check that the Volunteer Opportunity exists
        #    and has status = "Active".
        #
        #    - Do not allow applications for inactive/closed
        #      opportunities.

        # 3. Validate the required application fields:
        #    - volunteer_opportunity
        #    - full_name
        #    - email
        #    - phone_number
        #    - privacy_consent

        # 4. Validate Preferred Available Days if provided.
        #    Allowed values:
        #    - Daily
        #    - Few times a week
        #    - Only on Weekends
        #    - Flexible

        # 5. Validate Privacy & Consent.
        #    - The user must provide consent before submitting
        #      the application.

        # 6. Create a new Volunteer Application document.

        # 7. Set the User field to the currently logged-in user.

        # 8. Set the Volunteer Opportunity field to the selected
        #    volunteer opportunity.

        # 9. Set the applicant profile fields:
        #    - Full Name
        #    - Email
        #    - Phone Number
        #    - Age
        #    - Gender

        # 10. Set the application fields:
        #     - Preferred Available Days
        #     - Why do you want to volunteer?
        #     - Privacy & Consent

        # 11. Insert the Volunteer Application document.

        # 12. Return the created application using the standard
        #     Result pattern.

        # 13. Return an appropriate success message.
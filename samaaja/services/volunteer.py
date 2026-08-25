class VolunteerManager:

    @staticmethod
    def get_list(
        limit=10,
        offset=0,
        location=None,
        category=None,
        skills_needed=None
    ):
        # Pseudocode:
        # 1. Build filters for the Volunteer Opportunity DocType.
        #    - Only fetch opportunities with Status = "Active".
        #    - Apply Location filter if provided.
        #    - Apply Category filter if provided.
        #    - Apply Skills Needed filter if provided.
        #
        # 2. Query the Volunteer Opportunity DocType using
        #    the appropriate Frappe database/query method.
        #
        # 3. Fetch the fields required for the opportunity cards:
        #    - name (system-generated document ID)
        #    - title
        #    - category
        #    - description
        #    - location
        #    - skills_needed
        #
        # 4. Resolve linked Category and Location information
        #    where required for the API response.
        #
        # 5. Handle the Skills Needed MultiSelect Table and return
        #    the selected skills.
        #
        # 6. Apply pagination using limit and offset.
        #
        # 7. Convert the records into the standard Result format.
        #
        # 8. Return the Result containing the matching opportunities.

        pass

    @staticmethod
    def get_by_id(volunteer_id):
        # Pseudocode:
        # 1. Find the Volunteer Opportunity using its
        #    system-generated document ID.
        #
        # 2. Fetch the fields required for the opportunity detail page:
        #    - name (system-generated document ID)
        #    - title
        #    - category
        #    - location
        #    - description
        #    - expected_time_commitment
        #    - start_date
        #    - end_date
        #    - volunteer_format
        #    - compensation_type
        #    - skills_needed
        #
        # 3. Resolve linked Category and Location information.
        #
        # 4. Handle the Skills Needed MultiSelect Table and return
        #    the selected skills.
        #
        # 5. If the opportunity does not exist, return an appropriate
        #    not-found Result/error response.
        #
        # 6. Convert the opportunity into the standard Result format.
        #
        # 7. Return the Result containing the opportunity details.
        pass
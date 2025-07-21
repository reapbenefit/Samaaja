import frappe
import json

def create_event_types():
    parent_types = ["Workshop / Seminar", "Awareness Drive", "Investigation/Audit", "Campaign"]

    for pt in parent_types:
        if not frappe.db.exists("Event Type", {"type": pt, "is_group": 1}):
            frappe.get_doc({
                "doctype": "Event Type",
                "type": pt,
                "is_group": 1
            }).insert()

    # Format: (child_type, parent_type)
    child_types = [
        ("Mentorship Session", "Workshop / Seminar"),
        ("Bootcamp", "Workshop / Seminar"),
        ("Teaching Session/ Course", "Workshop / Seminar"),
        ("Survey", "Awareness Drive"),
        ("Interview", "Awareness Drive"),
        ("Reading Material Distribution", "Awareness Drive"),
        ("Community Meeting", "Awareness Drive"),
        ("Incident Report", "Investigation/Audit"),
        ("Street Audits", "Investigation/Audit"),
        ("Community Activity", "Campaign"),
        ("Online Petition", "Campaign"),
        ("Volunteering work", "Campaign")
    ]

    for child, parent in child_types:
        if not frappe.db.exists("Event Type", {"type": child, "parent_event_type": parent}):
            frappe.get_doc({
                "doctype": "Event Type",
                "type": child,
                "is_group": 0,
                "parent_event_type": parent
            }).insert()

def create_event_categories_and_subcategories():
    # Define categories with icons and subcategories
    event_structure = {
        "Education & Awareness": {
            "icon": "https://static.thenounproject.com/png/7062467-512.png",  
            "sub_category": [
            "School Outreach",
            "Girl Education",
            "Teacher Training Program"
            ]
        },
        "Health & Sanitisation": {
            "icon": "https://static.thenounproject.com/png/2583590-512.png",  
            "sub_category": [
            "Health Camps",
            "Hygiene & Sanitation"
            ]
        },
        "Civic And Climate Action": {
            "icon": "https://static.thenounproject.com/png/1795959-512.png", 
            "sub_category": [
            "Pollution",
            "Waste Management",
            "Tree Planting & Reforestation"
            ]
        },
        "Livelihood & Skill Building": {
            "icon": "https://static.thenounproject.com/png/5517807-512.png",  
            "sub_category": [
            "Vocational Training",
            "Entrepreneurship Support",
            "Artisans Support System"
            ]
        },
        "Civic & Governance": {
            "icon": "https://static.thenounproject.com/png/1152481-512.png",  
            "sub_category": [
            "Civic Reporting",
            "Policy Engagement"
            ]
        }
        }

    for category, details in event_structure.items():
        # Insert Event Category if not exists
        if not frappe.db.exists("Event Category", {"category": category}):
            frappe.get_doc({
                "doctype": "Event Category",
                "category": category,
                "icon": details["icon"]
            }).insert()

        for subcat in details["sub_category"]:
            if not frappe.db.exists("Event Sub Category", {"subcategory": subcat}):
              frappe.get_doc({
                  "doctype": "Event Sub Category",
                  "subcategory": subcat
              }).insert()

def create_event_sources():
    sources = [
        "Social Media",
        "Whatsapp/Email/SMS",
        "Events",
        "Partner/ Alliance"
    ]

    for src in sources:
        if not frappe.db.exists("Event Source", {"source": src}):
            frappe.get_doc({
                "doctype": "Event Source",
                "source": src
            }).insert()

def create_badges_and_energy_point_rules():
    badges = [
        {
            "title": "Action Star",
            "icon": "1f9f1.svg",
            "description": "For completing your first ever activity on Samaaja",
            "subtypes": [
                "Mentorship Session", "Bootcamp", "Teaching Session/ Course", "Survey", "Interview",
                "Reading Material Distribution", "Community Meeting", "Incident Report",
                "Street Audits", "Community Activity", "Online Petition", "Volunteering work"
            ]
        },
        {
            "title": "Consistency Champion",
            "icon": "1f501.svg",
            "description": "For participating in 3+ activities in any sub-type within a 30-day period",
            "subtypes": [
                "Mentorship Session", "Bootcamp", "Teaching Session/ Course", "Survey", "Interview",
                "Reading Material Distribution", "Community Meeting", "Incident Report",
                "Street Audits", "Community Activity", "Online Petition", "Volunteering work"
            ]
        },
        {
            "title": "Conversation Starter",
            "icon": "1f4ac.svg",
            "description": "For initiating or contributing meaningfully in at least 3 community discussions",
            "subtypes": ["Community Meeting", "Interview", "Mentorship Session"]
        },
        {
            "title": "Collaboration Champion",
            "icon": "1f9e9.svg",
            "description": "For completing an activity in partnership with 2 or more users",
            "subtypes": ["Community Activity", "Teaching Session/ Course", "Bootcamp", "Volunteering work"]
        },
        {
            "title": "Impact Maker",
            "icon": "1f4c8.svg",
            "description": "For contributing to a campaign that crosses 100+ participants or signups",
            "subtypes": ["Online Petition", "Campaigns", "Awareness Drives"]
        },
        {
            "title": "Insight Seeker",
            "icon": "1f575.svg",
            "description": "For submitting data from 5+ surveys or reports",
            "subtypes": ["Survey", "Incident Report", "Street Audits"]
        },
        {
            "title": "Community Star",
            "icon": "1f31f.svg",
            "description": "For receiving 5 or more shout-outs or endorsements from peers",
            "subtypes": ["Volunteering work", "Mentorship Session", "Bootcamp", "Teaching Session/ Course", "Community Meeting"]
        },
        {
            "title": "Pathfinder",
            "icon": "1f9ed.svg",
            "description": "For guiding fellow changemakers with your lived experience and wisdom.",
            "subtypes": ["Mentorship Session"]
        },
        {
            "title": "Skill Sprinter",
            "icon": "1f6e0.svg",
            "description": "For completing an intensive hands-on bootcamp and leveling up your abilities.",
            "subtypes": ["Bootcamp"]
        },
        {
            "title": "Community Educator",
            "icon": "1f4da.svg",
            "description": "For sharing knowledge through structured learning sessions or community teaching.",
            "subtypes": ["Teaching Session/ Course"]
        },
        {
            "title": "Citizen Researcher",
            "icon": "1f4dd.svg",
            "description": "For collecting data that supports grassroots decision-making.",
            "subtypes": ["Survey"]
        },
        {
            "title": "Voice Amplifier",
            "icon": "1f399.svg",
            "description": "For capturing and sharing real community stories and insights.",
            "subtypes": ["Interview"]
        },
        {
            "title": "Knowledge Carrier",
            "icon": "1f4d6.svg",
            "description": "For helping spread awareness through distributing informative material.",
            "subtypes": ["Reading Material Distribution"]
        },
        {
            "title": "Dialogue Driver",
            "icon": "1f5e3.svg",
            "description": "For organizing or contributing to meaningful community discussions.",
            "subtypes": ["Community Meeting"]
        },
        {
            "title": "Issue Spotter",
            "icon": "1f6a8.svg",
            "description": "For flagging civic or community issues that need attention.",
            "subtypes": ["Incident Report"]
        },
        {
            "title": "Street Scanner",
            "icon": "1f3d9.svg",
            "description": "For conducting or leading audits in public spaces like roads, markets, or parks.",
            "subtypes": ["Street Audits"]
        },
        {
            "title": "Community Catalyst",
            "icon": "1f91d.svg",
            "description": "For organizing or participating in local collective action.",
            "subtypes": ["Community Activity"]
        },
        {
            "title": "Digital Advocate",
            "icon": "270d.svg",
            "description": "For launching or supporting issue-based petitions to drive policy change.",
            "subtypes": ["Online Petition"]
        },
        {
            "title": "Everyday Hero",
            "icon": "1f4aa.svg",
            "description": "For putting your time and heart into volunteering that supports social change.",
            "subtypes": ["Volunteering work"]
        }
    ]

    for badge in badges:
        # Create Badge
        if not frappe.db.exists("Badge", {"title": badge["title"]}):
            doc = frappe.new_doc("Badge")
            doc.title = badge["title"]
            doc.icon = f"/assets/samaaja/images/{badge['icon']}"
            doc.description = badge["description"]
            doc.badge_type = "Skill"
            doc.active=1
            doc.insert()
            frappe.db.commit()
           
        # Create Energy Point Rule
        if not frappe.db.exists("Energy Point Rule", {"name": badge["title"]+" Rule"}):
            rule = frappe.new_doc("Energy Point Rule")
            rule.rule_name = badge["title"]+" Rule"
            rule.reference_doctype = "Events"
            rule.user_field = "user"
            rule.subject = f"Earned {badge['title']} badge!"
            rule.for_doc_event = "Custom"
            rule.points = 5

            if badge.get("subtypes"):
                subtype_list = badge["subtypes"]
                quoted = ", ".join([f"'{s}'" for s in subtype_list])
                rule.condition = f"doc.sub_type in [{quoted}]"
            rule.apply_only_once = 1
            rule.badge = badge.get("title")
            try:
                rule.insert()
                frappe.db.commit()
            except Exception as e:
                print(f"Failed to insert rule for badge: {badge['title']}. Error: {e}")

def enable_energy_points():
    ss = frappe.get_single("Energy Point Settings")
    ss.enable_energy_points = 1  # ✅ Enable Energy Points
    ss.save()
    frappe.db.commit()

def create_users():
    user_data = [
        {"first_name": "Ayesha", "full_name": "Ayesha Khan", "email": "ayesha@samaaja.org", "age": 22, "gender": "Female", "city": "Lucknow", "state": "Uttar Pradesh"},
        {"first_name": "Rohan", "full_name": "Rohan Mehta", "email": "rohan@samaaja.org", "age": 29, "gender": "Male", "city": "Ahmedabad", "state": "Gujarat"},
        {"first_name": "Sneha", "full_name": "Sneha Reddy", "email": "sneha@samaaja.org", "age": 19, "gender": "Female", "city": "Hyderabad", "state": "Telangana"},
        {"first_name": "Aditya", "full_name": "Aditya Sharma", "email": "aditya@samaaja.org", "age": 34, "gender": "Male", "city": "New Delhi", "state": "Delhi"},
        {"first_name": "Priya", "full_name": "Priya Menon", "email": "priya@samaaja.org", "age": 27, "gender": "Female", "city": "Kochi", "state": "Kerala"},
        {"first_name": "Kabir", "full_name": "Kabir Singh", "email": "kabir@samaaja.org", "age": 21, "gender": "Male", "city": "Mohali", "state": "Punjab"},
        {"first_name": "Meera", "full_name": "Meera Banerjee", "email": "meera@samaaja.org", "age": 31, "gender": "Female", "city": "Kolkata", "state": "West Bengal"},
        {"first_name": "Aniket", "full_name": "Aniket Joshi", "email": "aniket@samaaja.org", "age": 25, "gender": "Male", "city": "Pune", "state": "Maharashtra"},
        {"first_name": "Iqra", "full_name": "Iqra Sheikh", "email": "iqra@samaaja.org", "age": 18, "gender": "Female", "city": "Bhopal", "state": "Madhya Pradesh"},
        {"first_name": "Harshad", "full_name": "Harshad Iyer", "email": "harshad@samaaja.org", "age": 30, "gender": "Male", "city": "Bengaluru", "state": "Karnataka"},
    ]

    for u in user_data:
        # Ensure city exists in Samaaja Cities
        if not frappe.db.exists("Samaaja Cities", {"city_name": u["city"]}):
            city_doc = frappe.get_doc({
                "doctype": "Samaaja Cities",
                "city_name": u["city"],
                "state": u["state"]  # assuming Samaaja Cities has a "state" field too
            })
            city_doc.insert(ignore_permissions=True)
            frappe.db.commit()

        # Create User if not exists
        if not frappe.db.exists("User", u["email"]):
            user = frappe.get_doc({
                "doctype": "User",
                "email": u["email"],
                "first_name": u["first_name"],
                "full_name": u["full_name"],
                "gender": u["gender"],
                "send_welcome_email": 0,
                "new_password": "samaaja@123"
            })
            user.insert(ignore_permissions=True)
            frappe.db.commit()
            
        if not frappe.db.exists("User Metadata", u["email"]):
            # Create User Metadata
            meta = frappe.get_doc({
                "doctype": "User Metadata",
                "user": u["email"],
                "city": u["city"],
                "state": u["state"]
            })
            meta.insert(ignore_permissions=True)
            frappe.db.commit()

def create_events():
    events = [
        {"user": "ayesha@samaaja.org", "title": "Parents’ Roundtable", "description": "Parents’ Roundtable", "category": "Education & Awareness", "subcategory": "Girl Education", "event_type": "Awareness Drive", "subtype": "Community Meeting", "hours": 1},
        {"user": "rohan@samaaja.org", "title": "Road Safety Survey", "description": "Road Safety Survey", "category": "Civic & Governance", "subcategory": "Civic Reporting", "event_type": "Investigation/Audit", "subtype": "Street Audits", "hours": 2},
        {"user": "aditya@samaaja.org", "title": "Tailoring for Beginners Bootcamp", "description": "Tailoring for Beginners Bootcamp", "category": "Livelihood & Skill Building", "subcategory": "Vocational Training", "event_type": "Workshop / Seminar", "subtype": "Mentorship Session", "hours": 2},
        {"user": "priya@samaaja.org", "title": "Anemia Screening for Women", "description": "Anemia Screening for Women", "category": "Health & Sanitisation", "subcategory": "Health Camps", "event_type": "Awareness Drive", "subtype": "Survey", "hours": 3},
        {"user": "kabir@samaaja.org", "title": "Rainwater Harvesting Workshop", "description": "Rainwater Harvesting Workshop", "category": "Civic And Climate Action", "subcategory": "Pollution", "event_type": "Awareness Drive", "subtype": "Interview", "hours": 4},
        {"user": "meera@samaaja.org", "title": "Plastic Waste Clean-up Drive", "description": "Plastic Waste Clean-up Drive", "category": "Civic And Climate Action", "subcategory": "Waste Management", "event_type": "Campaign", "subtype": "Community Activity", "hours": 1},
        {"user": "aniket@samaaja.org", "title": "Urban School Campus Greening", "description": "Urban School Campus Greening", "category": "Civic And Climate Action", "subcategory": "Tree Planting & Reforestation", "event_type": "Campaign", "subtype": "Community Activity", "hours": 2},
        {"user": "harshad@samaaja.org", "title": "Career Awareness Session", "description": "Career Awareness Session", "category": "Education & Awareness", "subcategory": "School Outreach", "event_type": "Workshop / Seminar", "subtype": "Mentorship Session", "hours": 2},
        {"user": "sneha@samaaja.org", "title": "Community Tree Plantation", "description": "Community Tree Plantation", "category": "Civic And Climate Action", "subcategory": "Tree Planting & Reforestation", "event_type": "Campaign", "subtype": "Community Activity", "hours": 1},
    ]

    for e in events:
        if not frappe.db.exists("Events", {"title": e["title"]}):
            doc = frappe.get_doc({
                "doctype": "Events",
                "title": e["title"],
                "description": e["description"],
                "category": e["category"],
                "subcategory": e["subcategory"],
                "type": e["event_type"],
                "sub_type": e["subtype"],
                "hours_invested": e["hours"],
                "user": e["user"]
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            doc.save(ignore_permissions=True)

def create_campaign_templates():
    data = [
        {
            "title": "Clean-Up Drive",
            "header_logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTb89_HRfrOIehYifLckaAT8CgX5SU6jDigZg&s",
            "email_subject_template": "Join the Clean-Up Drive for a Greener Tomorrow!",
            "email_body_template": "Let’s come together for a community clean-up. Join hands to make our parks, roads, and riversides clean and green again. Participate in the drive, bring your friends, and let’s make a visible difference together.",
            "recipient_name": "Rahul Poddar",
            "recipient_email": "rahul@impactyaan.com",
            "route": "campaign/clean-up-drive",
            "partner": "Reap Benefit",
            "logo": "https://media.licdn.com/dms/image/v2/D560BAQHLz7j54BE1-Q/company-logo_200_200/company-logo_200_200/0/1709957751243?e=2147483647&v=beta&t=APWWYHiiyk6J5uWs3hlljeyDo9ihZRJYzTK_kz8Tz9g"
        },
        {
            "title": "Cleanliness & Hygiene Awareness",
            "header_logo": "https://www.sterloc.com/blog/wp-content/uploads/2021/11/cleanliness-and-hygiene.jpg",
            "email_subject_template": "Clean Hands, Safe Homes: Hygiene Awareness Drive",
            "email_body_template": "Access to sanitation and hygiene education saves lives. Be part of our community campaign promoting healthy hygiene habits, distributing kits, and conducting interactive handwashing demos in schools and households. Volunteer with us and help build a healthier tomorrow.",
            "recipient_name": "Ankit Saxena",
            "recipient_email": "ankit@impactyaan.com",
            "route": "campaign/cleanliness-hygiene-awareness",
            "partner": "Impactyaan",
            "logo": "https://media.licdn.com/dms/image/v2/D560BAQG0XJIGaxZqcg/company-logo_100_100/B56ZaMIcyuHUAQ-/0/1746107747953/impactyaan_logo?e=2147483647&v=beta&t=OvbPqig2XHpCILlRSx6BPxFAcN76Yu3AKI3V6Z1W8GE"
        },
        {
            "title": "Tree Planting & Reforestation",
            "header_logo": "https://dva1blx501zrw.cloudfront.net/uploaded_images/us/images/2443/original/shutterstock_604290230.jpg",
            "email_subject_template": "Plant for the Planet: One Tree, One Future",
            "email_body_template": "Urban and rural green cover is vanishing—but we can reverse that. Join our Tree Planting campaign focused on native species, local biodiversity, and community ownership. Lend your hands to the soil—let’s root change together.",
            "recipient_name": "Pranav Prabhu",
            "recipient_email": "pranav@oasishq.org",
            "route": "campaign/tree-plantation-reforestation",
            "partner": "Oasis",
            "logo": "https://oasishq.org/assets/oasis/images/logo.svg"
        }
    ]

    for entry in data:
        if not frappe.db.exists("Campaign Template", {"title": entry["title"]}):

          doc = frappe.get_doc({
              "doctype": "Campaign Template",
              "title": entry["title"],
              "header_logo": entry["header_logo"],
              "email_subject_template": entry["email_subject_template"],
              "email_body_template": entry["email_body_template"],
              "published": 1,
              "accept_petitions": 1,
              "organization_name": "Samaaja",
              "route": entry["route"],
              "recipients": [
                  {
                      "doctype": "Campaign Recipient",
                      "recipient_name": entry["recipient_name"],
                      "email": entry["recipient_email"],
                      "is_selected_by_default": 1
                  }
              ],
              "partners": [
                  {
                      "doctype": "Campaign Partner",
                      "partner_name": entry["partner"],
                      "logo": entry["logo"]
                  }
              ]
          })

          doc.insert(ignore_permissions=True)

          frappe.db.commit()

def create_print_format():
    if not frappe.db.exists("Print Format", {"name": "User Profile"}):
        html = """
       <div class="hidden">
    {% set actions = frappe.get_all("Events", {"user": doc.name}, page_length=1, order_by="creation desc", pluck="creation") %}
    {% set all_actions = frappe.get_all("Events", {"user": doc.name}, pluck="hours_invested") %}
    {% set highlight = frappe.get_all("Events", {"user": doc.name, "highlight": 1}, page_length=1, pluck="description") %}
    {% set user_event_details_category = frappe.db.get_all('Events', fields=['count(name) as count', 'category'], filters={"user": doc.name}, group_by='category', order_by='count desc', page_length=3) %}
    {% set user_badges = frappe.db.get_all('User badge', filters={'user':doc.name},pluck='badge') %}
    {% set reviews = frappe.get_all("User Review", {"user": doc.name}, ["review_title", "reviewer_name", "designation", "comment", "organisation"], page_length=3) %}
    {% set superhero = [] %}
    {% set skills = [] %}
    {% set partners = [] %}
    {% set qr = frappe.get_doc("User Profile QR", doc.name) %}
    {% for badge in user_badges %}
        {% set badge = frappe.get_doc('Badge', badge) %}
        {% if badge.badge_type == 'Skill' %}
            {{ skills.append({"name": badge.title, "image": badge.icon}) }}
        {% endif %}
        {% if 'Partners' in badge_tags %}
            {{ partners.append({"name": badge.title, "image": badge.icon}) }}
        {% endif %}
    {% endfor %}
    {% for cat in user_event_details_category %}
        {% set cat = frappe.get_doc('Event Category', cat.category) %}
            {{ superhero.append({"name": cat.name, "image": cat.icon}) }}
    {% endfor %}
</div>
<div class="lb_wrapper_outer">
        <div class="lb_wrapper">
          <div class="lb_section_left">
            <div class="lb_left_content">
                <div class="user_badge">
                {% if doc.user_image %}
                    <img src="{{frappe.utils.get_url()}}{{ doc.user_image }}" title="{{ doc.full_name }}" />
                {% else %}
                    <img src="https://secure.gravatar.com/avatar/72810bb8f925ab4eae9a3e0b2f681fa5?d=mm&s=200" title="{{ doc.full_name }}" />
                {% endif %}
            </div>
              <div class="user_detail">
                <h3>{{ doc.full_name }}</h3>
                {% if doc.city %}
                    <p>
                      <svg viewBox="0 0 20 20">
                        <path
                          fill="#51A76A"
                          d="M10,1.375c-3.17,0-5.75,2.548-5.75,5.682c0,6.685,5.259,11.276,5.483,11.469c0.152,0.132,0.382,0.132,0.534,0c0.224-0.193,5.481-4.784,5.483-11.469C15.75,3.923,13.171,1.375,10,1.375 M10,17.653c-1.064-1.024-4.929-5.127-4.929-10.596c0-2.68,2.212-4.861,4.929-4.861s4.929,2.181,4.929,4.861C14.927,12.518,11.063,16.627,10,17.653 M10,3.839c-1.815,0-3.286,1.47-3.286,3.286s1.47,3.286,3.286,3.286s3.286-1.47,3.286-3.286S11.815,3.839,10,3.839 M10,9.589c-1.359,0-2.464-1.105-2.464-2.464S8.641,4.661,10,4.661s2.464,1.105,2.464,2.464S11.359,9.589,10,9.589"
                        ></path>
                      </svg>
    
                      <span>{{ doc.city }}</span>
                    </p>
                {% endif %}
                {% if doc.verified_by %}
                        <p>
                            <div class="verified_profile">
<svg id="Layer_1" data-name="Layer 1" viewBox="0 0 122.88 116.87"><polygon fill="#00ade9" points="61.37 8.24 80.43 0 90.88 17.79 111.15 22.32 109.15 42.85 122.88 58.43 109.2 73.87 111.15 94.55 91 99 80.43 116.87 61.51 108.62 42.45 116.87 32 99.08 11.73 94.55 13.73 74.01 0 58.43 13.68 42.99 11.73 22.32 31.88 17.87 42.45 0 61.37 8.24 61.37 8.24"/><path fill="#ffffff" d="M37.92,65c-6.07-6.53,3.25-16.26,10-10.1,2.38,2.17,5.84,5.34,8.24,7.49L74.66,39.66C81.1,33,91.27,42.78,84.91,49.48L61.67,77.2a7.13,7.13,0,0,1-9.9.44C47.83,73.89,42.05,68.5,37.92,65Z"/></svg>
                                <span>Verified Change Maker</span>
                            </div>
                        </p>
                {% endif %}
              </div>
              <div class="user_stats">
                <div class="user_stats_item">
                  <strong>Hours Invested</strong>
                  <span>{{ frappe.utils.flt(sum(all_actions)) }}</span>
                </div>
                <div class="user_stats_item">
                  <strong>Actions Taken</strong>
                  <span>{{ all_actions|length }}</span>
                </div>
              </div>

                {% if doc.bio %}
                    <div class="user_bio">
                        <h4>Bio</h4>
                        <p>
                          {{ doc.bio }}
                        </p>
                    </div>
                {% endif %}
              <div class="qr_scan">
                <p>To see the profile scan the code below:</p>
                <div class="qr_code">
                  <img
                    src="{{frappe.utils.get_url()}}{{ qr.qr }}"
                    alt=""
                  />
                </div>
              </div>
            </div>
          </div>
          <div class="lb_section_right">
            {% if skills %}
            <div class="skill-badges">
              <div class="title">Skill Badges</div>
              <div class="badges-wrapper">
                {% for skill in skills %}
                    <div class="badge">
                      <img src="{{frappe.utils.get_url()}}{{ skill.image }}" alt="" />
                      <span>{{ skill.name }}</span>
                    </div>
                {% endfor %}
              </div>
            </div>
            {% endif %}
            <div class="tabs-wrapper">
              <div class="title">Overview</div>
              <div class="tabs_content panels">
                <div class="overview_content panel">
                    <div class="hidden">
                        {% if highlight %}
                        <fieldset class="profile_fieldset">
                            <legend>Highlight</legend>
                            <p>{{ highlight[0] }}</p>
                        </fieldset>
                        {% endif %}    
                    </div>
                    {% if superhero %}
                        <fieldset class="profile_fieldset">
                            <legend>Interested in</legend>
                            <div class="shf_items">
                                {% for superhe in superhero %}
                                <div class="item">
                                    <img src="{{frappe.utils.get_url()}}{{ superhe.image }}" alt="" />
                                    <span>{{ superhe.name }}</span>
                                </div>
                                {% endfor %}
                            </div>
                        </fieldset>
                    {% endif %}
                    {% if reviews %}
                      <fieldset class="profile_fieldset profile_fieldset100" style="padding: 16px 16px 0">
                        <legend>Expert Review</legend>
                        <div class="expert_review">
                          <div class="content">
                            {% for review in reviews %}
                                <p>
                                  {{ review.comment }}
                                </p>
                                <strong>{{review.reviewer_name}}, {{review.designation}} {{review.organisation}}</strong>
                            {% endfor %}
                          </div>
                        </div>
                      </fieldset>
                    {% endif %}
                  {% if partners %}
                  <fieldset class="profile_fieldset profile_fieldset100">
                        <legend>Partners/Supporters</legend>
                        <div class="partners_wrapper">
                            {% for partner in partners %}
                                <div class="partners_content">
                                    <img src="{{frappe.utils.get_url()}}{{ partner.image }}" alt=""/>
                                </div>
                            {% endfor %}
                        </div>
                  </fieldset>
                  {% endif %}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
        """
        css = """
            .lb_wrapper_outer {
        width: 100%;
        background: linear-gradient(
          180deg,
          rgba(232, 255, 238, 0) 5.73%,
          #e8ffee 23.44%,
          #e7f5ff 100%
        );
      }
      .lb_wrapper {
        width: 100%;
        max-width: 1440px;
        padding: 25px 32px 55px;
        margin: 0 auto;
        box-sizing: border-box;
        display: flex;
        justify-content: space-between;
      }
      .lb_section_left {
        width: 40%;
      }
      .user_badge {
        width: 50px;
        height: 50px;
        margin: 0 auto;
        border-radius: 50%;
        overflow: hidden;
        position: relative;
        z-index: 100;
      }
      .user_badge img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      .lb_left_content {
        width: 100%;
        background: #fff;
        box-shadow: 4px 8px 30px 0px rgba(0, 0, 0, 0.12);
        border-radius: 32px;
        position: relative;
        z-index: 99;
        padding: 15px 0 0;
      }
      .edit_cta {
        position: absolute;
        top: 18px;
        right: 18px;
      }
      .edit_cta svg {
        width: 24px;
        height: 24px;
      }
      .user_detail{
        padding: 0 16px;
      }
      .user_detail h3 {
        margin: 0;
        font-size: 20px;
        font-weight: 700;
        color: #2b4754;
        text-align: center;
      }
      .user_detail p {
        margin: 8px 0 0;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #2b4754;
        font-size: 12px;
        font-weight: 400;
      }
      .user_detail svg {
        width: 16px;
        height: 16px;
        margin-right: 4px;
      }
      .last_activity {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 15px 0 0;
        padding: 0 16px;
        font-size: 12px;
      }
      .last_activity svg {
        width: 16px;
        height: 16px;
        margin-right: 5px;
      }
      .user_stats {
        background: #51a76a;
        padding: 6px 32px;
        margin: 17px 0 0;
        display: flex;
      }
      .user_stats_item {
        width: 50%;
        padding: 0 12px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border-right: 1px solid #fff;
        box-sizing: border-box;
        text-align: center;
      }
      .user_stats_item:last-child {
        border-right: 0;
      }
      .user_stats_item strong {
        color: #2b4754;
        font-size: 12px;
        font-weight: 700;
      }
      .user_stats_item span {
        color: #fff;
        font-size: 16px;
        font-weight: 700;
      }
      .user_bio {
        padding: 20px 16px;
      }
      .user_bio h4 {
        margin: 0;
        padding: 0;
        color: #2b4754;
        font-size: 16px;
        font-weight: 700;
      }
      .user_bio p {
        margin: 8px 0 0;
        color: #2b4754;
        font-size: 12px;
        font-weight: 400;
      }
      .qr_scan{
        padding: 0 16px 20px;
      }
      .qr_scan p {
        color: #e59735;
        font-size: 12px;
        text-align: center;
      }
      .qr_code img {
        width: 100%;
      }
      .ctas_wrapper {
        padding: 48px 32px 0;
      }
      .btn {
        width: 100%;
        margin-bottom: 16px;
        background: transparent;
        outline: 0;
        padding: 18px 0;
        border-radius: 32px;
        box-sizing: border-box;
        font-size: 20px;
        font-weight: 700;
      }
      .btn_fill {
        background-color: #52a769;
        color: #fff;
        border: 0;
      }
      .btn_outline {
        color: #51a76a;
        border: 2px solid #51a76a;
      }
      .report_user {
        padding: 16px 0 32px;
        text-align: center;
      }
      .report_user a {
        color: #51a76a;
        font-size: 16px;
        text-decoration: none;
      }
      .lb_section_right {
        width: 58%;
      }
      .skill-badges {
        width: 100%;
        background: #fff;
        box-shadow: 4px 8px 30px 0px rgba(0, 0, 0, 0.12);
        padding: 15px 20px 0px;
        border-radius: 32px;
      }
      .profile_content .skill-badges {
        display: none;
      }
      .skill-badges .title {
        font-size: 16px;
        font-weight: 700;
        color: #2b4754;
      }
      .badges-wrapper {
        margin: 20px 0 0;
        display: flex;
        justify-content: flex-start;
        flex-wrap: wrap;
      }
      .badge {
        min-width: 18%;
        width: 30%;
        margin: 0 1% 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        border: 0;
        background-color: transparent !important;
      }
      .badge img {
        width: 40px;
      }
      .badge span {
        font-size: 11px;
        font-weight: 400;
        color: #2b4754;
        line-height: 1.3;
        white-space: break-spaces;
      }
      .badge small {
        font-size: 14px;
        font-weight: 600;
        color: #d85930;
        margin: 4px 0 0;
      }
      .tabs-wrapper {
        width: 100%;
        background: #fff;
        box-shadow: 4px 8px 30px 0px rgba(0, 0, 0, 0.12);
        padding: 15px 20px 0;
        margin: 24px 0 0;
        border-radius: 32px;
      }
      .tabs-wrapper .title{
        font-size: 16px;
        font-weight: 700;
        color: #2b4754;
      }
      .panels .panel {
        display: none;
      }
      .panels .panel:first-child {
        display: flex;
      }
      .overview_content {
        margin: 10px 0 0;
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
      }
      .overview_content fieldset {
        border-radius: 32px;
        border: 1px solid #edb550;
      }
      .overview_content legend {
        color: #51a76a;
        font-size: 16px;
        font-weight: 700;
        width: auto;
        padding: 0 8px;
        margin: 0;
      }
      .profile_fieldset {
        width: 100%;
        padding: 16px;
        margin: 0 0 16px;
        box-sizing: border-box;
      }
      .profile_fieldset h3 {
        padding: 0;
        margin: 0;
        color: #2b4754;
        font-size: 23px;
        font-weight: 700;
      }
      .profile_fieldset p {
        margin: 5px 0 0;
        color: #2b4754;
        font-size: 11px;
        font-weight: 400;
      }
      .shf_items {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
      }
      .shf_items .item {
        display: flex;
        flex-direction: column;
        align-items: center;
      }
      .shf_items .item span {
        font-size: 11px;
        white-space: break-spaces;
      }
      .shf_items .item img {
        width: 40px;
        margin: 0 0 4px;
      }
      .persona_content {
        display: flex;
        justify-content: flex-start;
        align-items: center;
      }
      .persona_content img {
        width: 212px;
      }
      .persona_content .content {
        margin: 0 0 0 60px;
      }
      .persona_content .content strong {
        color: #e59735;
        font-size: 20px;
        font-weight: 700;
        margin: 0 0 12px;
      }
      .persona_content .content p {
        margin: 0 0 24px;
      }
      .persona_content .content ul {
        padding: 0;
        margin: 12px 0 0 20px;
      }
      .expert_review .content p {
        margin: 0;
      }
      .expert_review .content strong {
        color: #e59735;
        font-size: 12px;
        font-weight: 600;
        margin: 0 0 10px;
        display: inline-block;
      }
      .partners_wrapper {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        flex-wrap: wrap;
      }
      .partners_content {
        display: flex;
        align-items: center;
        margin: 0 10px 10px 0;
      }
      .partners_content img {
        margin-right: 10px;
        width: 50px;
      }
      .sign-designation {
        display: flex;
        flex-direction: column;
      }
      .sign-designation strong {
        color: #e59735;
        font-size: 20px;
        font-weight: 600;
      }
      .sign-designation p {
        font-size: 16px;
        font-weight: 600;
      }
      .action_item {
        border-bottom: 1px solid #786b5a;
        padding: 24px 18px 0;
      }
      .action_item:last-child {
        border-bottom: 0;
        padding-bottom: 24px;
      }
      .action_item_head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 0 24px;
      }
      .action_item_head a {
        color: #2b4754;
      }
      .action_item h3 {
        margin: -14px 0 10px;
        padding: 0;
        color: #2b4754;
        font-size: 24px;
        font-weight: 700;
        display: flex;
        justify-content: flex-start;
        align-items: center;
      }
      .action_item p svg {
        width: 20px;
        height: 20px;
      }
      .action_item_head p {
        color: #2b4754;
        font-size: 16px;
        font-weight: 400;
        display: flex;
        align-items: center;
        margin: 0;
      }
      .action_item_head svg {
        width: 20px;
        height: 20px;
        margin: 0 4px 0 0;
      }
      .dropdown-menu.show {
        right: 0 !important;
        left: inherit !important;
        top: 25px !important;
        transform: none !important;
      }
      .action_content {
        padding: 20px 0;
      }
      .verified_profile {
        font-size: 12px;
        font-weight: 600;
        color: #666666;
        text-align: center;
        padding: 0 15px;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .verified_profile svg,
      .vouched_by svg {
        width: 25px;
        height: 25px;
        margin-right: 4px;
      }
      .vouched_by svg {
        flex-shrink: 0;
        margin-top: 3px;
      }
      .vouched_by {
        font-size: 22px;
        font-weight: 600;
        color: #51a76a;
        display: flex;
        align-items: flex-start;
        justify-content: center;
        margin-left: 10px;
      }
        """
        print_format = frappe.get_doc({
            "doctype": "Print Format",
            "name": "User Profile",
            "doc_type": "User",
            "module": "Core",
            "custom_format": 1,
            "html": html,
            "css":css,
            "print_format_type":"Jinja"
        })

        print_format.insert(ignore_permissions=True)
        frappe.db.commit()

def create_discussions_web_page():
    if frappe.db.exists("Web Page", "discussions"):
        print("Web Page already exists.")
        return

    doc = frappe.get_doc({
        "doctype": "Web Page",
        "title": "Discussions",
        "route": "discussions",
        "published": 1,
        "content_type": "Page Builder",
        "full_width": 1,
        "show_title": 0,
        "show_sidebar": 0,
        "enable_comments": 0,
        "page_blocks": [
            {
                "doctype": "Web Page Block",
                "web_template": "Discussions",
                "web_template_values": json.dumps({
                    "title": "Samaaja conversations",
                    "cta_title": "New conversation",
                    "docname": "discussions",
                    "single_thread": 0
                }),
                "add_container": 1,
                "add_top_padding": 1,
                "add_bottom_padding": 1
            }
        ]
    })

    doc.insert(ignore_permissions=True)
    frappe.db.commit()

def create_sample_discussions():
    titles = [
        "How can civic engagement improve local governance?",
        "Innovative methods to increase girl education enrollment?",
        "What’s your opinion on tree planting initiatives?",
        "How can vocational training be more inclusive?",
        "Is policy advocacy working at the grassroots level?"
    ]

    replies = [
        "Great question! In our area, regular ward meetings helped.",
        "We used peer mentors and that really boosted attendance.",
        "I’ve seen mixed results, but engaging communities helps.",
        "Yes, especially when tied to local job markets.",
        "Grassroots voices are rising, but more training is needed."
    ]

    for i in range(5):
        title = titles[i]
        reply_text = replies[i]

        # Check if Discussion Topic with this title already exists
        existing_topic = frappe.db.exists("Discussion Topic", {"title": title})
        
        if not existing_topic:
            # Create Discussion Topic
            topic = frappe.get_doc({
                "doctype": "Discussion Topic",
                "title": title,
                "reference_doctype": "Web Page",
                "reference_docname": "discussions",
                "owner":"kabir@samaaja.org"
            }).insert(ignore_permissions=True)

            # Create Discussion Reply linked to the topic
            frappe.get_doc({
                "doctype": "Discussion Reply",
                "topic": topic.name,
                "reply": reply_text,
                "owner":"sneha@samaaja.org"
            }).insert(ignore_permissions=True)

            frappe.db.commit()

def website_settings():
    settings = frappe.get_single("Website Settings")
    settings.home_page = "leaderboard"
    settings.banner_image = "/assets/samaaja/images/Samaaja.png"
    settings.save()
    frappe.db.commit()

def create_samaaja_settings():
    # Sample data — update as needed
    data = {
        "samaaja_icon":"/assets/samaaja/images/Samaaja.png",
        "tagline": "Samaaja: Where Changemakers Grow Together",
        "blurb": "#GrowWithSamaaja",
        "summary": "An open-source platform for non-profits to design, activate, and scale changemaker communities",
        "join_title": "",
        "join_link": "/discussions",
        "join_conversations_title":"Join Samaaja Conversations",
        "join_conversations_link":"/raven",
        "join_forum_link":"/discussions",
        "join_forum_title":"Join Samaaja Forum",
        "total_members_label": "Total Members",
        "actions_taken_label": "Actions Taken",
        "hours_invested_label": "Hours Invested",
        "verified_members_label": "Verified Members",
        "verified_members_summary": "Members who have been vetted and verified.",
        "most_active_members_label": "Most Active Members",
        "most_active_members_summary": "Top contributors who lead the change.",
        "most_active_cities_label": "Most Active Cities",
        "most_active_cities_summary": "Cities showing the greatest participation.",

        "samaaja_feature_list": [
            {
                "feature_name": "Dynamic Portfolio",
                "icon": "/assets/samaaja/images/build_skills.png"
            },
            {
                "feature_name": "Leaderboards",
                "icon": "/assets/samaaja/images/access_mentorship.png"
            },
            {
                "feature_name": "Build Expertise",
                "icon": "/assets/samaaja/images/land_internships.png"
            },
            {
                "feature_name": "Funding Opportunities",
                "icon": "/assets/samaaja/images/seeds_funds.png"
            }
        ]
    }

    # Load the single doc (or create if doesn't exist — handled by frappe.get_single)
    doc = frappe.get_single("Samaaja Settings")

    # Set scalar fields
    for field, value in data.items():
        if field != "samaaja_feature_list":
            doc.set(field, value)

    # Clear and set feature list (child table)
    doc.set("samaaja_feature_list", [])
    for feature in data["samaaja_feature_list"]:
        doc.append("samaaja_feature_list", {
            "feature_name": feature["feature_name"],
            "icon": feature["icon"]
        })

    # Save the document
    doc.save(ignore_permissions=True)
    frappe.db.commit()


@frappe.whitelist()
def setup_samaaja():
    print("🔥 Setting up samaaja")
    create_event_types()
    create_event_categories_and_subcategories()
    create_event_sources()
    create_badges_and_energy_point_rules()
    enable_energy_points()
    create_users()
    create_events()
    create_campaign_templates()
    create_print_format()
    create_discussions_web_page()
    create_sample_discussions()
    website_settings()
    create_samaaja_settings()
    print("🔥 Setting up samaaja successful!")
    frappe.msgprint("Samaaja setup completed successfully.")


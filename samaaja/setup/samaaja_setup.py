import frappe

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
    # Define categories and their corresponding subcategories
    event_structure = {
        "Education & Awareness": [
            "School Outreach",
            "Girl Education",
            "Teacher Training Program"
        ],
        "Health & Sanitisation": [
            "Health Camps",
            "Hygiene & Sanitation"
        ],
        "Civic And Climate Action": [
            "Pollution",
            "Waste Management",
            "Tree Planting & Reforestation"
        ],
        "Livelihood & Skill Building": [
            "Vocational Training",
            "Entrepreneurship Support",
            "Artisans Support System"
        ],
        "Civic & Governance": [
            "Civic Reporting",
            "Policy Engagement"
        ]
    }

    for category, subcategories in event_structure.items():
        # Insert Event Category if not exists
        if not frappe.db.exists("Event Category", {"category": category}):
            frappe.get_doc({
                "doctype": "Event Category",
                "category": category
            }).insert()

        for subcat in subcategories:
            # Insert Event Sub Category if not exists
            if not frappe.db.exists("Event Sub Category", {
                "subcategory": subcat,
                "event_category": category
            }):
                frappe.get_doc({
                    "doctype": "Event Sub Category",
                    "subcategory": subcat,
                    "event_category": category
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
        if not frappe.db.exists("Energy Point Rule", {"name": badge["title"]+" Eb Rule"}):
            rule = frappe.new_doc("Energy Point Rule")
            rule.rule_name = badge["title"]+" Eb Rule"
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
    ss = frappe.get_single("System Settings")
    ss.enable_energy_points = 1  # ✅ Enable Energy Points
    ss.save()
    frappe.db.commit()

def create_users():
    user_data = [
        {"first_name": "Ayesha", "full_name": "Ayesha Khan", "email": "Ayesha@samaaja.org", "age": 22, "gender": "Female", "city": "Lucknow", "state": "Uttar Pradesh"},
        {"first_name": "Rohan", "full_name": "Rohan Mehta", "email": "Rohan@samaaja.org", "age": 29, "gender": "Male", "city": "Ahmedabad", "state": "Gujarat"},
        {"first_name": "Sneha", "full_name": "Sneha Reddy", "email": "Sneha@samaaja.org", "age": 19, "gender": "Female", "city": "Hyderabad", "state": "Telangana"},
        {"first_name": "Aditya", "full_name": "Aditya Sharma", "email": "Aditya@samaaja.org", "age": 34, "gender": "Male", "city": "New Delhi", "state": "Delhi"},
        {"first_name": "Priya", "full_name": "Priya Menon", "email": "Priya@samaaja.org", "age": 27, "gender": "Female", "city": "Kochi", "state": "Kerala"},
        {"first_name": "Kabir", "full_name": "Kabir Singh", "email": "Kabir@samaaja.org", "age": 21, "gender": "Male", "city": "Mohali", "state": "Punjab"},
        {"first_name": "Meera", "full_name": "Meera Banerjee", "email": "Meera@samaaja.org", "age": 31, "gender": "Female", "city": "Kolkata", "state": "West Bengal"},
        {"first_name": "Aniket", "full_name": "Aniket Joshi", "email": "Aniket@samaaja.org", "age": 25, "gender": "Male", "city": "Pune", "state": "Maharashtra"},
        {"first_name": "Iqra", "full_name": "Iqra Sheikh", "email": "Iqra@samaaja.org", "age": 18, "gender": "Female", "city": "Bhopal", "state": "Madhya Pradesh"},
        {"first_name": "Harshad", "full_name": "Harshad Iyer", "email": "Harshad@samaaja.org", "age": 30, "gender": "Male", "city": "Bengaluru", "state": "Karnataka"},
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
    print("🔥 Setting up samaaja successful!")
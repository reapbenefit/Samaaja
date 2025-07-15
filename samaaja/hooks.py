from . import __version__ as app_version

app_name = "samaaja"
app_title = "Samaaja"
app_publisher = "FOSS United"
app_description = "Samaaja is an open source software solution for rapidly building location based civic services connected with volunteer, human interactions. It comes with all necessary UI and management features and can be easily extended into web applications and external mobile apps and systems via built-in APIs."
app_email = "abhinav.raut@zerodha.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/samaaja/css/samaaja.css"
# app_include_js = "/assets/samaaja/js/samaaja.js"

# include js, css files in header of web template
web_include_css = ["samaaja.bundle.css"]
web_include_js = ""

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "samaaja/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "samaaja.utils.jinja_methods",
# 	"filters": "samaaja.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "samaaja.install.before_install"
# after_install = "samaaja.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "samaaja.uninstall.before_uninstall"
# after_uninstall = "samaaja.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "samaaja.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"samaaja.tasks.all"
# 	],
# 	"daily": [
# 		"samaaja.tasks.daily"
# 	],
# 	"hourly": [
# 		"samaaja.tasks.hourly"
# 	],
# 	"weekly": [
# 		"samaaja.tasks.weekly"
# 	],
# 	"monthly": [
# 		"samaaja.tasks.monthly"
# 	],
# }

scheduler_events = {
    #"all": ["samaaja.tasks.location_update"],
    # "hourly": ["samaaja.tasks.badge_update"]
}


# Testing
# -------

# before_tests = "samaaja.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "samaaja.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "samaaja.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"samaaja.auth.validate"
# ]

page_renderer = [
    "samaaja.page_renderers.ProfilePage",
]

""" website_redirects = [
    {"source": "/update-profile/", "target": "/edit-profile/"},
] """

website_route_rules = [
    {"from_route": "/user-profile/<username>", "to_route": "user-profile"},
    {"from_route": "/campaign/<route>", "to_route": "campaign"},
]

has_website_permission = {
    "Events": "samaaja.samaaja.doctype.events.events.has_website_permission"
}

profile_url_prefix = "/users/"


doc_events = {
   "Events": {
        "on_update": [
            "samaaja.doc_events.events.update_subcategory",
            "samaaja.doc_events.events.update_profile_hook",
        ],
        "after_insert": [
			"samaaja.doc_events.events.after_insert",
            "samaaja.doc_events.events.update_profile_hook",
		],
        "on_trash": "samaaja.doc_events.events.update_profile_hook",
    },
    "User": {
        "after_insert": "samaaja.doc_events.user.after_insert",
        "on_trash": "samaaja.doc_events.user.on_trash"
    },
    "Organization":{
        "before_save":"samaaja.api.common.update_organization_id_case"
    },
    "User Metadata": {
        "validate": "samaaja.doc_events.user_metadata.on_save"
    },
    "Energy Point Log": {
        "after_insert": "samaaja.doc_events.energy_point_log.handle_energy_point_log"
    }
}

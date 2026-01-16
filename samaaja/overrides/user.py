"""Overrides for User doctype"""

import frappe
from frappe.utils import random_string
from samaaja.samaaja.utils import make_image_public


def before_save(doc, _):
    """
    Number of new lines check for profile headline
    """
    if doc.headline:
        doc.headline = doc.headline.strip("\n")
        nlines = doc.headline.count("\n")
        if nlines > 5:
            frappe.throw(
                "Please make sure your profile headline is fewer than 7 lines long and try again.",
                title="Could not save profile headline",
            )
    doc.user_image = make_image_public(doc.user_image)
    doc.banner_image = make_image_public(doc.banner_image)


def username(doc, _):
    """Generate random username from first & last name"""
    if not doc.username:
        size = 6

        prefix = doc.first_name
        if doc.last_name:
            prefix += "-" + doc.last_name
        prefix = prefix.lower()

        username = prefix + "-" + random_string(size)
        while frappe.db.get_value("User", {"username": username}, "name"):
            username = prefix + random_string(size)

        doc.username = username.lower().replace(".", "").replace(" ", "")

def after_insert(doc, _):
    create_user_metadata(doc)

def create_user_metadata(doc):
    if not frappe.db.exists("User Metadata", {"user": doc.name}) and doc.name != "Administrator":
        frappe.get_doc({
            "doctype": "User Metadata",
            "user": doc.name
        }).insert(ignore_permissions=True)

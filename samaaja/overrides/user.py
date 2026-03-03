"""Overrides for User doctype"""

import frappe
from samaaja.utils.utils import make_image_public


def make_user_images_public(doc, method=None):
    """
    Make user_image and banner_image publicly accessible.

    Converts private file URLs to public ones using the `make_image_public` utility.
    Typically used in the `before_save` hook of the User doctype.
    """
    doc.user_image = make_image_public(doc.user_image)
    doc.banner_image = make_image_public(doc.banner_image)


def create_user_metadata(doc, method=None):
    if not frappe.db.exists("User Metadata", {"user": doc.name}) and doc.name != "Administrator":
        frappe.get_doc({
            "doctype": "User Metadata",
            "user": doc.name
        }).insert(ignore_permissions=True)

def delete_user_metadata(doc, method=None):
    if frappe.db.exists("User Metadata", doc.name):
        frappe.delete_doc("User Metadata", doc.name)

def generate_username_if_missing(doc, method=None):
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

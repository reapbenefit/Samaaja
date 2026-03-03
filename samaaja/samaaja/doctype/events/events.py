# Copyright (c) 2022, FOSSUnited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from samaaja.api.location import new_location
from frappe.utils import validate_email_address
from samaaja.utils.utils import make_image_public


class Events(Document):

    def validate(self):
        self.attachment1 = make_image_public(self.attachment1)
        self.attachment2 = make_image_public(self.attachment2)

    def before_insert(self):
        roles = frappe.get_roles()
        session_user = frappe.session.user

        # -------------------------------------------------
        # 1️⃣ Logged-in users
        # -------------------------------------------------
        if session_user != "Guest":

            # Auto-assign user if not provided
            if not self.user:
                self.user = session_user

            # Allow System Manager to create for anyone
            if "System Manager" in roles:
                pass

            # Allow user creating record for themselves
            elif self.user == session_user:
                pass

            # Block creating on behalf of others
            else:
                frappe.throw("Not allowed", frappe.PermissionError)

        # -------------------------------------------------
        # 2️⃣ Guest users (Web Form public submission)
        # -------------------------------------------------
        else:
            if not self.user:
                frappe.throw("Email is required")

            self.user = self.user.strip().lower()

            exists = frappe.db.exists("User", self.user)

            if exists:
                frappe.throw(
                    f"Looks like you already have an account with email {self.user}. "
                    "Please <a href='/login'>login</a>",
                    title="Account already exists",
                )

            # Create new Website User
            valid_email = validate_email_address(self.user)
            if valid_email:
                user = frappe.new_doc("User")
                first_name = (
                    self.user.split("@")[0]
                    .replace(".", "")
                    .replace("+", "")
                )

                user.update({
                    "first_name": first_name,
                    "email": self.user,
                    "enabled": 1,
                    "user_type": "Website User",
                    "send_welcome_email": 1,   # Better than generate_hash()
                })

                user.insert(ignore_permissions=True)

        # -------------------------------------------------
        # 3️⃣ Location auto creation
        # -------------------------------------------------
        if self.latitude and self.longitude:
            location = new_location({
                "latitude": self.latitude,
                "longitude": self.longitude
            })
            self.location = location.get("name")

def has_website_permission(doc, ptype, user, verbose=False):
    if doc.user == frappe.session.user:
        return True
    return False

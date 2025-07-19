# Copyright (c) 2025, Impactyaan and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestUserMetadata(FrappeTestCase):
    def setUp(self):
        self.test_email = "test_user_metadata@example.com"

        # Create test user if not exists
        if not frappe.db.exists("User", self.test_email):
            self.test_user = frappe.get_doc({
                "doctype": "User",
                "email": self.test_email,
                "first_name": "Test",
                "last_name": "User",
                "send_welcome_email": 0
            }).insert(ignore_permissions=True)
        else:
            self.test_user = frappe.get_doc("User", self.test_email)

    def test_user_metadata_created(self):
        """Test if User Metadata is created after inserting a User"""
        self.assertTrue(
            frappe.db.exists("User Metadata", self.test_user.name),
            "User Metadata should be created with same name as User"
        )

    def test_skip_administrator_user(self):
        """Ensure Administrator does not get a User Metadata document"""
        self.assertFalse(
            frappe.db.exists("User Metadata", "Administrator"),
            "User Metadata should not be created for Administrator"
        )

    def test_user_has_username(self):
        """Ensure that the created user has a valid username"""
        self.assertTrue(
            self.test_user.username,
            "Created User must have a username"
        )
    
    def test_user_metadata_fields_default(self):
        """Test default values of User Metadata fields after creation"""
        metadata = frappe.get_doc("User Metadata", self.test_user.name)
        self.assertIsNone(metadata.city)

    def test_user_metadata_deleted_with_user(self):
        """Test that User Metadata is deleted when User is deleted"""
        user_name = self.test_user.name
        self.assertTrue(frappe.db.exists("User Metadata", user_name))

        # Delete the user
        frappe.delete_doc("User", user_name)

        # Ensure User Metadata is deleted
        self.assertFalse(
            frappe.db.exists("User Metadata", user_name),
            "User Metadata should be deleted when User is deleted"
        )

    def tearDown(self):
        # Cleanup both user and metadata (if any)
        if frappe.db.exists("User Metadata", self.test_email):
            frappe.delete_doc("User Metadata", self.test_email)

        if frappe.db.exists("User", self.test_email):
            frappe.delete_doc("User", self.test_email)
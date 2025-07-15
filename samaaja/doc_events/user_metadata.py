import frappe
from samaaja.api.common import fetch_data_gov_in


@frappe.whitelist()
def update_user_metadata_location(doc):
    """
    Enqueue-safe method to update location (city, state) from pincode.
    """
    location_data = fetch_data_gov_in(doc.pincode)
    if location_data.get("records"):
        record = location_data["records"][0]
        city = record["district"].title()
        state = record["statename"].title()
        # Create city if not exists
        if not frappe.db.exists('Samaaja Cities', {'city_name': city}):
            frappe.get_doc({
                'doctype': 'Samaaja Cities',
                'city_name': city
            }).insert(ignore_permissions=True)

        doc.city = city
        doc.state = state
def on_save(doc, method):
    """
    Hook to update location fields when User Metadata is saved.
    """
    if doc.pincode:
        update_user_metadata_location(doc)
        
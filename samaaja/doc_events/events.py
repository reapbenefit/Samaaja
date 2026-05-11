import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count
from pypika.terms import Order
from frappe.utils import now_datetime, add_to_date


def update_profile(user: str):
    if not user:
        return

    # Aggregate event data
    result = frappe.db.get_all(
        "Events",
        filters={"user": user},
        fields=["sum(hours_invested) as total_hours", "count(*) as total_events"],
        group_by="user"
    )

    if result:
        total_hours = result[0].get("total_hours") or 0
        total_events = result[0].get("total_events") or 0
    else:
        total_hours = 0
        total_events = 0

    if frappe.db.exists("User Metadata", user):
        frappe.db.set_value("User Metadata", user, {
            "hours_invested": total_hours,
            "contributions": total_events
        }, update_modified=False)


def update_profile_hook(doc, method=None):
    if doc.user:
        frappe.enqueue("samaaja.doc_events.events.update_profile", queue='default', user=doc.user)

def process_manualupload_events():
    """Batch job to save Events created in the last 25 hours with source=manualupload"""
    from_date = add_to_date(now_datetime(), hours=-25)

    events = frappe.get_all(
        "Events",
        filters={
            "source": "manualupload",
            "creation": [">=", from_date]
        },
        fields=["name"]
    )

    for event in events:
        try:
            doc = frappe.get_doc("Events", event.name)
            doc.save(ignore_permissions=True)  # Triggers Energy Points
        except Exception as e:
            frappe.log_error(f"Failed to save Event: {event.name} - {str(e)}")

import frappe

def after_insert(doc, method=None):
    frappe.enqueue(
        "samaaja.services.action.update_action_details_in_user_metadata",
        queue='default',
        doc_name=doc.name
    )
    frappe.enqueue(
        "samaaja.services.user.update_user_interest_from_top_categories",
        queue='default',
        doc_name=doc.name
    )
    frappe.enqueue(
        "samaaja.services.community_post.create",
        queue='default',
        doc_name=doc.name
    )
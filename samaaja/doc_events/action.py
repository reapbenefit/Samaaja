import frappe
from frappe.utils import logger


logger.set_log_level("DEBUG")
logger = frappe.logger("samaaja", allow_site=True, file_count=50)

def after_insert(doc, method=None):
    logger.info("Action created: " + doc.name)
    frappe.enqueue(
        "samaaja.services.action.update_action_details_in_user_metadata",
        queue='short',
        doc_name=doc.name
    )
    frappe.enqueue(
        "samaaja.services.user.update_user_interest_from_top_categories",
        queue='short',
        doc_name=doc.name
    )
    frappe.enqueue(
        "samaaja.services.community_post.create",
        queue='short',
        doc_name=doc.name
    )

def on_trash(doc, method=None):
    frappe.enqueue(
        "samaaja.services.user.update_user_metadata",
        queue='short',
        doc_name=doc.name
    )
    frappe.enqueue(
        "samaaja.services.user.update_user_interest_from_top_categories",
        queue='short',
        doc_name=doc.name
    )
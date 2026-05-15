import frappe
from http import HTTPStatus
from samaaja.api.common import custom_response
from samaaja.services.action import ActionManager

@frappe.whitelist(methods=["POST"])
def create():
    try:
        title = frappe.form_dict.get("title")
        description = frappe.form_dict.get("description")
        hours_invested = frappe.form_dict.get("hours_invested")
        category = frappe.form_dict.get("category")
        media = frappe.request.files.get("attachments")
        action_type = frappe.form_dict.get("type")
        return ActionManager.create(
                                    title=title,
                                    description=description,
                                    hours_invested=hours_invested,
                                    category=category,
                                    user=frappe.session.user,
                                    action_type=action_type,
                                    media=media
                                ).to_custom_response()
    except Exception as e:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to create action"
        )
        return custom_response("Failed to create action", status_code=500)



@frappe.whitelist(methods=["DELETE"])
def delete(doc_name):
    """
    Delete an Event document if the current user is the owner.

    This function checks if the logged-in user is the owner of the event. If they are, 
    it proceeds to delete the event document. If not, it returns a Forbidden response.

    Parameters:
        doc_name (str): The name (ID) of the Event document to delete.

    Returns:
        Response: A custom HTTP response indicating success or failure.
    """
    
    # Check if the current user is the owner of the event
    if frappe.session.user != frappe.get_value("Events", doc_name, "user"):
        return custom_response("Forbidden", status_code=HTTPStatus.FORBIDDEN)

    # Proceed to delete the event document
    frappe.delete_doc("Events", doc_name)

    # Return a success response
    return custom_response("OK", status_code=HTTPStatus.OK)



@frappe.whitelist()
def get_event_type_query(get_child_types: bool=False, parent_event: str|None=None):

    if get_child_types:
        if parent_event:
            return frappe.db.sql("""
                SELECT name
                FROM `tabEvent Type`
                WHERE parent_event_type = %(parent_event)s
                AND is_group = 0
            """, {
                "parent_event": parent_event
            })
        else:
            return frappe.db.sql("""
                SELECT name
                FROM `tabEvent Type`
                WHERE is_group = 0
                """)
    else:
        return frappe.db.sql("""
            SELECT name
            FROM `tabEvent Type`
            WHERE is_group = 1
            """)
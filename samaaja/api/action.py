import frappe
from http import HTTPStatus
from samaaja.api.common import custom_response

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
import frappe

def after_insert(doc, method):
    if not frappe.db.exists("User Metadata", doc.name) and doc.name != "Administrator":
        frappe.get_doc({
            "doctype": "User Metadata",
            "user": doc.name
        }).insert(ignore_permissions=True)
    
def on_trash(doc, method):
    """
    Delete the associated User Metadata when a User is deleted.
    """
    if frappe.db.exists("User Metadata", doc.name):
        frappe.delete_doc("User Metadata", doc.name, ignore_permissions=True)
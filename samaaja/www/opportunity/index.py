import frappe

def get_context(context):
    route = frappe.form_dict.opportunity  # captures dynamic part of the URL

    doc = frappe.get_doc("Opportunity Template", {"route": route, "published": 1})
    if not doc:
        frappe.throw("Opportunity not found or not published")

    context.opportunity = doc
    #context.show_apply_button = doc.accept_applications and doc.deadline >= frappe.utils.today()
    context.show_apply_button = True
import frappe

@frappe.whitelist(allow_guest=True)
def get_opportunity_type(opportunity_title):
    doc = frappe.get_doc("Opportunity Template", {"title": opportunity_title})
    return doc.opp_type

@frappe.whitelist(allow_guest=True)
def get_opportunity(name):
    doc = frappe.get_doc("Opportunity Template", {"name": name})
    return doc
import frappe

def get_context(context):
    frappe.local.flags.redirect_location = "https://samaaja.impactyaan.com"
    raise frappe.Redirect
import frappe
import json

@frappe.whitelist(allow_guest=True)
def submit_campaign_petition(data):
    try:
        if isinstance(data, str):
            data = frappe._dict(json.loads(data))
        else:
            data = frappe._dict(data)

        petition = frappe.new_doc("Campaign Petition")
        petition.update({
            "campaign": data.campaign,
            "subject": data.subject,
            "message_body": data.message_body,
            "first_name": data.first_name,
            "last_name": data.last_name,
            "email": data.email,
            "address_line_1": data.address_line_1,
            "town": data.town,
            "pincode": data.pincode,
        })

        # Load the full campaign to get recipient emails
        campaign_doc = frappe.get_doc("Campaign Template", data.campaign)
        recipient_lookup = {r.recipient_name: r for r in campaign_doc.recipients}

        for r in data.recipients or []:
            name = r.get("recipient")
            row = recipient_lookup.get(name)
            if row:
                petition.append("recipients", {
                    "recipient": row.recipient_name,
                    "email": row.email
                })

        petition.insert(ignore_permissions=True)
        frappe.db.commit()
        return "ok"

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Campaign Petition Submission Failed")
        frappe.throw("Something went wrong while submitting your petition. Please try again later.")

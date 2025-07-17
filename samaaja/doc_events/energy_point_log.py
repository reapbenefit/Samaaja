import frappe

def before_insert(doc, method):
    doc.flags.ignore_permissions = True
    if not doc.user:
        return
    if doc.type == "Auto" and doc.badge:
        user_badge_name = frappe.db.exists("User badge", {"user": doc.user, "badge": doc.badge})

        if user_badge_name:
            user_badge = frappe.get_doc("User badge", user_badge_name)
            user_badge.badge_count += 1
        else:
            user_badge = frappe.get_doc({
                "doctype": "User badge",
                "user": doc.user,
                "badge": doc.badge,
                "active": 1,
                "badge_count": 1
            })
            user_badge.insert(ignore_permissions = True)

        user_badge.active = 1  # Ensure it's active
        user_badge.flags.ignore_permissions = True
        user_badge.save()

    elif doc.type == "Revert" and doc.revert_of:
        if not frappe.db.exists("Energy Point Log", doc.revert_of):
            return  # Avoid error if revert_of doesn't exist
        
        revert_of = frappe.get_doc("Energy Point Log", doc.revert_of)

        if revert_of.badge and revert_of.user:
            user_badge_name = frappe.db.exists("User badge", {"user": revert_of.user, "badge": revert_of.badge})

            if user_badge_name:
                user_badge = frappe.get_doc("User badge", user_badge_name)

                if user_badge.badge_count > 0:
                    user_badge.badge_count -= 1
                
                # Deactivate if count reaches zero
                user_badge.active = 1 if user_badge.badge_count > 0 else 0
                user_badge.flags.ignore_permissions = True
                user_badge.save()

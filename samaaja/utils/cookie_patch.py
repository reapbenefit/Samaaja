import frappe.auth

def apply_patch():
    if not getattr(frappe.auth, "_cookie_patch_done", False):
        original_set_cookie = frappe.auth.CookieManager.set_cookie

        def custom_set_cookie(self, key, value, *args, **kwargs):
            kwargs["samesite"] = "None"
            kwargs["secure"] = True
            return original_set_cookie(self, key, value, *args, **kwargs)

        frappe.auth.CookieManager.set_cookie = custom_set_cookie
        frappe.auth._cookie_patch_done = True

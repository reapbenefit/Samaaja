import frappe
from frappe import _
from samaaja.utils.result import Result


class AnnouncementManager:

    @staticmethod
    def get_announcement(name: str) -> dict:
        return frappe.get_doc("Announcement", name).as_dict()

    @staticmethod
    def get_active_announcements() -> Result:
        now = frappe.utils.now_datetime()

        names = frappe.get_all("Announcement",
            filters={"published": 1},
            pluck="name"
        )

        announcements = []
        for name in names:
            doc = frappe.get_doc("Announcement", name)

            if doc.valid_from and doc.valid_from > now:
                continue
            if doc.valid_to and doc.valid_to < now:
                continue
            if doc.target_audience == "Registered Users" and frappe.session.user == "Guest":
                continue

            announcements.append({
                "name": doc.name,
                "title": doc.title,
                "message": doc.message,
                "url_link": doc.url_link,
                "image": doc.image,
                "valid_from": doc.valid_from,
                "valid_to": doc.valid_to,
                "target_audience": doc.target_audience,
            })

        announcements.sort(key=lambda x: x["valid_from"] or "", reverse=True)
        return Result.success("Announcements fetched successfully", data=announcements)

    @staticmethod
    def record_interaction(announcement: str, interaction_type: str, contact_id: str = None) -> Result:
        if interaction_type not in ["View", "Click"]:
            return Result.bad_request("Invalid interaction type. Must be View or Click.")

        if not frappe.db.exists("Announcement", announcement):
            return Result.not_found(f"Announcement {announcement} not found.")

        frappe.get_doc({
            "doctype": "Announcement Interaction",
            "announcement": announcement,
            "interaction_type": interaction_type,
            "user": frappe.session.user,
            "contact_id": contact_id,
            "ip_address": frappe.local.request.remote_addr if hasattr(frappe.local, "request") else None
        }).insert(ignore_permissions=True)
        frappe.db.commit()

        return Result.success("Interaction recorded", data={"status": "success"})

    @staticmethod
    def process_scheduled_announcements():
        from frappe.utils import now_datetime, add_to_date, get_datetime
        now = now_datetime()

        scheduled = frappe.get_all("Announcement",
            filters={"published": 0, "publish_on": ["<=", now]},
            pluck="name"
        )
        for name in scheduled:
            doc = frappe.get_doc("Announcement", name)
            doc.published = 1
            doc.valid_from = now
            doc.save(ignore_permissions=True)
            AnnouncementManager.deliver_announcement(doc)
            frappe.db.commit()

        recurring = frappe.get_all("Announcement",
            filters={"published": 1, "is_recurring": 1},
            fields=["name", "frequency", "last_sent_on", "repeat_until", "total_repeat_times", "current_repeat_count"]
        )
        for r in recurring:
            if r.repeat_until and get_datetime(r.repeat_until) < now:
                continue
            if r.total_repeat_times and r.current_repeat_count >= r.total_repeat_times:
                continue

            should_send = not r.last_sent_on
            if not should_send:
                last_sent = get_datetime(r.last_sent_on)
                if r.frequency == "Hourly" and add_to_date(last_sent, hours=1) <= now:
                    should_send = True
                elif r.frequency == "Daily" and add_to_date(last_sent, days=1) <= now:
                    should_send = True
                elif r.frequency == "Weekly" and add_to_date(last_sent, weeks=1) <= now:
                    should_send = True
                elif r.frequency == "Monthly" and add_to_date(last_sent, months=1) <= now:
                    should_send = True

            if should_send:
                doc = frappe.get_doc("Announcement", r.name)
                AnnouncementManager.deliver_announcement(doc)
                doc.last_sent_on = now
                doc.current_repeat_count = (doc.current_repeat_count or 0) + 1
                doc.save(ignore_permissions=True)
                frappe.db.commit()

    @staticmethod
    def deliver_announcement(doc):
        for channel in (doc.delivery_channels or []):
            if not channel.enabled:
                continue
            if channel.channel_name == "Email":
                AnnouncementManager._send_email(doc)
            elif channel.channel_name == "App Notification":
                AnnouncementManager._send_app_notification(doc)
            elif channel.channel_name == "WhatsApp":
                frappe.log_error(f"WhatsApp delivery pending for {doc.name}", "WhatsApp")

    @staticmethod
    def _send_email(doc):
        users = AnnouncementManager._get_target_users(doc.target_audience)
        if users:
            frappe.sendmail(
                recipients=users,
                subject=doc.title,
                message=doc.message,
                reference_doctype=doc.doctype,
                reference_name=doc.name
            )

    @staticmethod
    def _send_app_notification(doc):
        for user in AnnouncementManager._get_target_users(doc.target_audience):
            frappe.get_doc({
                "doctype": "Notification Log",
                "for_user": user,
                "subject": doc.title,
                "email_content": doc.message,
                "document_type": doc.doctype,
                "document_name": doc.name,
                "type": "Alert"
            }).insert(ignore_permissions=True)

    @staticmethod
    def _get_target_users(audience: str) -> list:
        if audience == "All":
            return frappe.get_all("User", filters={"enabled": 1}, pluck="name")
        if audience == "Registered Users":
            return frappe.get_all("User", filters={"enabled": 1, "name": ["!=", "Guest"]}, pluck="name")
        return []

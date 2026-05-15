import frappe
from frappe import _
from samaaja.utils.result import Result

class AnnouncementManager:
    @staticmethod
    def get_active_announcements():
        now = frappe.utils.now_datetime()
        
        # Fetch all published announcements
        announcements = frappe.get_all("Announcement", 
            filters={"published": 1},
            fields=["name", "title", "message", "url_link", "image", "valid_from", "valid_to", "target_audience", "total_views", "total_clicks"]
        )
        
        filtered_announcements = []
        for a in announcements:
            # 1. Valid From Check
            if a.valid_from and a.valid_from > now:
                continue
                
            # 2. Valid To Check
            if a.valid_to and a.valid_to < now:
                continue
            
            # 3. Audience Check
            if a.target_audience == "Registered Users" and frappe.session.user == "Guest":
                continue
                
            filtered_announcements.append(a)
            
        # Sort by valid_from descending
        filtered_announcements.sort(key=lambda x: x.valid_from, reverse=True)
            
        return filtered_announcements

    @staticmethod
    def get_unread_count():
        """Returns count of active announcements not yet viewed by current user"""
        active = AnnouncementManager.get_active_announcements()
        if not active:
            return 0
            
        active_names = [a.name for a in active]
        
        # Identify views by this user
        viewed_filters = {
            "announcement": ["in", active_names],
            "interaction_type": "View"
        }
        
        if frappe.session.user != "Guest":
            viewed_filters["user"] = frappe.session.user
        else:
            viewed_filters["ip_address"] = frappe.local.request.remote_addr if hasattr(frappe.local, "request") else "unknown"
            
        viewed_names = frappe.get_all("Announcement Interaction", 
            filters=viewed_filters, 
            pluck="announcement"
        )
        
        # Remove duplicates (one user might view multiple times)
        viewed_names = list(set(viewed_names))
        
        unread_count = len(active_names) - len(viewed_names)
        return max(0, unread_count)

    @staticmethod
    def record_interaction(announcement, interaction_type, contact_id=None):
        if interaction_type not in ["View", "Click"]:
            frappe.throw(_("Invalid interaction type"))
        
        doc = frappe.get_doc({
            "doctype": "Announcement Interaction",
            "announcement": announcement,
            "interaction_type": interaction_type,
            "user": frappe.session.user if frappe.session.user != "Guest" else None,
            "contact_id": contact_id,
            "ip_address": frappe.local.request.remote_addr if hasattr(frappe.local, "request") else None
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return {"status": "success"}

    @staticmethod
    def process_scheduled_announcements():
        from frappe.utils import now_datetime
        now = now_datetime()
        
        # 1. Process Scheduled Publish
        scheduled = frappe.get_all("Announcement", 
            filters={
                "published": 0,
                "publish_on": ["<=", now]
            },
            fields=["name", "title"]
        )
        
        for s in scheduled:
            doc = frappe.get_doc("Announcement", s.name)
            doc.published = 1
            doc.valid_from = now
            doc.save(ignore_permissions=True)
            AnnouncementManager.deliver_announcement(doc)
            frappe.db.commit()

        # 2. Process Recurring Announcements
        recurring = frappe.get_all("Announcement",
            filters={
                "published": 1,
                "is_recurring": 1
            },
            fields=["name", "frequency", "last_sent_on", "repeat_until", "total_repeat_times", "current_repeat_count"]
        )
        
        from frappe.utils import add_to_date, get_datetime
        for r in recurring:
            if r.repeat_until and get_datetime(r.repeat_until) < now:
                continue
            if r.total_repeat_times and r.current_repeat_count >= r.total_repeat_times:
                continue

            should_send = False
            if not r.last_sent_on:
                should_send = True
            else:
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
        if not doc.delivery_channels:
            return
            
        for channel in doc.delivery_channels:
            if not channel.enabled:
                continue
                
            if channel.channel_name == "Email":
                AnnouncementManager.send_email(doc)
            elif channel.channel_name == "App Notification":
                AnnouncementManager.send_app_notification(doc)
            elif channel.channel_name == "WhatsApp":
                AnnouncementManager.send_whatsapp(doc)

    @staticmethod
    def send_email(doc):
        users = AnnouncementManager.get_target_users(doc.target_audience)
        if not users:
            return
        frappe.sendmail(
            recipients=users,
            subject=doc.title,
            message=doc.message,
            reference_doctype=doc.doctype,
            reference_name=doc.name
        )

    @staticmethod
    def send_app_notification(doc):
        users = AnnouncementManager.get_target_users(doc.target_audience)
        for user in users:
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
    def send_whatsapp(doc):
        frappe.log_error(f"WhatsApp requested for {doc.name}, but Glific API integration is pending configuration.", "WhatsApp Delivery")

    @staticmethod
    def get_target_users(audience):
        if audience == "All":
            return frappe.get_all("User", filters={"enabled": 1}, pluck="name")
        elif audience == "Registered Users":
            return frappe.get_all("User", filters={"enabled": 1, "name": ["!=", "Guest"]}, pluck="name")
        return []

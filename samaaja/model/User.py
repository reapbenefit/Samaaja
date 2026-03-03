# Copyright (c) 2025, Impactyaan and contributors
# For license information, please see license.txt

"""
Samaaja User Profile Model/Service

This class aggregates user profile data from multiple doctypes:
- User (core Frappe doctype)
- User Metadata (Samaaja custom doctype)
- Location (Samaaja custom doctype)
- District (Samaaja custom doctype)
- User Review (verification status)
- Events (actions/contributions)
- User badge (badges, skills, partners)

Usage:
    profile = SamaajaUserProfile(user_name="user@example.com")
    # or
    profile = SamaajaUserProfile.from_username("username")
    
    # Access aggregated data
    profile.full_name
    profile.location_info
    profile.stats
    profile.badges
"""

import frappe
from frappe.query_builder import DocType, functions as fn
from typing import Optional, Dict, List


class SamaajaUserProfile:
	"""
	Service class that aggregates user profile data from multiple doctypes.
	Provides a unified interface to access all user-related information.
	"""
	
	def __init__(self, user_name: str):
		"""
		Initialize with user name (email or username)
		
		Args:
			user_name: User name (email) or username
		"""
		self.user_name = user_name
		self._user = None
		self._user_metadata = None
		self._location = None
		self._district = None
		self._user_review = None
		self._stats = None
		self._badges = None
		self._actions = None
		self._reviews = None
		self._loaded = False
	
	@classmethod
	def from_username(cls, username: str) -> 'SamaajaUserProfile':
		"""
		Create instance from username
		
		Args:
			username: Username of the user
			
		Returns:
			SamaajaUserProfile instance
		"""
		user_name = frappe.db.get_value("User", {"username": username}, "name")
		if not user_name:
			raise frappe.DoesNotExistError(f"User with username '{username}' not found")
		return cls(user_name)
	
	@property
	def user(self):
		"""Get User document (lazy loaded)"""
		if self._user is None:
			self._user = frappe.get_doc("User", self.user_name)
		return self._user
	
	@property
	def user_metadata(self):
		"""Get User Metadata document (lazy loaded)"""
		if self._user_metadata is None:
			if frappe.db.exists("User Metadata", self.user_name):
				self._user_metadata = frappe.get_doc("User Metadata", self.user_name)
			else:
				self._user_metadata = None
		return self._user_metadata
	
	@property
	def location(self):
		"""Get Location document (lazy loaded)"""
		if self._location is None and self.user_metadata and self.user_metadata.location:
			if frappe.db.exists("Location", self.user_metadata.location):
				self._location = frappe.get_doc("Location", self.user_metadata.location)
		return self._location
	
	@property
	def district(self):
		"""Get District document (lazy loaded)"""
		if self._district is None and self.location and self.location.district:
			if frappe.db.exists("District", self.location.district):
				self._district = frappe.get_doc("District", self.location.district)
		return self._district
	
	@property
	def user_review(self):
		"""Get User Review document if verified (lazy loaded)"""
		if self._user_review is None:
			review = frappe.db.get_value(
				"User Review",
				{"user": self.user_name, "status": "Accepted"},
				"name"
			)
			if review:
				self._user_review = frappe.get_doc("User Review", review)
		return self._user_review
	
	# Basic Profile Properties
	@property
	def full_name(self) -> str:
		"""Get user's full name"""
		return self.user.full_name or ""
	
	@property
	def username(self) -> str:
		"""Get username"""
		return self.user.username or ""
	
	@property
	def email(self) -> str:
		"""Get user email"""
		return self.user.name
	
	@property
	def user_image(self) -> Optional[str]:
		"""Get user image URL"""
		return self.user.user_image
	
	@property
	def focus_area(self) -> Optional[str]:
		"""Get user's interest/focus area"""
		return self.user.interest
	
	# Location Properties
	@property
	def location_info(self) -> Dict:
		"""
		Get complete location information
		
		Returns:
			Dict with city, district, state, village_name, panchayat_name
		"""
		if not self.location:
			return {}
		
		location_data = {
			"city": self.location.city,
			"state": self.location.state,
			"village_name": self.location.village_name,
			"panchayat_name": self.location.grama_panchayath,
		}
		
		if self.district:
			location_data["district"] = self.district.district_name
		elif self.location.district:
			location_data["district"] = self.location.district
		
		return location_data
	
	@property
	def display_location(self) -> str:
		"""Get display location based on Samaaja Settings"""
		if not self.location:
			return ""
		
		settings = frappe.get_cached_doc("Samaaja Settings")
		location_field = getattr(settings, "user_profile_location_field", "city")
		
		if location_field == "district" and self.district:
			return self.district.district_name
		
		return self.location.get(location_field) or ""
	
	# Verification
	@property
	def is_verified(self) -> bool:
		"""Check if user is verified"""
		return self.user_review is not None
	
	@property
	def verified_by(self) -> Optional[str]:
		"""Get name of person who verified the user"""
		if self.user_review:
			return self.user_review.reviewer_name
		return None
	
	# Statistics
	@property
	def stats(self) -> Dict:
		"""
		Get user statistics
		
		Returns:
			Dict with contributions, hours_invested, total_actions
		"""
		if self._stats is None:
			contributions = 0
			hours_invested = 0
			
			if self.user_metadata:
				contributions = self.user_metadata.contributions or 0
				hours_invested = self.user_metadata.hours_invested or 0
			
			# Get total actions count
			total_actions = frappe.db.count("Events", {"user": self.user_name})
			
			self._stats = {
				"contributions": contributions,
				"hours_invested": hours_invested,
				"total_actions": total_actions
			}
		
		return self._stats
	
	# Actions/Events
	@property
	def actions(self) -> List[Dict]:
		"""
		Get user's actions/events
		
		Returns:
			List of event dictionaries
		"""
		if self._actions is None:
			Events = DocType("Events")
			Location = DocType("Location")
			
			query = (
				frappe.qb.from_(Events)
				.left_join(Location)
				.on(Events.location == Location.name)
				.select(
					Events.name.as_("event_id"),
					Events.title,
					Events.type,
					Events.category,
					Events.description,
					Events.location,
					Events.creation,
					Events.highlight,
					Events.verified_by,
					Events.hours_invested,
					Location.district.as_("location_name")
				)
				.where(Events.user == self.user_name)
				.orderby(Events.creation, order=frappe.qb.desc)
			)
			
			self._actions = query.run(as_dict=True)
			
			# Process actions
			for action in self._actions:
				action.creation = frappe.utils.pretty_date(action.creation)
				action.review_exists = frappe.db.exists(
					"Events Review",
					{"events": action.event_id, "status": "Accepted"}
				)
				if action.review_exists:
					action.review = frappe.get_doc("Events Review", action.review_exists)
		
		return self._actions
	
	@property
	def highlighted_action(self) -> Dict:
		"""Get highlighted action"""
		for action in self.actions:
			if action.get("highlight") == 1:
				return {
					"title": action.get("title", ""),
					"description": action.get("description", "")
				}
		return {"title": "", "description": ""}
	
	# Badges
	@property
	def badges(self) -> Dict:
		"""
		Get user badges organized by type
		
		Returns:
			Dict with 'skills' and 'partners' lists
		"""
		if self._badges is None:
			user_badges = frappe.db.get_all(
				'User badge',
				filters={'user': self.user_name, 'active': 1},
				fields=['badge', 'badge_count']
			)
			
			skills = []
			partners = []
			
			for user_badge in user_badges:
				badge_doc = frappe.get_doc('Badge', user_badge.badge)
				tags = badge_doc.get_tags()
				
				badge_data = {
					"name": badge_doc.title,
					"image": badge_doc.icon,
					"badge_count": user_badge.badge_count
				}
				
				if badge_doc.badge_type == "Skill":
					skills.append(badge_data)
				if 'Partners' in tags:
					partners.append(badge_data)
			
			self._badges = {
				"skills": skills,
				"partners": partners
			}
		
		return self._badges
	
	# Reviews
	@property
	def reviews(self) -> List[Dict]:
		"""Get user reviews"""
		if self._reviews is None:
			self._reviews = frappe.db.get_all(
				"User Review",
				filters={"user": self.user_name, "status": "Accepted"},
				fields=["review_title", "reviewer_name", "designation", "comment", "organisation"]
			)
		return self._reviews
	
	# Profile URL
	@property
	def profile_url(self) -> str:
		"""Get user profile URL"""
		return frappe.utils.get_url(f"/user-profile/{self.username}")
	
	# Complete Profile Data
	def get_complete_profile(self) -> Dict:
		"""
		Get complete profile data as dictionary
		
		Returns:
			Dict with all profile information
		"""
		return {
			"user": {
				"name": self.user.name,
				"full_name": self.full_name,
				"username": self.username,
				"email": self.email,
				"user_image": self.user_image,
				"focus_area": self.focus_area,
			},
			"location": self.location_info,
			"display_location": self.display_location,
			"verification": {
				"is_verified": self.is_verified,
				"verified_by": self.verified_by,
			},
			"stats": self.stats,
			"badges": self.badges,
			"actions_count": len(self.actions),
			"reviews_count": len(self.reviews),
			"profile_url": self.profile_url,
		}
	
	def as_dict(self) -> Dict:
		"""Alias for get_complete_profile()"""
		return self.get_complete_profile()

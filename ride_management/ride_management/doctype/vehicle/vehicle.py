# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator


class Vehicle(WebsiteGenerator):

	def before_validate(self):
		self.is_published = self.status == "Available"
	pass

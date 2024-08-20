# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Ride(Document):

	def before_validate(self):
		self.calculate_cost()
	

	def calculate_cost(self):

		self.total_hours = 0

		for stop in self.ride_stops:
			self.total_hours += stop.hours
		
		self.total_cost = self.total_hours * (self.cost_per_hour or 0)
	pass

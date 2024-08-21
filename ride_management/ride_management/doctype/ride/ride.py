# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Ride(Document):

	def before_validate(self):
		self.calculate_cost()
	

	def calculate_cost(self):

		self.total_hours = 0

		for stop in self.ride_stops:
			self.total_hours += stop.hours
		
		self.total_cost = self.total_hours * (self.cost_per_hour or 0)
	
	def before_submit(self):
		# Check if the vehicle is available
		# If not, throw an error

		vehicle_status = frappe.db.get_value("Vehicle", self.vehicle, "status")

		if vehicle_status != "Available":
			frappe.throw("Vehicle is not available")
		
		self.status = "In Progress"
	
	def on_submit(self):
		# Update the vehicle status to "Unavailable"

		vehicle_doc = frappe.get_doc("Vehicle", self.vehicle)

		vehicle_doc.status = "Unavailable"

		vehicle_doc.save()

		# Alternate method
		# frappe.db.set_value("Vehicle", self.vehicle, "status", "Unavailable")
	
	def before_cancel(self):
		if self.status == "Completed":
			frappe.throw("Cannot cancel a completed ride")
		
		self.status = "Cancelled"
	
	def on_cancel(self):
		# Update the vehicle status to "Available"

		vehicle_doc = frappe.get_doc("Vehicle", self.vehicle)

		vehicle_doc.status = "Available"

		vehicle_doc.save()

		# Alternate method
		# frappe.db.set_value("Vehicle", self.vehicle, "status", "Available")


@frappe.whitelist()
def complete_ride(ride_id):

	status, docstatus = frappe.db.get_value("Ride", ride_id, ["status", "docstatus"])

	if status != "In Progress" or docstatus != 1:
		return frappe.throw("Cannot complete ride")
	
	frappe.db.set_value("Ride", ride_id, "status", "Completed")

	vehicle = frappe.db.get_value("Ride", ride_id, "vehicle")

	frappe.db.set_value("Vehicle", vehicle, "status", "Available")

	return "Ride Completed"
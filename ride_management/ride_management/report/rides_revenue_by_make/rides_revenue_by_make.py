# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count, Sum


def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data()

	chart = get_chart(data)

	return columns, data, None, chart


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Make"),
			"fieldname": "make",
			"fieldtype": "Link",
			"options": "Vehicle Make",
		},
		{
			"label": _("Number of Rides"),
			"fieldname": "number_of_rides",
			"fieldtype": "Int",
		},
		{
			"label": _("Total Revenue"),
			"fieldname": "total_revenue",
			"fieldtype": "Currency",
			"options": "currency",
		},
		{
			"label": _("Currency"),
			"fieldname": "currency",
			"fieldtype": "Data",
			"hidden": 1,
		}
	]


def get_data() -> list[list]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""

	# Using the Query Builder
	ride = DocType("Ride")
	vehicle = DocType("Vehicle")

	query = (frappe.qb.from_(ride)
		  .join(vehicle)
		  .on(ride.vehicle == vehicle.name)
		  .select(vehicle.make, 
			Count(ride.name).as_("number_of_rides"), 
			ride.currency,
			Sum(ride.total_cost).as_("total_revenue")
		)
		.where(ride.docstatus == 1)
		.groupby(vehicle.make)
	)

	result = query.run(as_dict=True)

	return result

	# Raw SQL Query

	# result = frappe.db.sql("""
	# 	SELECT `tabVehicle`.make, COUNT(`tabRide`.name) AS number_of_rides, `tabRide`.currency, SUM(`tabRide`.total_cost) AS total_revenue
	# 	FROM `tabRide`
	# 	JOIN `tabVehicle` ON `tabRide`.vehicle = `tabVehicle`.name
	# 	WHERE `tabRide`.docstatus = 1
	# 	GROUP BY `tabVehicle`.make
	# 	""", as_dict=True)
	
	# return result


	# Not a performant way to do this
	# rides = frappe.get_all("Ride", fields=["vehicle", "total_cost", "currency"],
	# 					filters={"docstatus": 1})

	# # For each ride, we need to find it's make

	# data = {}

	# vehicle_makes = {}

	# for ride in rides:

	# 	if not ride.vehicle in vehicle_makes:
	# 		vehicle_makes[ride.vehicle] = frappe.get_cached_value("Vehicle", ride.vehicle, "make")
		
	# 	make = vehicle_makes[ride.vehicle]

	# 	if make not in data:
	# 		data[make] = {"number_of_rides": 0, "total_revenue": 0}
		
	# 	data[make]["number_of_rides"] += 1
	# 	data[make]["total_revenue"] += ride.total_cost
	# 	data[make]["currency"] = ride.currency
		

	# return_data = []

	# for make, values in data.items():
	# 	return_data.append([make, values["number_of_rides"], values["total_revenue"], values["currency"]])

	# return return_data


def get_chart(data):

	makes = [d.make for d in data]

	revenue_values = [d.total_revenue for d in data]

	return {
		"data": {
			"labels": makes,
			"datasets": [
				{"name": _("Revenue"), "values": revenue_values},
			],
		},
		"type": "pie",
	}
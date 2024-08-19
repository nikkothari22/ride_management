# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, today


class Driver(Document):

	def before_naming(self):
		self.set_full_name()

	def before_validate(self):
		self.set_full_name()
		self.set_age()

	def validate(self):
		if self.age < 18:
			frappe.throw("Driver must be at least 18 years old")

	def set_full_name(self):
		self.full_name = f"{self.first_name} {self.last_name}"

	def set_age(self):
		if self.date_of_birth:
			self.age = date_diff(today(), self.date_of_birth) // 365
	pass

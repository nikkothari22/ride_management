// Copyright (c) 2024, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("Ride", {

    onload(frm) {

        if (frm.is_new()) {
            frappe.db.get_doc("Ride Settings", "Ride Settings")
                .then(ride_settings => {
                    frm.set_value("cost_per_hour", ride_settings.default_cost_per_hour);
                });
        }

    },
    refresh(frm) {

        // Set up a filter for vehicles to only show vehicles that are available
        frm.set_query("vehicle", function () {
            return {
                filters: {
                    status: "Available"
                }
            }
        })

    },

    cost_per_hour(frm) {
        frm.trigger("calculate_total_cost");
    },

    calculate_total_cost(frm) {
        // Calculate the total cost of the ride

        const total_cost = frm.doc.total_hours * frm.doc.cost_per_hour;
        frm.set_value("total_cost", total_cost);
    },

    calculate_total_hours(frm) {
        // Calculate the total hours of the ride
        let total_hours = 0;
        frm.doc.ride_stops.forEach(stop => {
            total_hours += stop.hours;
        });

        frm.set_value("total_hours", total_hours);
    },

    total_hours(frm) {
        frm.trigger("calculate_total_cost");
    }
});

frappe.ui.form.on("Ride Stops", {

    hours(frm, cdt, cdn) {
        // Calculate the total hours of the ride
        frm.trigger("calculate_total_hours");
    },
    ride_stops_remove(frm, cdt, cdn) {
        // Calculate the total hours of the ride
        frm.trigger("calculate_total_hours");
    }
})

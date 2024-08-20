// Copyright (c) 2024, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("Ride Booking", {
    refresh(frm) {

        frm.add_custom_button("Create Ride", () => {

            const dialog = new frappe.ui.Dialog({
                title: "Create Ride",
                fields: [
                    {
                        fieldtype: "Link",
                        fieldname: "driver",
                        label: "Driver",
                        options: "Driver",
                        reqd: 1
                    }
                ],
                primary_action_label: "Create",
                primary_action: function (data) {

                    frappe.new_doc('Ride', {
                        "ride_booking": frm.doc.name,
                        "driver": data.driver
                    })
                }
            })

            dialog.show()







        })

    },
});

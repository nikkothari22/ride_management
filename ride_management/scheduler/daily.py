import frappe

def send_insurance_reminder():

    thirty_days_ago = frappe.utils.add_days(frappe.utils.nowdate(), -30)
    # Get all vehicles whose insurance is expiring in 30 days
    vehicles = frappe.get_all("Vehicle", 
                              filters={"insurance_expiry_date": ["<=", thirty_days_ago]})
    
    for vehicle in vehicles:
        # Send email to the vehicle owner
        print(f"Sending insurance reminder to {vehicle.owner}")
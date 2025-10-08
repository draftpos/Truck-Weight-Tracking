import frappe

def before_save(doc, method):
    # Log for debugging
    print("------------------------before save on truck-----------------")

    # Only trigger for target item
    target_item = "LP"
    if not doc.items or not any(item.item_name == target_item for item in doc.items):
        return  # Skip if LP not in items

    # Ensure project is set
    if not doc.project:
        frappe.throw("For item 'LP', please provide a Project (Truck) 🚚")

    # Your custom logic
    frappe.msgprint(f"Applying special logic for {target_item} 🚚")

        # Get latest Truck Weight Entry for that project
    latest_entry = frappe.get_all(
        "Truck Weight Entry",
        filters={"truck_reg_no": doc.project},  # filter by invoice project
        order_by="creation desc",
        limit_page_length=1,
        fields=["name", "truck_reg_no", "invoice","offloaded_weight", "creation"]
    )

    # Get the first (latest) entry safely
    latest_entry = latest_entry[0] if latest_entry else None
    if not latest_entry:
        frappe.throw(f"No Truck Weight Entry found for project {doc.project} 🚛")

    if latest_entry.get('invoice'):
        frappe.throw(f"Truck Weight Entry already used with invoice : {latest_entry.get('invoice')}")


    

    # Make sure the invoice actually has the target item before updating qty
    if any(item.item_name == target_item for item in doc.items):
        # Update qty of all matching items
        for item in doc.items:
            if item.item_name == target_item:
                item.qty = latest_entry.get('offloaded_weight', 0)  # default 0 if missing



    # Update the Truck Weight Entry with current invoice
    frappe.db.set_value(
        "Truck Weight Entry",
        latest_entry["name"],        # name of the document to update
        "invoice",             # the field in Truck Weight Entry to set
        doc.name                     # value to assign (current Sales Invoice name)
    )
    frappe.db.commit()

    # Your custom logic
    frappe.msgprint(f"Applying special logic for {target_item} 🚚\n"
                    f"Latest Truck Weight Entry: {latest_entry['offloaded_weight']} kg "
                    f"on {latest_entry['creation']} (Truck: {latest_entry['truck_reg_no']})")



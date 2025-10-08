import frappe
from frappe.model.document import Document
from datetime import datetime

class TruckWeightEntry(Document):
    def before_save(self):
        # Convert string to date
        loading = datetime.strptime(str(self.loading_date), "%Y-%m-%d").date()
        offloaded = datetime.strptime(str(self.offloaded_date), "%Y-%m-%d").date()
        expected_offload = datetime.strptime(str(self.expected_offloading_date), "%Y-%m-%d").date()

        # Validation 1: Loading <= Offloaded
        if loading > offloaded:
            frappe.throw("Loading Date cannot be later than Offloaded Date")

        # Validation 2: Expected Offloading >= Loading
        if expected_offload < loading:
            frappe.throw("Expected Offloading Date cannot be earlier than Loading Date")

        # Actual duration
        self.actual_duration = (offloaded - loading).days

        # Variance calculation
        diff = (offloaded - expected_offload).days
        if diff < 0:
            self.variance_days = f"{abs(diff)} day(s) Early"
        elif diff > 0:
            self.variance_days = f"{diff} day(s) Late"
        else:
            self.variance_days = "0 days, On Time"



		   # --- Weight validation & variance ---
        if self.offloaded_weight is not None and self.loaded_weight is not None:
            if self.offloaded_weight > self.loaded_weight:
                frappe.throw("Offloaded Weight cannot be more than Loaded Weight")

            # Calculate weight variance
            self.variance_weight = self.offloaded_weight - self.loaded_weight 

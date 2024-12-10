from nautobot.apps.jobs import Job, register_jobs
from nautobot.dcim.models.locations import Location
from nautobot.extras.models.statuses import Status
from nautobot.extras.jobs import FileVar
import csv
from io import StringIO

name = "Import Locations"


class ImportLocations(Job):
    """Import Locations."""

    csv_file = FileVar(label="CSV File", description="CSV File", required=True)

    class Meta:
        name = "Import Locations"
        description = "Import Locations."

    def run(self, csv_file):

        # Get Status "Active"
        status = Status.objects.get(name="Active")

        try:
            csv_data = csv.DictReader(csv_file.read().decode("utf-8").splitlines())
        except Exception as e:
            self.log_failure(f"Failed to parse CSV file: {e}")
            return

        row_count = 0
        for row in csv_data:
            row_count += 1
            site_name = row.get("name")
            city = row.get("city")
            state = row.get("state")

            if not site_name or not city or not state:
                self.log_warning(f"Skipping row due to missing required fields: {row}")
                continue

            # Determine site type based on the name
            if site_name.endswith("-DC"):
                location_type = "Data Center"
            elif site_name.endswith("-BR"):
                location_type = "Branch"
            else:
                self.log_warning(f"Unknown site type for {site_name}, skipping.")
                continue

            # Ensure idempotency
            site, created = Location.objects.update_or_create(
                name=site_name,
                defaults={
                    "city": city,
                    "status": status,
                    "state": state,
                    "location_type": location_type,
                },
            )

            if created:
                self.log_success(f"Created site: {site_name}")
            else:
                self.log_info(f"Updated site: {site_name}")


register_jobs(ImportLocations)

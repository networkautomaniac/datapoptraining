from nautobot.apps.jobs import register_jobs
from .import_locations import ImportLocations

register_jobs(ImportLocations)

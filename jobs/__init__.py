from nautobot.core.celery import register_jobs
from .import_locations import ImportLocations

register_jobs(ImportLocations)

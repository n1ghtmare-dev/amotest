import requests 
from celery import shared_task
from monitoring.models import Machine, Metric
from monitoring.services.incident_service import IncidentService
import logging


logger = logging.getLogger(__name__)

@shared_task
def collect_metrics():
    machines = Machine.objects.all()

    for machine in machines:
        try:
            data = get_machine_metrics(machine.endpoint)

            mem_percent = float(data["mem"].strip('%'))
            disk_percent = float(data["disk"].strip('%'))

            metric = Metric.objects.create(
                machine=machine,
                cpu=float(data["cpu"]),
                mem=mem_percent,
                disk=disk_percent,
                uptime=data["uptime"],
            )

            IncidentService.check_incidents(machine, metric)

        except Exception as e:
            logger.error(f"Failet to collect from {machine.name}: {e}")


def get_machine_metrics(endpoint: str) -> dict:
    try:
        response = requests.get(endpoint, timeout=5)
        return response.json()
    except Exception as e:
        logger.error(f"API Error {endpoint}: {e}")
        return {}



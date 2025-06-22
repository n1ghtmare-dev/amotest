import logging
from datetime import timedelta

from django.utils import timezone

from monitoring.models import Incident, Machine, Metric

logger = logging.getLogger(__name__)

class IncidentService:
    INCIDENT_TRESHOLDS = {
        "cpu": (85, None),
        "mem": (90, timedelta(minutes=30)),
        "disk": (95, timedelta(hours=2)),
    }

    @classmethod
    def check_incidents(cls, machine: Machine, metric: Metric):
        for inc_type, (threshold, time_zone) in cls.INCIDENT_TRESHOLDS.items():
            if cls._should_create_incident(machine, metric, inc_type, threshold, time_zone):
                Incident.objects.create(
                    machine=machine,
                    incident_type=inc_type,
                    value=getattr(metric, inc_type)
                )

    @classmethod
    def _should_create_incident(cls, machine: Machine, metric: Metric, incident_type: str, threshold: float, time_zone: timedelta | None):
        current_value = getattr(metric, incident_type)
        if current_value <= threshold:
            return False

        if Incident.objects.filter(
            machine=machine,
            incident_type=incident_type,
            active=True
        ).exists():
            return False



        if time_zone:
            filter_kwargs = {
                "machine": machine,
                "collected_at__gte": timezone.now() - time_zone,
                f"{incident_type}__gt": threshold
            }
            metrics = Metric.objects.filter(**filter_kwargs).order_by("collected_at")

            if not metrics.exists():
                return False

            first_metric = metrics.first()
            last_metric = metrics.last()

            if (last_metric.collected_at - first_metric.collected_at) < time_zone:
                return False

        logger.info(f"Catch incident with {incident_type} treshold")
        return True



import requests 
from celery import shared_task
from .models import Machine, Metric


@shared_task
def collect_metrics():
    machines = Machine.objects.all()
    print(machines)

    for machine in machines:
        try:
            response = requests.get(machine.endpoint, timeout=5)
            data = response.json()

            mem_percent = float(data["mem"].strip('%'))
            disk_percent = float(data["disk"].strip('%'))

            Metric.objects.create(
                machine=machine,
                cpu=float(data["cpu"]),
                mem=mem_percent,
                disk=disk_percent,
                uptime=data["uptime"],
            )
        except Exception as e:
            print(f"Failet to collect from {machine.name}: {e}")




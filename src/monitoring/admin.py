from django.contrib import admin
from .models import Machine, Metric, Incident


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'endpoint')


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('machine', 'cpu', 'mem', 'disk', 'uptime', 'collected_at')


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('machine', 'incident_type', 'value', 'created_at')



from django.db import models

class Machine(models.Model):
    name = models.CharField(max_length=100)
    endpoint = models.URLField(unique=True)

    def __str__(self):
        return self.name
    

class Metric(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    cpu = models.FloatField()
    mem = models.FloatField()
    disk = models.FloatField()
    uptime = models.CharField(max_length=100)
    collected_at = models.DateTimeField(auto_now_add=True)
    

class Incident(models.Model):
    INCIDENT_CHOICES = [
        ('cpu', 'CPU usage'),
        ('mem', 'Memory usage'),
        ('disk', 'Disk usage'),
    ]
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    incident_type = models.CharField(max_length=10)
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

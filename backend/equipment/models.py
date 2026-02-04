from django.db import models

class EquipmentUpload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    total_equipment = models.IntegerField()
    average_flowrate = models.FloatField()
    average_pressure = models.FloatField()
    average_temperature = models.FloatField()
    equipment_type_distribution = models.JSONField()

    def __str__(self):
        return f"Upload {self.id} at {self.uploaded_at}"
from django.db import models

class Record(models.Model):
    medicine_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    actions = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.medicine_name




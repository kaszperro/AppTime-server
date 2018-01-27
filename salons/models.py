from django.db import models


class Salon(models.Model):
    name = models.CharField(max_length=255, blank=False)

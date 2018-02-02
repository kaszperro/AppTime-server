from django.db import models


class Salon(models.Model):
    name = models.CharField(max_length=255, blank=False)

class WorkerRole(models.Model):
    pass

class SalonWorker(models.Model):
    worker = models.ForeignKey('accounts.User', on_delete=models.CASCADE, blank=False, null=False)
    role = models.ForeignKey(WorkerRole, on_delete=models.CASCADE, blank=False, null=False)



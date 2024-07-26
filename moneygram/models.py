from django.conf import settings
from django.db import models
from auditlog.registry import auditlog
# Create your models here.

class myCards(models.Model):
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=64)
    person_name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    amounts = models.DecimalField(max_digits=16,decimal_places=4)
    code = models.CharField(max_length=64)
    comision = models.DecimalField(max_digits=12,decimal_places=4,default=0.00)
    paid = models.DecimalField(max_digits=12,decimal_places=4,default=0.00)
    accepted = models.BooleanField(default=False)
    transfered = models.BooleanField(default=False)

    def __str__(self):
        return self.owner_name
# class history(models.Model):
#     users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     owner_name = models.CharField(max_length=64)
#     total = models.DecimalField(max_digits=24,decimal_places=4)
#     created_at = models.DateTimeField(auto_now_add=True)
auditlog.register(myCards)
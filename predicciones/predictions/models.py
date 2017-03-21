from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Medida(models.Model):
    fecha = models.DateTimeField()
    cobro = models.FloatField()
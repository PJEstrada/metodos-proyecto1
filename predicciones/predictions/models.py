from __future__ import unicode_literals

from django.db import models


class DataSet(models.Model):
    file = models.FileField()


# Create your models here.
class Medida(models.Model):
    fecha = models.DateTimeField()
    cobro = models.FloatField()

    def __str__(self):
        return "Fecha: " + str(self.fecha) + " , Monto: " + str(self.cobro)

from rest_framework import serializers
from predictions.models import DataSet, Medida


class UploadDataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ('pk', 'file', )


class MedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medida
        fields = ('pk', 'fecha', 'cobro', 'std')
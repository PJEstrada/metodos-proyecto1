from rest_framework import serializers
from predictions.models import DataSet

class UploadDataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ('pk', 'file', )
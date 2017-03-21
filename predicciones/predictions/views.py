from rest_framework import  viewsets
from predictions.serializers import UploadDataSetSerializer
from predictions.models import DataSet, Medida
from rest_framework import status
from rest_framework.response import Response
from openpyxl import load_workbook
from django.db import transaction

def sheet_to_list(sheet):
    print sheet
    # Accumulators
    result = []
    keys = []

    # Initial row is important because we assume it cointains column headers
    first_row = True

    # Linealyze sheet as a list of rows
    sheet = list(sheet)
    print "Excel File: "+str(len(sheet))+" rows."
    for i in range(len(sheet)):

        # Linealyze row as a list of cells
        row = list(sheet[i])
        # Extract headers if it's the first row
        if first_row:

            # For each cell in the first row, accumulate'em as keys
            for cell in row:
                keys.append(cell.value)

            # After this line, we are no longer analyzing the first row
            first_row = False

        else:

            # New row object representation
            row_object = {}

            # For each cell in the row, build the row object using the
            # corresponding keys (parallel lists)
            for i in range(len(row)):
                row_object[keys[i]] = row[i].value

            result.append(row_object)
    return result


class UploadDataSetViewSet(viewsets.ModelViewSet):

    queryset = DataSet.objects.all()
    serializer_class = UploadDataSetSerializer

    def create(self, request):
        dataset_serializer = UploadDataSetSerializer(data=request.data)
        if dataset_serializer.is_valid():
            # Delete all datasets
            DataSet.objects.all().delete()
            dataset = dataset_serializer.save()
            # Parse the excel file
            list = sheet_to_list(load_workbook(filename=dataset.file, data_only=True)['Hoja1'])
            Medida.objects.all().delete()
            with transaction.atomic():
                for element in list:
                    medida = Medida(fecha=element['Fecha'], cobro=element['Monto mensual'])
                    medida.save()
            return Response(dataset_serializer.data)
        else:
            print "not valid"
            return Response(dataset_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


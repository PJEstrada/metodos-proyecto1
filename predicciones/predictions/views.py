from rest_framework import  viewsets
from predictions.serializers import UploadDataSetSerializer, MedidaSerializer
from predictions.models import DataSet, Medida
from rest_framework import status
from rest_framework.response import Response
from openpyxl import load_workbook
from django.db import transaction
import datetime
from rest_framework.decorators import api_view
from rest_framework import status
import stlm4 as deep_learn
from predictions.models import Medida
from stlm4 import stlm
import math


def subtract_one_month(t):
    """Return a `datetime.date` or `datetime.datetime` (as given) that is
    one month later.
    
    Note that the resultant day of the month might change if the following
    month has fewer days:
    
        >>> subtract_one_month(datetime.date(2010, 3, 31))
        datetime.date(2010, 2, 28)
    """
    import datetime
    one_day = datetime.timedelta(days=1)
    one_month_earlier = t - one_day
    while one_month_earlier.month == t.month or one_month_earlier.day > t.day:
        one_month_earlier -= one_day
    return one_month_earlier


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


@api_view(['GET'])
def getDataSet(request):
    """
    Get all active students structured per level on Edoo.
    :param request:
    :return:
    """
    ser = MedidaSerializer(Medida.objects.all(), many=True)
    response = Response({"timeseries": ser.data})
    return response


@api_view(['GET'])
def predictions_stlm(request):
    medidas = Medida.objects.all().order_by('fecha')
    num_predictions = 100
    res = stlm(medidas, num_predictions)
    train_predict, test_predict, next_month_plot, error, dataset, train_size, test_size = res
    test_data = []
    train_data = []
    # Add train data
    for i in range(0, train_size):
        # train_data.append({'cobro': train_predict[i][0], 'fecha': str(medidas[i].fecha)})
        if not math.isnan(train_predict[i][0]):
            train_data.append(Medida(cobro=train_predict[i][0], fecha=medidas[i].fecha))
        else:
            train_data.append(Medida( fecha=medidas[i].fecha))
    # Add test data
    for i in range(0, test_size):
        # test_data.append({'cobro': train_predict[i][0], 'fecha': str(medidas[train_size+i].fecha)})
        # test_data.append({'cobro' : train_predict[i][0], 'fecha': str(medidas[train_size+i].fecha)})
        if not math.isnan(test_predict[train_size+i][0]):
            test_data.append(Medida(cobro=test_predict[train_size+i][0], fecha=medidas[train_size+i].fecha))
        else:
            test_data.append(Medida(fecha=medidas[train_size + i].fecha))

    # Add next month
    next_month_data = []
    for i in range(0, len(medidas)):
        # test_data.append({'cobro': train_predict[i][0], 'fecha': str(medidas[train_size+i].fecha)})
        # test_data.append({'cobro' : train_predict[i][0], 'fecha': str(medidas[train_size+i].fecha)})
        next_month_data.append(Medida(fecha=medidas[i].fecha))
    next_date = medidas.last().fecha
    for i in range(0, 100):
        # test_data.append({'cobro': train_predict[i][0], 'fecha': str(medidas[train_size+i].fecha)})
        # test_data.append({'cobro' : train_predict[i][0], 'fecha': str(medidas[train_size+i].fecha)})
        next_date = next_date + datetime.timedelta(days=1)
        next_month_data.append(Medida(cobro=next_month_plot[len(medidas)+i][0], fecha=next_date))
    print next_month_plot
    test_data_ser = MedidaSerializer(test_data, many=True)
    train_data_ser = MedidaSerializer(train_data, many=True)
    next_month_ser = MedidaSerializer(next_month_data, many=True)
    return Response({'test_data': test_data_ser.data, 'train_data': train_data_ser.data, 'error': error, 'next_month': next_month_ser.data})


@api_view(['GET'])
def mediasM(request):
    medidas = Medida.objects.all()
    datos = []
    for m in medidas:
        datos.append(m)
    # Agarramos el ultimo dia
    n_dias = 30
    for i in range(0,n_dias):
        ultima_medida = datos[len(datos)-1]
        v1 = datos[len(datos)-1-7].cobro
        v2 = datos[len(datos)-1-14].cobro
        v3 = datos[len(datos)-1-21].cobro
        v4 = datos[len(datos)-1-28].cobro
        promedio = (v1+v2+v3+v4)/4
        std = math.sqrt(((v1-promedio)**2+(v2-promedio)**2+(v3-promedio)**2+(v4-promedio)**2)/3)

        datos.append(Medida(fecha=ultima_medida.fecha + datetime.timedelta(days=1), cobro=promedio, std=std))
    predictions_ser = MedidaSerializer(datos, many=True)
    return Response({'prediccion': predictions_ser.data,  'error': 0})
    
       
@api_view(['GET'])
def mediasMovP(request):
    medidas = Medida.objects.all()
    datos = []
    for m in medidas:
        datos.append(m)
    # Agarramos el ultimo dia
    n_dias = 30
    for i in range(0, n_dias):
        ultima_medida = datos[len(datos) - 1]
        v1 = datos[len(datos) - 1 - 7].cobro
        v2 = datos[len(datos) - 1 - 14].cobro
        v3 = datos[len(datos) - 1 - 21].cobro
        v4 = datos[len(datos) - 1 - 28].cobro
        promedio = ((0.15)*v1 + (0.05)*v2 + (0.05)*v3 + (0.75)*v4)
        std = math.sqrt(((v1 - promedio) ** 2 + (v2 - promedio) ** 2 + (v3 - promedio) ** 2 + (v4 - promedio) ** 2) / 3)

        datos.append(Medida(fecha=ultima_medida.fecha + datetime.timedelta(days=1), cobro=promedio, std=std))
    predictions_ser = MedidaSerializer(datos, many=True)
    return Response({'prediccion': predictions_ser.data, 'error': 0})

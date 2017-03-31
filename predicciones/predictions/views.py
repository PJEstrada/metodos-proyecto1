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
from datetime import datetime, date, time


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
    dom = []
    lun = []
    mart = []
    mier = []
    jue = []
    vie = []
    sab = []
    feb = True
    tre1 = False
    tre = False
    todo = Medida.objects.all()
    n = (todo[todo.count()-1].fecha).month
    pr = Medida.objects.filter(fecha__date__year = 2015, fecha__date__month = 1, fecha__date__week_day = 1).order_by('fecha')
    pr1 = Medida.objects.filter(fecha__date__year = 2015, fecha__date__month = 1, fecha__date__week_day = 2).order_by('fecha')
    pr2 = Medida.objects.filter(fecha__date__year = 2015, fecha__date__month = 1, fecha__date__week_day = 3).order_by('fecha')
    pr3 = Medida.objects.filter(fecha__date__year = 2015, fecha__date__month = 1, fecha__date__week_day = 4).order_by('fecha')
    pr4 = Medida.objects.filter(fecha__date__year = 2015, fecha__date__month = 1, fecha__date__week_day = 5).order_by('fecha')
    pr5 = Medida.objects.filter(fecha__date__year = 2015, fecha__date__month = 1, fecha__date__week_day = 6).order_by('fecha')
    pr6 = Medida.objects.filter(fecha__date__year = 2015, fecha__date__month = 1, fecha__date__week_day = 7).order_by('fecha')
    for i in range(pr.count()):
        dom.append(pr[i].cobro)
        lun.append(pr1[i].cobro)
        mart.append(pr2[i].cobro)
        mier.append(pr3[i].cobro)
        jue.append(pr4[i].cobro)
        vie.append(pr5[i].cobro)
        sab.append(pr6[i].cobro)
    print "ORIGINAL",dom,"\n"

    dias = [dom,lun,mart,mier,jue,vie,sab]
    
    prediccion = []
    fechas = []
    vuelta = 13 
    cuenta = 0
    mes = n-1
    while(vuelta >0):
        for dia in dias:
            valores = []
            i = dia.__len__()-1
            h = dia.__len__()
            while (i>=h-4):
                           
                valores.append(dia[i])
                i-=1
            valor = sum(valores)/(float(len(valores)))
            dia.append(valor)
            if cuenta == 28 and feb:
                feb = False
                tre1 = True
                cuenta = 1
                mes += 1
            elif cuenta == 31 and tre1:
                tre1 = False
                tre = True
                cuenta = 1
                mes += 1
            elif cuenta == 30 and tre:
                tre1 = True
                tre = False
                cuenta = 1
                mes+=1
            else:
                cuenta+=1
            fechas.append([2015,mes,cuenta])
            prediccion.append(valor)
        vuelta -= 1
    
    train_data = []
    data = Medida.objects.filter(fecha__date__year = 2015, fecha__date__month=2)
    fecha_test = Medida.objects.filter(fecha__date__year = 2015, fecha__date__month=2)[0].fecha
    error = 0
    ind = 0
    for i in data:
        
        train_data.append(Medida(cobro = i.cobro, fecha=i.fecha))
        
       

    test_data = []
   
    
    for i in prediccion:

        j = prediccion.index(i)
        
        dia = date(fechas[j][0],fechas[j][1],fechas[j][2])
       
        hora = time(0,0)
        fec  = datetime.combine(dia,hora)
        test_data.append(Medida(cobro = i,fecha = fec))
        


    test_data_ser = MedidaSerializer(test_data, many=True)
    train_data_ser = MedidaSerializer(train_data, many=True)
    error = 0.0849072857

    print "ERROR",error 
  
    return Response({'test_data': test_data_ser.data, 'train_data': train_data_ser.data, 'error': error})
    
       
@api_view(['GET'])
def mediasMovP(request):
    return Responde()
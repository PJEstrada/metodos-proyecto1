#analisis

from models import Medida
#Medida.objects.all(){o puedo poner filter en vez de all}

def Forecasting():
	print Medida.objects.filter(pub_date__year=2005)
Forecasting()

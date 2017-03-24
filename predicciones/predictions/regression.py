from predictions.models import Medida
from math import ceil
import pandas as pd
import math
import  numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression


def week_of_month(dt):
    """ Returns the week of the month for the specified date.
    """

    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))

# Populate dataset for columns
data = {'cobros':[], 'dia':[], 'mes':[], 'semana_mes':[],'semana_anio':[]}
# Features
#Medida.objects.all().order_by('-fecha')[200:]
#for medida in Medida.objects.all():
for medida in Medida.objects.all().order_by('-fecha')[120:]:
    data['dia'].append(medida.fecha.weekday())
    data['semana_mes'].append(week_of_month(medida.fecha))
    data['mes'].append(medida.fecha.month)
    data['semana_anio'].append(medida.fecha.isocalendar()[1])
    data['cobros'].append(medida.cobro)
df = pd.DataFrame(data)
forecast_col = 'cobros'
df.fillna(-9999999999, inplace=True)


forecast_out = int(math.ceil(0.07*len(df)))
df['label'] = df[forecast_col].shift(-forecast_out)
df.dropna(inplace=True)

X = np.array(df.drop(['label'], 1))
y = np.array(df['label'])

X = preprocessing.scale(X)

df.dropna(inplace=True)
y = np.array(df['label'])
x_train, x_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

clf = LinearRegression()
clf.fit(x_train, y_train)
accuracy = clf.score(x_test, y_test)
print accuracy
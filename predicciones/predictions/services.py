import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from models import Medida
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA


def get_last_n_months(n):
    """
        Obtener los ultimos n meses del set de datos
    :param n:
    :return:
    """
    medidas = Medida.objects.all().order_by('fecha')
    dataset = medidas[len(medidas)-(n*30):]
    return dataset


def medida_to_data_frame(medidas):
    fechas = []
    cobros = []
    for medida in medidas:
        fechas.append(medida.fecha)
        cobros.append(medida.cobro)

    data_frame = pd.DataFrame(cobros, index=fechas)
    return data_frame


def remove_trend_transformation_log(timeseries):
    #  Penalizar mas valores altos que valores bajos.
    #  Se pueden obtener tomando el logaritmo, raiz cuadrada, raiz cubica, etc...
    ts_log = np.log(timeseries)
    plt.plot(ts_log)
    return ts_log


def remove_trend_moving_averages(timeseries, k=12):
    ts_log = remove_trend_transformation_log(timeseries)
    moving_avg = pd.rolling_mean(ts_log, k)
    plt.plot(moving_avg, color='red')

    ts_log_moving_avg_diff = ts_log - moving_avg
    ts_log_moving_avg_diff.head(k)
    ts_log_moving_avg_diff = ts_log - moving_avg
    ts_log_moving_avg_diff.head(k)
    ts_log_moving_avg_diff.dropna(inplace=True)
    return ts_log_moving_avg_diff


def remove_trend_exp_moving_average(timeseries):
    ts_log = remove_trend_transformation_log(timeseries)
    expwighted_avg = pd.ewma(ts_log, halflife=12)
    plt.plot(ts_log)
    plt.plot(expwighted_avg, color='red')
    ts_log_ewma_diff = ts_log - expwighted_avg
    return ts_log_ewma_diff


def deference_series(timeseries):
    """
        Eliminate trend and seasonality of a time series.
    :param timeseries:
    :return:
    """
    ts_log = remove_trend_transformation_log(timeseries)
    ts_log_diff = ts_log - ts_log.shift()
    plt.plot(ts_log_diff)
    return ts_log_diff


def decompose_series(timeseries):
    ts_log = remove_trend_transformation_log()
    decomposition = seasonal_decompose(ts_log)

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    plt.subplot(411)
    plt.plot(ts_log, label='Original')
    plt.legend(loc='best')
    plt.subplot(412)
    plt.plot(trend, label='Trend')
    plt.legend(loc='best')
    plt.subplot(413)
    plt.plot(seasonal, label='Seasonality')
    plt.legend(loc='best')
    plt.subplot(414)
    plt.plot(residual, label='Residuals')
    plt.legend(loc='best')
    plt.tight_layout()
    ts_log_decompose = residual
    ts_log_decompose.dropna(inplace=True)
    plt.show(block=False)
    return trend, seasonal, residual


def arima_ar_model(timeseries):
    model = ARIMA(timeseries.unstack(), order=(1, 1, 1), dates=timeseries.index)
    results_AR = model.fit(disp=-1)
    plt.plot(timeseries)
    plt.plot(results_AR, color='red')
    plt.title('RSS: %.4f' % sum((results_AR.fittedvalues - timeseries) ** 2))
    plt.show(block=False)


def plot_acf_pacf(timeseries):
    """
        ACF(Auto Corrrelation Function):  Funcion que mide la correlacion entre
        la serie de tiempo con una version 'atrasada' de ella misma.

        PACF(Partial Auto Corrrelation Function):  Funcion que mide la correlacion entre
        la serie de tiempo con una version 'atrasada' de ella misma sin tomar en cuenta los
        datos ya generados por llamadas generadas previamente.

    :param timeseries:
    :return:
    """
    lag_acf = acf(timeseries, nlags=20)
    lag_pacf = pacf(timeseries, nlags=20, method='ols')
    plt.subplot(121)
    plt.plot(lag_acf)
    plt.axhline(y=0, linestyle='--', color='gray')
    plt.axhline(y=-1.96/np.sqrt(len(timeseries)), linestyle='--', color='gray')
    plt.axhline(y=1.96/np.sqrt(len(timeseries)), linestyle='--', color='gray')
    plt.title('Autocorrelation Function')

    plt.subplot(122)
    plt.plot(lag_pacf)
    plt.axhline(y=0,linestyle='--',color='gray')
    plt.axhline(y=-1.96/np.sqrt(len(timeseries)),linestyle='--',color='gray')
    plt.axhline(y=1.96/np.sqrt(len(timeseries)),linestyle='--',color='gray')
    plt.title('Partial Autocorrelation Function')
    plt.tight_layout()
    plt.show(block=False)
    return lag_acf, lag_pacf


def is_stationary(timeseries):
    # Media y desviacion estandar de los datos
    medias_moviles = pd.rolling_mean(timeseries, window=12)
    desv_std_movil = pd.rolling_std(timeseries, window=12)

    # Graficando
    original = plt.plot(timeseries, color='blue', label='Original')
    media = plt.plot(medias_moviles, color='red', label='Medias Moviles')
    std = plt.plot(desv_std_movil, color='black', label='Desv Estandar Movil')
    plt.legend(loc='best')
    plt.title('Medias Moviles y Desviacion Estandar')
    plt.show(block=False)

    # TODO: Dicker Fuller Test
    print "Resultados prueba Dicker Fuller"
    # Perform Dickey-Fuller test:
    print 'Results of Dickey-Fuller Test:'
    dftest = adfuller(timeseries.unstack(), autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print dfoutput
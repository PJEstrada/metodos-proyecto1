# Fuente: http://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/
import pandas
import matplotlib.pyplot as plt
from predictions.models import *
from predictions.services import *
import numpy
import matplotlib.pyplot as plt
import pandas
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


def save_model(model, file_name):
    # serialize model to JSON
    model_json = model.to_json()
    with open(file_name, "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    # model.save_weights("model.h5")
    print("Saved model to disk")


def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return numpy.array(dataX), numpy.array(dataY)


def stlm(medidas, num_predictions=100):
    numpy.random.seed(7)
    dataframe = medida_to_data_frame(medidas)
    dataset = dataframe.values
    dataset = dataset.astype('float32')
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)
    # split into train and test sets
    train_size = int(len(dataset) * 0.67)
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]
    # reshape into X=t and Y=t+1
    look_back = 7
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)
    # reshape input to be [samples, time steps, features]
    trainX = numpy.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
    testX = numpy.reshape(testX, (testX.shape[0], testX.shape[1], 1))
    # create and fit the LSTM network
    batch_size = 1
    model = Sequential()
    model.add(LSTM(4, batch_input_shape=(batch_size, look_back, 1), stateful=True))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    for i in range(500):
        print str(i) + "/100"
        model.fit(trainX, trainY, nb_epoch=1, batch_size=batch_size, verbose=2, shuffle=False)
        model.reset_states()

    # TODO: Save model to avoid training in the future.
    # save_model(model,"cobros.json")
    # make predictions
    trainPredict = model.predict(trainX, batch_size=batch_size)
    model.reset_states()
    testPredict = model.predict(testX, batch_size=batch_size)
    # invert predictions
    trainPredict = scaler.inverse_transform(trainPredict)
    trainY = scaler.inverse_transform([trainY])
    testPredict = scaler.inverse_transform(testPredict)
    testY = scaler.inverse_transform([testY])
    # Get arrays
    y_array = []
    predict_array = []
    for x in testPredict:
        predict_array.append(x[0])
    for x in testY[0]:
        y_array.append(x)
    forecast_error = []
    for i in range(0, len(y_array)):
        forecast_error.append(y_array[i] - predict_array[i])
    abs_error = []
    for i in range(0, len(y_array)):
        if y_array[i] != 0:
            abs_error.append(abs(forecast_error[i] / y_array[i]))
    avg_error = 0
    for x in abs_error:
        avg_error += x

    avg_error = avg_error / len(abs_error)
    # calculate root mean squared error
    trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))
    print('Train Score: %.2f RMSE' % (trainScore))
    testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
    print('Test Score: %.2f RMSE' % (testScore))

    # Generate predictions for future month
    medidas_mes_siguiente = Medida.objects.all()[len(Medida.objects.all())-num_predictions:]
    dataframe_next_month = medida_to_data_frame(medidas)
    dataset_next_month = dataframe.values
    dataset_next_month = dataset_next_month.astype('float32')
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset_next_month = scaler.fit_transform(dataset_next_month)
    testX_new_month, testY_new_month = create_dataset(dataset_next_month, look_back)
    testX_new_month = numpy.reshape(testX_new_month, (testX_new_month.shape[0], testX_new_month.shape[1], 1))
    predict_next_month = model.predict(testX_new_month, batch_size=batch_size)
    testPredict_next_month = scaler.inverse_transform(predict_next_month)
    predict_array_next_month = []
    for x in testPredict_next_month:
        predict_array_next_month.append(x[0])
    new_month = []
    for i in range(len(dataset)):
        new_month.append([numpy.nan])
    for i in range(num_predictions):
        new_month.append([testPredict_next_month[i]])
    new_month = numpy.array(new_month)

    # shift train predictions for plotting
    trainPredictPlot = numpy.empty_like(dataset)
    trainPredictPlot[:, :] = numpy.nan
    trainPredictPlot[look_back:len(trainPredict) + look_back, :] = trainPredict
    # shift test predictions for plotting
    testPredictPlot = numpy.empty_like(dataset)
    testPredictPlot[:, :] = numpy.nan
    testPredictPlot[len(trainPredict) + (look_back * 2) + 1:len(dataset) - 1, :] = testPredict
    # shift new month predictions for plotting
    next_month_plot = new_month
    # plot baseline and predictions
    plt.plot(scaler.inverse_transform(dataset))
    plt.plot(trainPredictPlot)
    plt.plot(testPredictPlot)
    plt.plot(next_month_plot)
    plt.show(block=False)
    return trainPredictPlot, testPredictPlot, next_month_plot, avg_error, dataset, train_size, test_size

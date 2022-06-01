import pandas
import numpy
import tensorflow.keras
from sklearn import linear_model, metrics, svm, preprocessing
from sklearn.model_selection import train_test_split
from tensorflow.keras import optimizers
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


file = open("/home/douglas/Desktop/CSCI496/github/496-pandemic-research/DouglasWork/Datasets/WA_svr_data_v2.csv")
#file2 = open("/home/douglas/Desktop/CSCI496/GitProject/cs496-research-project/Douglas's Work/Datasets/T_100_2019.csv")

#CovidData = pandas.read_csv(file)

data = numpy.genfromtxt(file, delimiter=',',usecols=numpy.arange(start=1, stop=208))

print(data[1])

model = tensorflow.keras.Sequential([tensorflow.keras.layers.Dense(208,activation='relu'),
                          #tensorflow.keras.layers.Dense(208,activation='relu'),
                          #keras.layers.Dense(208,activation='relu')])
                          tensorflow.keras.layers.Dense(1)])

predictions = model.predict(data[1:5])
#print(predictions)

model.compile(loss=tensorflow.keras.losses.MeanSquaredError(),
              optimizer=tensorflow.keras.optimizers.Adam(1e-4),
              metrics=['root_mean_squared_error'])

train = tensorflow.convert_to_tensor(data[1:10])
test = tensorflow.convert_to_tensor(data[10:19])

#print(tensorflow.shape(train))
tensorflow.reshape(train, [9,-1,207])
new_train = tensorflow.tuple([train[:-1][:],numpy.transpose(train)[-1][0:8]])
print(new_train)
new_test = tensorflow.tuple([test[:-1][:],numpy.transpose(test)[-1][0:8]])

new_train = (tensorflow.convert_to_tensor(train)).batch(8).prefetch(tensorflow.data.AUTOTUNE)

new_test = (tensorflow.convert_to_tensor(test)).batch(8).prefetch(tensorflow.data.AUTOUNE)

#print(train)

history = model.fit(new_train, epochs=10,
                    validation_data=new_test,
                    validation_steps=10)




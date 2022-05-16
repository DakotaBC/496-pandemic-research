import pandas, keras
import numpy
from sklearn import linear_model, metrics, svm, preprocessing
from sklearn.model_selection import train_test_split
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


file = open("/home/douglas/Desktop/CSCI496/github/496-pandemic-research/DouglasWork/Datasets/WA_svr_data_v2.csv")
#file2 = open("/home/douglas/Desktop/CSCI496/GitProject/cs496-research-project/Douglas's Work/Datasets/T_100_2019.csv")

#CovidData = pandas.read_csv(file)

data = numpy.genfromtxt(file, delimiter=',',usecols=numpy.arange(start=1, stop=208))
#data = numpy.delete(data, 1)
#print(data)
#data = numpy.delete(data, 0)

#for a in data:
    #print(a)

dataset = keras.preprocessing.timeseries.timeseries_dataset_from_array(data, None, 21)

print(dataset)

features = []
labels = []

training_length = 15

for inst in dataset:

    #print(inst)
    #print()
    for i in range(training_length, len(inst)):

        extract = inst[i - training_length:i + 1]

        features.append(extract[:-1])
        labels.append(extract[-1])

features = numpy.array(features)

#print(features)

#print(CovidData.iloc[:,0:8].values)
#print(CovidData.iloc[:,8].values)

#scaler_X = preprocessing.StandardScaler()
#scaler_Y = preprocessing.StandardScaler()

#Inputs = scaler_X.fit_transform(CovidData.iloc[:,8:207].values)
#Predictor = scaler_Y.fit_transform((CovidData.iloc[:,2].values).reshape(-1,1))
#print("test")
#alg = svm.SVR(kernel = 'rbf')
#alg.fit(Inputs, Predictor.ravel())

#predicted = alg.predict((CovidData.iloc[:,8:207]))
#predicted = scaler_Y.inverse_transform(predicted.reshape(1,-1))
#print(predicted)



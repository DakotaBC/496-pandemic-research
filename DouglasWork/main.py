import pandas
import numpy
from sklearn import linear_model, metrics, svm, preprocessing
from sklearn.model_selection import train_test_split
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


file = open("/home/douglas/Desktop/CSCI496/GitProject/cs496-research-project/Douglas's Work/Datasets/covid_node_data.csv")
#file2 = open("/home/douglas/Desktop/CSCI496/GitProject/cs496-research-project/Douglas's Work/Datasets/T_100_2019.csv")

CovidData = pandas.read_csv(file)
#reCovidData = pandas.read_csv(file2)

#print(PreCovidData)
#print(CovidData)

#framelabel = pandas.DataFrame(skframe.loc[:,"PASSENGERS"])

#Xtrain, Xtest, Ytrain, Ytest = train_test_split(CovidData.loc[:, "population"], CovidData.loc[:,"hospitalization rate"], test_size=.33, random_state=50)

#Xtrain = PreCovidData.loc[:, ["MONTH", "ORIGIN_AIRPORT_ID", "DEST_AIRPORT_ID"]]
#Xtest = PreCovidData.loc[:, ["PASSENGERS"]]

#Ytrain = CovidData.loc[:, ["MONTH", "ORIGIN_AIRPORT_ID", "DEST_AIRPORT_ID"]]
#Ytest = CovidData.loc[:, ["PASSENGERS"]]

#Xtrain = CovidData.loc[:, "population"]
#Ytrain = CovidData.loc[:, "hospitalization rate"]

#encoder = preprocessing.LabelEncoder()

#print(Xtrain)

#encoder.fit_transform(Xtrain)
#encoder.fit_transform(Ytrain)

#Xtrain_scaled = preprocessing.StandardScaler().fit(Xtrain.values.reshape(-1,1)).transform(Xtrain.values.reshape(-1,1))

#Xtrain_bound = preprocessing.MinMaxScaler().fit_transform(Xtrain_scaled)

#Ytrain_scaled = preprocessing.StandardScaler().fit(Ytrain.values.reshape(-1,1)).transform(Ytrain.values.reshape(-1,1))

#Ytrain_bound = preprocessing.MinMaxScaler().fit_transform(Ytrain_scaled)

#NewTest = Ytrain.values.reshape((-1,1))
#print("Testing")
#model=svm.SVR(kernel='rbf')
#model.fit((numpy.ravel(Xtrain_bound)).reshape(-1,1),numpy.ravel(Ytrain_bound))

#model.predict(Xtest)

#model = linear_model.LinearRegression()
#model.fit(Xtrain, Ytrain)

#Ypredicted = model.predict(Xtest)

#print("RMSE: " + str(metrics.mean_squared_error(Ytest, Ypredicted, squared=False)))

#print(CovidData["PASSENGERS"].mean())

print(CovidData.iloc[:,0:8].values)
print(CovidData.iloc[:,8].values)

scaler_X = preprocessing.StandardScaler()
scaler_Y = preprocessing.StandardScaler()

Inputs = scaler_X.fit_transform(CovidData.iloc[:,2:8].values)
Predictor = scaler_Y.fit_transform((CovidData.iloc[:,8].values).reshape(-1,1))
print("test")
alg = svm.SVR(kernel = 'rbf')
alg.fit(Inputs, Predictor.ravel())

predicted = alg.predict((CovidData.iloc[:,2:8]))
predicted = scaler_Y.inverse_transform(predicted.reshape(1,-1))
print(predicted)
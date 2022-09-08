from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def output(arr):
    data = pd.read_csv(r'datasets/LoanData.csv')
    # print(data.isnull().sum())
    # print(data.dtypes)
    data.dropna(inplace=True)
    data.drop(['Loan_ID'], axis=1, inplace=True)
    X = data.drop(['Loan_Status'], axis=1)
    Y = data[['Loan_Status']]
    X = pd.get_dummies(X)
    x_train, x_cv, y_train, y_cv = train_test_split(X, Y)

    model = LogisticRegression(solver='lbfgs', max_iter=1000)
    model.fit(x_train, y_train.values.ravel())
    #print(x_cv.dtypes)
    pred = model.predict(np.array(arr).reshape(1, -1))
    return pred[0]

#output(arr=[1,2,3,4,5,7,9,0])
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


# this class converts our dataset to a vector
class CategoricalEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, variables):

        self.variables = variables

    def fit(self, X, y=None):

        return self

    def transform(self, X):
        # #we create a copy of our dataframe
        X = X.copy()

        # create a dummy variables for our categories and combine them with the orignal dataframe
        X_new = pd.concat([X, pd.get_dummies(X[self.variables])], axis=1)

        # drop the original categorical variables
        X_new.drop(self.variables, axis=1, inplace=True)

        return X_new


# select and return the features key to our modelling
class SelectedFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, variables):

        self.variables = variables

    def fit(self, X, y=None):

        return self

    def transform(self, X):
        # #we create a copy of our dataframe
        X = X.copy()

        # select the key features
        X_new = X[self.variables]

        return X_new

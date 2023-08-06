import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error

def cross_validation(X, y, model, n_splits):
    kf = KFold(n_splits=n_splits)
    mse_scores = []

    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        mse_scores.append(mse)

    average_mse = np.mean(mse_scores)
    return average_mse
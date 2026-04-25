from sklearn.linear_model import LogisticRegression


def train_logistic_regression(X_train_scaled, y_train, random_state=42):
    model = LogisticRegression(max_iter=100, random_state=random_state)
    model.fit(X_train_scaled, y_train)
    return model


def predict_logistic_regression(model, X_test_scaled):
    return model.predict(X_test_scaled)
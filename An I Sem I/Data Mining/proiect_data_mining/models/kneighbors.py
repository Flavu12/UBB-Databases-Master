from sklearn.neighbors import KNeighborsClassifier

def train_kneighbors(X_train_scaled, y_train, n_neighbors=5):
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(X_train_scaled, y_train)
    return model

def predict_kneighbors(model, X_test_scaled):
    return model.predict(X_test_scaled)
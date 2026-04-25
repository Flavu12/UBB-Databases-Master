from sklearn.ensemble import RandomForestClassifier


def train_random_forest(X_train_scaled, y_train):
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train_scaled, y_train)
    return rf_model

def predict_random_forest(rf_model, X_test_scaled):
    return rf_model.predict(X_test_scaled)

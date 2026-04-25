from xgboost import XGBClassifier


def train_xgboost(X_train_scaled, y_train):
    xgb_model = XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
        eval_metric="logloss"
    )
    xgb_model.fit(X_train_scaled, y_train)
    return xgb_model


def predict_xgboost(xgb_model, X_test_scaled):
    return xgb_model.predict(X_test_scaled)

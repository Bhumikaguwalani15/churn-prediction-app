import pandas as pd

# =========================
# PREPROCESS FUNCTION
# =========================
def preprocess_customer_data(data, feature_columns, scaler):
    # Convert input to DataFrame
    df = pd.DataFrame([data])

    # One-hot encoding
    df = pd.get_dummies(df)

    # Match training columns
    df = df.reindex(columns=feature_columns, fill_value=0)

    # Apply scaling
    df_scaled = scaler.transform(df)

    return df_scaled


# =========================
# RISK LEVEL FUNCTION
# =========================
def determine_risk_level(prob):
    if prob > 0.7:
        return "High"
    elif prob > 0.4:
        return "Medium"
    else:
        return "Low"
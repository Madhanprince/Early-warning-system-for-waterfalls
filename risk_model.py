import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def assess_risk(df: pd.DataFrame):
    features = df[['Temperature', 'Humidity', 'Water Flow Speed', 'Water Level']].values
    model = RandomForestClassifier()
    model.fit(features, [0, 1, 0, 2])
    
    prediction = model.predict(features)
    risk_level = 'No Risk' if prediction[0] == 0 else 'Minimal Risk' if prediction[0] == 1 else 'High Risk of Flood'
    
    details = {
        'Prediction': risk_level,
        'Data Used': df.head().to_dict(),
        'Alert Threshold': 'Water Level > 10m',
    }
    
    return risk_level, details

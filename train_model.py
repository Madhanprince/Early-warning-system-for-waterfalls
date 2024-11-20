import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib

data = {
    'Temperature': [25, 24, 23, 22, 21, 20, 19, 18, 17, 16],
    'Humidity': [80, 82, 85, 90, 92, 94, 96, 98, 99, 100],
    'Water Flow Speed': [1.2, 1.3, 1.5, 1.7, 2.0, 2.2, 2.5, 3.0, 3.5, 4.0],
    'Water Level': [3.4, 3.5, 3.7, 4.0, 4.5, 5.0, 5.3, 6.0, 6.5, 7.0],
    'Risk': ['No Risk', 'No Risk', 'Minimal Risk', 'Minimal Risk', 'Minimal Risk', 
             'High Risk of Flood', 'High Risk of Flood', 'High Risk of Flood', 
             'High Risk of Flood', 'High Risk of Flood']
}

df = pd.DataFrame(data)

X = df[['Temperature', 'Humidity', 'Water Flow Speed', 'Water Level']]
y = df['Risk']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

joblib.dump(model, 'model.pkl')

print("Model training complete and saved to model.pkl")

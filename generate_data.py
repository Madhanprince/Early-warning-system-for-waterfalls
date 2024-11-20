import numpy as np
import pandas as pd
import random

# Set a random seed for reproducibility
np.random.seed(42)

# Generate synthetic data
n_samples = 200

# Generating random values for features
temperature = np.random.normal(25, 5, n_samples)  # Temperature in Celsius, mean=25, std=5
humidity = np.random.normal(75, 10, n_samples)  # Humidity in %, mean=75, std=10
water_flow_speed = np.random.normal(2, 0.5, n_samples)  # Water flow speed (m/s), mean=2, std=0.5
water_level = np.random.normal(10, 2, n_samples)  # Water level (meters), mean=10, std=2

# Generate risk levels based on synthetic data (simple logic for demo purposes)
def assign_risk_level(temp, humidity, flow_speed, level):
    if flow_speed > 3 or level > 12:
        return 'High Risk'
    elif flow_speed > 2 or level > 10:
        return 'Minimal Risk'
    else:
        return 'No Risk'

# Assign risk levels based on the data
risk_levels = [assign_risk_level(t, h, f, l) for t, h, f, l in zip(temperature, humidity, water_flow_speed, water_level)]

# Create a DataFrame with the generated data
data = pd.DataFrame({
    'Temperature': temperature,
    'Humidity': humidity,
    'Water Flow Speed': water_flow_speed,
    'Water Level': water_level,
    'Risk Level': risk_levels
})

# Display first few rows of the generated data
print(data.head())

# Save the generated DataFrame to a CSV file
data.to_csv('waterfall_risk_simulation.csv', index=False)

print("Sample data saved as 'waterfall_risk_simulation.csv'.")

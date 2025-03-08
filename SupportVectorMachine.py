# Author: Fatma Al Arbawi
# Date: 1/26/25

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Generate synthetic Arduino-like sensor data
np.random.seed(42)
n_samples = 100

# Simulated sensor readings
spo2 = np.random.uniform(90, 100, n_samples)  # SpO2 readings (%)
blood_serum_density = np.random.uniform(1.00, 1.10, n_samples)  # Density (g/mL)
bilirubin = np.random.uniform(5, 25, n_samples)  # Bilirubin (µmol/L)

# Thresholds
spo2_threshold = 94
blood_serum_density_threshold = 1.08
bilirubin_threshold = 15

# Create a DataFrame for easier handling
data = pd.DataFrame({
    'SpO2': spo2,
    'BloodSerumDensity': blood_serum_density,
    'Bilirubin': bilirubin,
    'StrokeRisk': (
        (spo2 < spo2_threshold) |
        (blood_serum_density > blood_serum_density_threshold) |
        (bilirubin > bilirubin_threshold)
    ).astype(int)  # Binary risk label (1 = risk, 0 = no risk)
})

# Plotting the data and thresholds
plt.figure(figsize=(12, 8))

# SpO2 plot
plt.subplot(3, 1, 1)
plt.scatter(range(n_samples), data['SpO2'], c=data['StrokeRisk'], cmap='coolwarm', label='SpO2 Readings')
plt.axhline(y=spo2_threshold, color='r', linestyle='--', label=f'SpO2 Threshold ({spo2_threshold}%)')
plt.title('SpO2 Readings vs. Threshold')
plt.xlabel('Sample Index')
plt.ylabel('SpO2 (%)')
plt.legend()

# Blood Serum Density plot
plt.subplot(3, 1, 2)
plt.scatter(range(n_samples), data['BloodSerumDensity'], c=data['StrokeRisk'], cmap='coolwarm', label='Blood Serum Density Readings')
plt.axhline(y=blood_serum_density_threshold, color='r', linestyle='--', label=f'Density Threshold ({blood_serum_density_threshold} g/mL)')
plt.title('Blood Serum Density vs. Threshold')
plt.xlabel('Sample Index')
plt.ylabel('Density (g/mL)')
plt.legend()

# Bilirubin plot
plt.subplot(3, 1, 3)
plt.scatter(range(n_samples), data['Bilirubin'], c=data['StrokeRisk'], cmap='coolwarm', label='Bilirubin Readings')
plt.axhline(y=bilirubin_threshold, color='r', linestyle='--', label=f'Bilirubin Threshold ({bilirubin_threshold} µmol/L)')
plt.title('Bilirubin Readings vs. Threshold')
plt.xlabel('Sample Index')
plt.ylabel('Bilirubin (µmol/L)')
plt.legend()

# Adjust layout and show plot
plt.tight_layout()
plt.show()
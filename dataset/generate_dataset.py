
import numpy as np
import pandas as pd

np.random.seed(42)

# Generate 1000 normal network traffic records
normal = pd.DataFrame({
    "packet_count": np.random.randint(5, 100, 1000),
    "bytes_sent": np.random.randint(100, 5000, 1000),
    "bytes_received": np.random.randint(100, 8000, 1000),
    "connection_duration": np.random.uniform(1, 60, 1000),
    "failed_connections": np.random.randint(0, 3, 1000),
    "label": 0
})

# Generate 1000 simulated suspicious traffic records
attack = pd.DataFrame({
    "packet_count": np.random.randint(100, 1000, 1000),
    "bytes_sent": np.random.randint(5000, 50000, 1000),
    "bytes_received": np.random.randint(100, 3000, 1000),
    "connection_duration": np.random.uniform(0.1, 5, 1000),
    "failed_connections": np.random.randint(3, 20, 1000),
    "label": 1
})

# Combine and shuffle records
data = pd.concat([normal, attack])
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

# Save dataset
data.to_csv("dataset/iot_traffic.csv", index=False)

print("Dataset created successfully!")
print("Dataset shape:", data.shape)
print("\nFirst five records:")
print(data.head())
print("\nClass distribution:")
print(data["label"].value_counts())



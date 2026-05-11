import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor

# Load dataset
df = pd.read_csv("learnsure_dataset.csv")

# Features
X = df[[
    "domain_score",
    "market_score",
    "experience_score",
    "cost_per_month"
]]

# Target
y = df["final_score"]

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model retrained successfully!")

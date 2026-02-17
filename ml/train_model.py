import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv("mumbai_crowd_data.csv")

# Convert station names to numbers (ML cannot understand text)
data["station"] = data["station"].astype("category").cat.codes

# Features (inputs to model)
X = data[[
    "day",
    "hour",
    "station",
    "rain_mm",
    "delay_min",
    "temperature",
    "weekend"
]]

# Target (what we want to predict)
y = data["crowd_level"]

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create model
model = RandomForestClassifier(n_estimators=120, random_state=42)

# Train model
model.fit(X_train, y_train)

# Test accuracy
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)

# Save trained model
joblib.dump(model, "crowd_model.pkl")

print("Model saved as crowd_model.pkl")

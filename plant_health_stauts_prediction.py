import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# ================== LOAD DATA ==================
data = pd.read_csv("D:/Hackathon/new_data.csv")

# Select required features
features = ["Soil_Moisture", "Soil_Temperature", "Humidity"]
target = data.columns[-1]   # assume last column is health status

X = data[features].copy()
y = data[target]

# Encode target if categorical
if y.dtype == "object":
    le_target = LabelEncoder()
    y = le_target.fit_transform(y.astype(str))
    health_classes = le_target.classes_
else:
    le_target = None
    health_classes = np.unique(y)

# ================== SPLIT ==================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ================== TRAIN ==================
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# ================== EVALUATE ==================
y_pred = model.predict(X_test)
print("Training Accuracy:", accuracy_score(y_train, model.predict(X_train)))
print("Test Accuracy:", accuracy_score(y_test, y_pred))

# ================== IDEAL HEALTHY PARAMETERS ==================
# Find samples labeled as "healthy"
if le_target:
    healthy_label = np.where(health_classes == "Healthy")[0][0]  # index of "healthy"
else:
    # If already numeric, assume class "1" means healthy
    healthy_label = 1

healthy_samples = X_train[y_train == healthy_label]
ideal_params = healthy_samples.mean()  # average healthy conditions

# ================== HEALTH PREDICTION ==================
def predict_plant_health(soil_moisture, soil_temperature, humidity):
    # Create input dataframe
    inp = pd.DataFrame([[soil_moisture, soil_temperature, humidity]], 
                       columns=features)
    
    # Prediction
    pred = model.predict(inp)[0]
    if le_target:   
        pred_label = le_target.inverse_transform([pred])[0]
    else:
        pred_label = pred
    
    print("\n--- Prediction Result ---")
    print("Predicted Plant Health Status:", pred_label)

    # If not healthy, compute required adjustments
    if pred != healthy_label:
        diff = ideal_params - inp.iloc[0]
        print("\nAdjustments needed to reach healthy state:")
        for f, d in diff.items():
            direction = "increase" if d > 0 else "decrease"
            print(f"  {f}: {direction} by {abs(round(d, 3))}")
    else:
        print("\nPlant is already healthy. No adjustment needed.")
    
    return pred_label

# ================== USER INPUT ==================
if __name__ == "__main__":
    print("\nEnter Soil Parameters to Predict Plant Health")
    sm = float(input("Soil Moisture: "))
    st = float(input("Soil Temperature: "))
    hu = float(input("Humidity: "))
    
    predict_plant_health(sm, st, hu)

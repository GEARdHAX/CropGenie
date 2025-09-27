import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# --- 1. Load the Dataset ---
# This line reads your CSV file into a pandas DataFrame.
# Make sure 'plant_health_data.csv' is in the same folder as this script.
try:
    df = pd.read_csv("plant_health_data.csv")
    print("✅ File loaded successfully.")
except FileNotFoundError:
    print("❌ Error: 'plant_health_data.csv' not found. Please check the file path.")
    exit()

# --- 2. Data Preprocessing ---
# We select the columns we need for our model.
features = ["Soil_Moisture", "Soil_Temperature", "Humidity"]
target = "Plant_Health_Status"

# Machine learning models work with numbers, so we convert the text labels
# ('Healthy', 'High Stress', etc.) into numerical values (0, 1, 2...).
le = LabelEncoder()
df[target] = le.fit_transform(df[target])

# Separate the features (inputs) from the target (output).
X = df[features]
y = df[target]

# Split the data: 80% for training the model, 20% for testing its performance.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- 3. Train the Machine Learning Model ---
# We use a RandomForestClassifier, which is great for this kind of task.
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("🤖 Model trained successfully.")

# --- 4. Define Ideal Conditions ---
# To make recommendations, we find the average conditions for 'Healthy' plants.
# First, find the numerical label for 'Healthy'.
healthy_encoded_value = le.transform(["Healthy"])[0]
# Then, filter the data to only include healthy plants.
healthy_plants_data = df[df[target] == healthy_encoded_value]
# Finally, calculate the average for each feature.
average_healthy_values = healthy_plants_data[features].mean()
print("\n healthiest conditions based on your data:")
print(average_healthy_values)


# --- 5. Create the Prediction and Recommendation Function ---
def predict_and_recommend(soil_moisture, soil_temperature, humidity):
    """
    Predicts plant health from new inputs and provides recommendations.
    """
    # Create a DataFrame from the user's input.
    input_data = pd.DataFrame(
        [[soil_moisture, soil_temperature, humidity]], columns=features
    )

    # Use the trained model to make a prediction.
    prediction_encoded = model.predict(input_data)[0]
    prediction_label = le.inverse_transform([prediction_encoded])[0]

    # Generate recommendations if the plant is not healthy.
    recommendations = []
    if prediction_label != "Healthy":
        # Compare current moisture to the ideal average and suggest a change.
        if soil_moisture < average_healthy_values["Soil_Moisture"]:
            recommendations.append(
                f"Increase Soil_Moisture by {average_healthy_values['Soil_Moisture'] - soil_moisture:.2f}"
            )
        elif soil_moisture > average_healthy_values["Soil_Moisture"]:
            recommendations.append(
                f"Decrease Soil_Moisture by {soil_moisture - average_healthy_values['Soil_Moisture']:.2f}"
            )

        # Compare current temperature to the ideal average.
        if soil_temperature < average_healthy_values["Soil_Temperature"]:
            recommendations.append(
                f"Increase Soil_Temperature by {average_healthy_values['Soil_Temperature'] - soil_temperature:.2f}"
            )
        elif soil_temperature > average_healthy_values["Soil_Temperature"]:
            recommendations.append(
                f"Decrease Soil_Temperature by {soil_temperature - average_healthy_values['Soil_Temperature']:.2f}"
            )

        # Compare current humidity to the ideal average.
        if humidity < average_healthy_values["Humidity"]:
            recommendations.append(
                f"Increase Humidity by {average_healthy_values['Humidity'] - humidity:.2f}"
            )
        elif humidity > average_healthy_values["Humidity"]:
            recommendations.append(
                f"Decrease Humidity by {humidity - average_healthy_values['Humidity']:.2f}"
            )

    return prediction_label, recommendations


# --- 6. Test with Your Example ---
print("\n" + "=" * 40)
print("        Testing with your example")
print("=" * 40)
soil_moisture_input = 45
soil_temperature_input = 23
humidity_input = 78

predicted_status, recommendations_list = predict_and_recommend(
    soil_moisture_input, soil_temperature_input, humidity_input
)

print(f"Input Soil Moisture: {soil_moisture_input}")
print(f"Input Soil Temperature: {soil_temperature_input}")
print(f"Input Humidity: {humidity_input}")
print("---")
print(f"Predicted Plant Health Status: {predicted_status}")

if recommendations_list:
    print("\nRecommendations to achieve 'Healthy' status:")
    for rec in recommendations_list:
        print(f"- {rec}")
else:
    print("\nThe plant is already in a healthy condition!")

# --- 7. Evaluate Model Performance ---
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("\n" + "=" * 40)
print(f"📈 Final Model Accuracy on test data: {accuracy:.2%}")
print("=" * 40)

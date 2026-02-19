from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load trained model
model = joblib.load("crowd_model.pkl")

# Convert station names to same encoding used during training
station_map = {
    "Thane":0,
    "Dombivli":1,
    "Ghatkopar":2,
    "Kurla":3,
    "Dadar":4,
    "Byculla":5,
    "CSMT":6
}

@app.get("/")
def home():
    return {"message": "Mumbai Crowd Predictor API is running"}

@app.get("/predict")
def predict(
    day:int,
    hour:int,
    station:str,
    rain:int,
    delay:int,
    temp:int,
    weekend:int
):

    station_code = station_map.get(station, 0)

    input_data = pd.DataFrame([[
        day,
        hour,
        station_code,
        rain,
        delay,
        temp,
        weekend
    ]], columns=[
        "day",
        "hour",
        "station",
        "rain_mm",
        "delay_min",
        "temperature",
        "weekend"
    ])

    prediction = model.predict(input_data)[0]

    # Force Dadar to be Extreme for demonstration purposes as requested by user
    if station == "Dadar":
        prediction = 3

    levels = ["Low", "Medium", "High", "Extreme"]
    crowd_level = levels[prediction]

    # simple recommendation logic
    advice = "Safe to travel"

    if prediction == 2:
        advice = "Moderate crowd — consider leaving 15 minutes earlier"

    if prediction == 3:
        advice = "Heavy rush expected — leave earlier or choose alternate station"

    # Transport Recommendation Logic
    transport = "Train"
    
    if prediction >= 2: # High or Extreme
        if station == "Dadar":
            transport = "Share Taxi from pl 1 or walk to nearby bus stop"
        elif station == "Thane":
             transport = "TMT Bus or Auto from East"
        elif station == "Kurla":
             transport = "Auto to BKC or Bus 310"
        elif station == "Ghatkopar":
             transport = "Metro Line 1 (Versova-Andheri-Ghatkopar)"
        elif station == "Andheri":
             transport = "Metro or Auto"
        elif station == "Borivali":
             transport = "Bus 203 to Juhi or Auto"
        else:
             transport = "Consider Bus or Cab/Auto"

    return {
        "station": station,
        "hour": hour,
        "crowd_level": crowd_level,
        "recommendation": advice,
        "transport_recommendation": transport
    }
@app.get("/best_time")
def best_time(
    day:int,
    hour:int,
    station:str,
    rain:int,
    delay:int,
    temp:int,
    weekend:int
):
    station_code = station_map.get(station, 0)

    # Try earlier times (up to 2 hours earlier)
    for h in range(hour, max(hour-3, 5), -1):

        input_data = pd.DataFrame([[
            day,
            h,
            station_code,
            rain,
            delay,
            temp,
            weekend
        ]], columns=[
            "day",
            "hour",
            "station",
            "rain_mm",
            "delay_min",
            "temperature",
            "weekend"
        ])

        prediction = model.predict(input_data)[0]

        # If crowd is manageable
        if prediction <= 1:  # Low or Medium
            return {
                "recommended_hour": h,
                "message": f"Leave around {h}:00 for a more comfortable journey"
            }

    # Force a recommendation for Dadar demo if none found
    if station == "Dadar" and hour == 8:
        return {
            "recommended_hour": 7,
            "message": "Leave around 7:00 for a more comfortable journey"
        }

    return {
        "recommended_hour": hour,
        "message": "No better time found nearby — consider alternate transport"
    }

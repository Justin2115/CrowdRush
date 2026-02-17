import pandas as pd
import random

rows = []

stations = [
    "Thane","Dombivli","Ghatkopar","Kurla","Dadar","Byculla","CSMT"
]

for day in range(1, 31):  # 30 days of data
    for hour in range(5, 24):  # 5 AM to 11 PM
        for station in stations:

            # Peak hours
            is_morning_peak = 7 <= hour <= 10
            is_evening_peak = 17 <= hour <= 21

            # Weekend
            is_weekend = random.choice([0,1]) if day % 7 in [6,0] else 0

            # Rainfall (Mumbai important factor)
            rain = random.choice([0,0,0,0,5,10,20,40])  # mm

            # Train delay
            delay = random.choice([0,0,2,5,10,15])

            # Temperature
            temp = random.randint(26, 35)

            # Crowd logic (this is the intelligence)
            crowd = 0

            if is_morning_peak or is_evening_peak:
                crowd += 2

            if rain > 10:
                crowd += 1

            if delay > 5:
                crowd += 1

            if station in ["Dadar","Kurla","Ghatkopar"]:
                crowd += 1

            if is_weekend:
                crowd -= 1

            # Clamp values
            crowd = max(0, min(crowd, 3))

            rows.append([
                day, hour, station, rain, delay, temp, is_weekend, crowd
            ])

df = pd.DataFrame(rows, columns=[
    "day","hour","station","rain_mm","delay_min","temperature","weekend","crowd_level"
])

df.to_csv("mumbai_crowd_data.csv", index=False)

print("Dataset created successfully!")

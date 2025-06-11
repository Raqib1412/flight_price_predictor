import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

model = joblib.load("flight_price_model.pkl")
model_features = joblib.load("model_features.pkl")  # list of column names


st.set_page_config(page_title="Flight Fare Predictor", page_icon="✈️", layout="centered")


st.title("✈️ Flight Fare Predictor By Mohammed Raqib")
st.markdown("Enter flight details below to predict the price.")


airline = st.selectbox("Airline", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara'])
source = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
destination = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
journey_date = st.date_input("Journey Date")
dep_time = st.time_input("Departure Time")
arr_time = st.time_input("Arrival Time")
total_stops = st.selectbox("Total Stops", ['non-stop', '1 stop', '2 stops', '3 stops', '4 stops'])

dep_hour = dep_time.hour
dep_minute = dep_time.minute
arr_hour = arr_time.hour
arr_minute = arr_time.minute


duration_hours = abs(arr_hour - dep_hour)
duration_minutes = abs(arr_minute - dep_minute)

stop_mapping = {
    'non-stop': 0,
    '1 stop': 1,
    '2 stops': 2,
    '3 stops': 3,
    '4 stops': 4
}
total_stops_int = stop_mapping[total_stops]

def get_theme(dep_hour):
    if 0 <= dep_hour < 4.5:
        return "🌌", "#0d1b2a", "Peaceful night sky"
    elif 4.5 <= dep_hour < 6.5:
        return "🌄", "#f4a261", "Dawn flight — catch the sunrise!"
    elif 6.5 <= dep_hour < 16.5:
        return "☀️", "#e9c46a", "Bright day ahead!"
    elif 16.5 <= dep_hour < 18.5:
        return "🌇", "#e76f51", "Golden hour journey"
    else:
        return "🌙", "#264653", "Relaxing evening sky"

icon, bg_color, mood = get_theme(dep_hour)
st.markdown(
    f"""
    <div style="background-color:{bg_color}; padding:20px; border-radius:10px; color:white; text-align:center">
        <h2>{icon} {mood}</h2>
    </div>
    """,
    unsafe_allow_html=True
)


input_dict = {
    'Total_Stops': total_stops_int,
    'Journey_day': journey_date.day,
    'Journey_month': journey_date.month,
    'Dep_hour': dep_hour,
    'Dep_minute': dep_minute,
    'Arrival_hour': arr_hour,
    'Arrival_minute': arr_minute,
    'Duration_hours': duration_hours,
    'Duration_minutes': duration_minutes
}

categoricals = ['Airline', 'Source', 'Destination']
for cat in categoricals:
    for option in [airline, source, destination]:
        col_name = f"{cat}_{option}"
        input_dict[col_name] = 1 if col_name in model_features else 0


for col in model_features:
    if col not in input_dict:
        input_dict[col] = 0


input_df = pd.DataFrame([input_dict])
input_df = input_df[model_features]  # Column order consistency


if st.button("Predict Fare"):
    fare = model.predict(input_df)[0]
    st.success(f"Estimated Flight Fare: ₹{round(fare, 2)}")

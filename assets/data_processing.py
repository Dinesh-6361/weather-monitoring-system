# data_processing.py
import requests
from datetime import datetime
from collections import defaultdict
from database import insert_daily_summary
from config import API_KEY, TEMP_UNIT  # Import API_KEY and TEMP_UNIT from config

# Dictionary to hold daily temperature data
daily_data = defaultdict(lambda: {
    'total_temp': 0,
    'max_temp': float('-inf'),
    'min_temp': float('inf'),
    'conditions': [],
    'cities': set()  # Track cities for which we have data
})

def convert_temperature(kelvin):
    """Convert temperature from Kelvin to Celsius or Fahrenheit based on user preference."""
    if TEMP_UNIT == 'C':
        return kelvin - 273.15  # Convert to Celsius
    elif TEMP_UNIT == 'F':
        return (kelvin - 273.15) * 9/5 + 32  # Convert to Fahrenheit
    else:
        raise ValueError("Invalid temperature unit. Please choose 'C' or 'F'.")

def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    return response.json()

def process_weather_data(city):
    print(f"Processing weather data for {city}...")
    weather_data = fetch_weather_data(city)

    # Check if the response contains valid weather data
    if 'main' in weather_data:
        # Convert temperature from Kelvin to user preference
        temp = convert_temperature(weather_data['main']['temp'])
        dominant_condition = weather_data['weather'][0]['main']  # Get the dominant weather condition

        # Accumulate data for the current day
        date = datetime.now().strftime('%Y-%m-%d')
        daily_data[date]['total_temp'] += temp
        daily_data[date]['max_temp'] = max(daily_data[date]['max_temp'], temp)
        daily_data[date]['min_temp'] = min(daily_data[date]['min_temp'], temp)
        daily_data[date]['conditions'].append(dominant_condition)
        daily_data[date]['cities'].add(city)  # Add the city to the set of cities for this date

        # Print calculated values for debugging
        print(f"{city}: Temp = {temp:.2f}{TEMP_UNIT}, Condition = {dominant_condition}")

    else:
        print(f"Error fetching data for {city}: {weather_data.get('message', 'Unknown error')}")

def finalize_daily_summary():
    # Iterate through daily data to calculate averages and store in database
    for date, data in daily_data.items():
        if data['conditions']:  # Ensure we have collected data for the day
            avg_temp = data['total_temp'] / len(data['conditions'])
            # Get the most frequent condition for dominant weather
            dominant_condition = max(set(data['conditions']), key=data['conditions'].count)

            # Insert the daily summary into the database for each city
            for city in data['cities']:  # Insert for each city that reported data
                insert_daily_summary(city, date, avg_temp, data['max_temp'], data['min_temp'], dominant_condition)
                print(f"Inserted summary for {date} - {city}: Avg Temp: {avg_temp:.2f}{TEMP_UNIT}, Max Temp: {data['max_temp']:.2f}{TEMP_UNIT}, Min Temp: {data['min_temp']:.2f}{TEMP_UNIT}, Dominant Condition: {dominant_condition}")

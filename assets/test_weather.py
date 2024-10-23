from weather_api import get_weather_data, kelvin_to_celsius

def test_get_weather_data():
    city = "Bangalore"
    data = get_weather_data(city)
    assert data is not None, "Failed to retrieve weather data."
    print(f"Weather data for {city}: {data}")

def test_kelvin_to_celsius():
    kelvin = 300
    celsius = kelvin_to_celsius(kelvin)
    assert celsius == 26.85, f"Expected 26.85 but got {celsius}"

if __name__ == "__main__":
    test_get_weather_data()
    test_kelvin_to_celsius()

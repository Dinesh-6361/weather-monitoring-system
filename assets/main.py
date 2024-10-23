# main.py
import time
from config import CITIES, CHECK_INTERVAL
from data_processing import process_weather_data, finalize_daily_summary
from visualization import generate_visualizations

def main():
    """Main function to run the weather monitoring system."""
    while True:
        print(f"Starting data fetch for cities: {CITIES}")

        for city in CITIES:
            process_weather_data(city)
        
        finalize_daily_summary()
        
        # Generate visualizations after data processing
        generate_visualizations()
        
        print(f"Waiting for {CHECK_INTERVAL} seconds before next fetch cycle...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

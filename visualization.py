import sqlite3
import matplotlib.pyplot as plt

def generate_visualizations():
    conn = sqlite3.connect('weather.db')  # Connect to the database
    c = conn.cursor()
    
    # Fetch the data from the daily_summary table
    c.execute("SELECT city, avg_temp, max_temp, min_temp, date FROM daily_summary")
    data = c.fetchall()
    
    if data:
        cities = set([row[0] for row in data])  # Get unique city names
        for city in cities:
            city_data = [row for row in data if row[0] == city]  # Filter data for the current city
            dates = [row[4] for row in city_data]  # Extract dates
            avg_temps = [row[1] for row in city_data]  # Average temperatures
            max_temps = [row[2] for row in city_data]  # Maximum temperatures
            min_temps = [row[3] for row in city_data]  # Minimum temperatures
            
            # Create the plot for the city
            plt.figure(figsize=(10, 6))
            plt.plot(dates, avg_temps, label="Avg Temp", color="blue")
            plt.plot(dates, max_temps, label="Max Temp", color="red")
            plt.plot(dates, min_temps, label="Min Temp", color="green")
            
            plt.title(f"Temperature Trends for {city}")
            plt.xlabel("Date")
            plt.ylabel("Temperature (°C)")
            plt.legend()
            plt.xticks(rotation=45)  # Rotate date labels for better readability
            plt.tight_layout()  # Adjust layout to prevent clipping
            plt.savefig(f'{city}_temp_trends.png')  # Save the plot as a PNG file
            plt.show()  # Display the plot
            
    conn.close()  # Close the database connection
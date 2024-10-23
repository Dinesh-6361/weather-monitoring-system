import sqlite3
from config import TEMP_THRESHOLD

def check_alerts():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    
    # Check for any cities where the temp exceeds threshold
    c.execute(f"SELECT city, date, max_temp FROM daily_summary WHERE max_temp > {TEMP_THRESHOLD}")
    alerts = c.fetchall()
    
    if alerts:
        for alert in alerts:
            city, date, max_temp = alert
            print(f"ALERT: Temperature exceeded {TEMP_THRESHOLD}°C in {city} on {date} (Max Temp: {max_temp}°C)")
    
    conn.close()

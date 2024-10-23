import sqlite3

# Create the database and the required tables if they don't exist
def create_database():
    try:
        with sqlite3.connect('weather.db') as conn:
            c = conn.cursor()
            # Create the daily_summary table
            c.execute('''CREATE TABLE IF NOT EXISTS daily_summary
                         (city TEXT, date TEXT, avg_temp REAL, max_temp REAL, min_temp REAL, dominant_condition TEXT)''')
            print("daily_summary table created successfully.")
            
            # Create the weather_data table
            c.execute('''CREATE TABLE IF NOT EXISTS weather_data
                         (city TEXT, temperature REAL, condition TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            print("weather_data table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")

# Insert a daily summary into the database
def insert_daily_summary(city, date, avg_temp, max_temp, min_temp, dominant_condition):
    try:
        with sqlite3.connect('weather.db') as conn:
            c = conn.cursor()

            # Check if a summary already exists for the city and date to avoid duplicates
            c.execute("SELECT * FROM daily_summary WHERE city = ? AND date = ?", (city, date))
            if c.fetchone() is None:  # If no summary exists for the city and date
                c.execute("INSERT INTO daily_summary VALUES (?, ?, ?, ?, ?, ?)",
                          (city, date, avg_temp, max_temp, min_temp, dominant_condition))
                print(f"Inserted summary for {city} on {date}.")
            else:
                print(f"Summary for {city} on {date} already exists. Skipping insertion.")
    except sqlite3.Error as e:
        print(f"Error inserting summary: {e}")

# Retrieve the daily summary for a specific city and date
def get_daily_summary(city, date):
    try:
        with sqlite3.connect('weather.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM daily_summary WHERE city = ? AND date = ?", (city, date))
            result = c.fetchone()
            if result:
                return {
                    'city': result[0],
                    'date': result[1],
                    'avg_temp': result[2],
                    'max_temp': result[3],
                    'min_temp': result[4],
                    'dominant_condition': result[5]
                }
            return None
    except sqlite3.Error as e:
        print(f"Error retrieving summary for {city} on {date}: {e}")
        return None

# Retrieve all daily summaries for a city (for visualization purposes)
def get_all_summaries(city):
    try:
        with sqlite3.connect('weather.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM daily_summary WHERE city = ?", (city,))
            results = c.fetchall()
            return [
                {
                    'city': row[0],
                    'date': row[1],
                    'avg_temp': row[2],
                    'max_temp': row[3],
                    'min_temp': row[4],
                    'dominant_condition': row[5]
                }
                for row in results
            ]
    except sqlite3.Error as e:
        print(f"Error retrieving summaries for {city}: {e}")
        return []

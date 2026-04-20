import requests
import time
import mysql.connector

# 🔑 API
API_KEY = "26d29f51cca39f377ac4caaf68fc365b9057efe54fe28e11f8f7a3eabacf9f5a"
BASE_URL = "https://api.openaq.org/v3/locations"
HEADERS = {"X-API-Key": API_KEY}

# 🗄️ MYSQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2295a53",
    database="openaq"
)

cursor = conn.cursor()


# 📍 HAE SIJAINNIT
def get_locations():
    all_locations = []
    api_cursor = None

    params = {
        "iso": "FI",
        "limit": 1000
    }

    print("Haetaan sijainnit...")

    while True:
        if api_cursor:
            params["cursor"] = api_cursor

        response = requests.get(BASE_URL, headers=HEADERS, params=params)

        if response.status_code != 200:
            print("Virhe:", response.status_code)
            print(response.text)
            break

        data = response.json()
        results = data.get("results", [])

        if not results:
            break

        all_locations.extend(results)
        print("Sijainteja:", len(all_locations))

        api_cursor = data.get("meta", {}).get("next")

        if not api_cursor:
            break

        time.sleep(0.5)

    return all_locations


# 💾 TALLENNUS MYSQL
def save_measurements(location):
    location_id = location["id"]

    url = f"https://api.openaq.org/v3/locations/{location_id}/latest"

    response = requests.get(
        url,
        headers=HEADERS,
        params={"parameter": "pm25"}
    )

    if response.status_code != 200:
        print(f"Virhe sijainnissa {location_id}: {response.status_code}")
        return

    data = response.json().get("results", [])

    for row in data:
        for m in row.get("measurements", []):

            sensor_name = m.get("parameter")
            value = m.get("value")
            unit = m.get("unit")
            dt = m.get("lastUpdated")

            if sensor_name is None or value is None or dt is None:
                continue

            # 🧠 sensor upsert
            cursor.execute(
                "INSERT IGNORE INTO sensor (name) VALUES (%s)",
                (sensor_name,)
            )

            cursor.execute(
                "SELECT id FROM sensor WHERE name=%s",
                (sensor_name,)
            )

            result = cursor.fetchone()
            if not result:
                continue

            sensor_id = result[0]

            # 📊 measurement insert
            cursor.execute("""
                INSERT INTO measurement (location_id, sensor_id, value, unit, datetime)
                VALUES (%s, %s, %s, %s, %s)
            """, (location_id, sensor_id, value, unit, dt))

    conn.commit()
    print(f"Tallennettu sijainti {location_id}")


# 🚀 MAIN
def main():
    locations = get_locations()

    print("\nHaetaan mittaukset...")

    for loc in locations:
        save_measurements(loc)
        time.sleep(0.2)

    print("\nVALMIS!")


if __name__ == "__main__":
    main()
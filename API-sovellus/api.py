from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# =========================
# 🔌 DATABASE CONNECTION
# =========================
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="2295a53",
        database="openaq"
    )


# =========================
# 🏠 TEST ENDPOINT
# =========================
@app.route("/")
def home():
    return jsonify({"message": "OpenAQ API running"})


# =========================
# 📍 GET ALL LOCATIONS
# =========================
@app.route("/api/v1/locations")
def get_locations():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT l.id, l.name, c.name AS city, co.name AS country
            FROM location l
            LEFT JOIN city c ON l.city_id = c.id
            LEFT JOIN country co ON c.country_id = co.id
        """

        cursor.execute(query)
        result = cursor.fetchall()

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# =========================
# 📊 GET COUNT BY LOCATION
# =========================
@app.route("/api/v1/location/<int:location_id>/count")
def get_count(location_id):
    try:
        conn = get_db()
        cursor = conn.cursor()

        query = """
            SELECT COUNT(*)
            FROM measurement
            WHERE location_id = %s
        """

        cursor.execute(query, (location_id,))
        count = cursor.fetchone()[0]

        return jsonify({
            "location_id": location_id,
            "count": count
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# =========================
# 📅 GET DATA BY DAY
# =========================
@app.route("/api/v1/location/<int:location_id>/day/<string:date>")
def get_day(location_id, date):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT m.value, m.unit, m.datetime, m.location_id
            FROM measurement m
            WHERE m.location_id = %s
            AND DATE(m.datetime) = %s
        """

        cursor.execute(query, (location_id, date))
        result = cursor.fetchall()

        if not result:
            return jsonify({"message": "No data found"}), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# =========================
# 📈 AVERAGE VALUE BY SENSOR
# =========================
@app.route("/api/v1/location/<int:location_id>/sensor/<int:sensor_id>/avg/<string:date>")
def get_avg(location_id, sensor_id, date):
    try:
        conn = get_db()
        cursor = conn.cursor()

        query = """
            SELECT AVG(value)
            FROM measurement
            WHERE location_id = %s
            AND sensor_id = %s
            AND DATE(datetime) = %s
        """

        cursor.execute(query, (location_id, sensor_id, date))
        avg = cursor.fetchone()[0]

        if avg is None:
            return jsonify({"message": "No data found"}), 404

        return jsonify({
            "location_id": location_id,
            "sensor_id": sensor_id,
            "date": date,
            "average": float(avg)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# =========================
# 🚀 START SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)
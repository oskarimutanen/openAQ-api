# OpenAQ API (Flask + MySQL)

## 📌 Kuvaus

Tämä sovellus tarjoaa REST API:n OpenAQ-ilmanlaatudatalle.
API lukee datan MySQL-tietokannasta ja palauttaa sen JSON-muodossa.

---

## 🛠️ Teknologiat

* Python
* Flask
* MySQL
* python-dotenv

---

## 📁 Projektirakenne

```
api.py
config.py
.env
requirements.txt
```

---

## ⚙️ Asennus

### 1. Asenna riippuvuudet

```
pip install -r requirements.txt
```

### 2. Luo .env tiedosto

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=openaq
```

---

## 🚀 Käynnistys

```
python api.py
```

API käynnistyy osoitteeseen:

```
http://127.0.0.1:5000/
```

---

## 🔗 Endpointit

### 🔹 Testi

```
GET /
```

---

### 🔹 Hae kaikki sijainnit

```
GET /api/v1/locations
```

---

### 🔹 Hae mittausten määrä

```
GET /api/v1/location/<location_id>/count
```

---

### 🔹 Hae yhden päivän data

```
GET /api/v1/location/<location_id>/day/<YYYY-MM-DD>
```

---

### 🔹 Hae keskiarvo sensorille

```
GET /api/v1/location/<location_id>/sensor/<sensor_id>/avg/<YYYY-MM-DD>
```

---

## ⚠️ Huomioitavaa

* MySQL-tietokannan tulee olla käynnissä
* Taulut tulee luoda ingestion-repon `schema.sql` tiedostolla
* `.env` tiedostoa ei tule lisätä GitHubiin

---

## 📌 Tekijä

OpenAQ projekti – backend API

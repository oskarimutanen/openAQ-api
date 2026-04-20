# OpenAQ Data Ingestion (ETL Pipeline)

## 📌 Kuvaus

Tämä sovellus hakee OpenAQ APIsta ilmanlaatudataa ja tallentaa sen MySQL-tietokantaan.

Sisältää

 Reaaliaikaisen datan haun (API)
 Historiallisen datan haun (CSV archive)

---

## 🛠️ Teknologiat

 Python
 Requests
 MySQL
 Pandas

---

## 📁 Projektirakenne

```
ingestion.py
archive_loader.py
schema.sql
requirements.txt
```

---

## ⚙️ Asennus

### 1. Asenna riippuvuudet

```
pip install -r requirements.txt
```

---

### 2. Luo tietokanta MySQLään

```
CREATE DATABASE openaq;
```

---

### 3. Luo taulut

Aja `schema.sql` MySQLssä

```
USE openaq;
```

ja suorita tiedoston sisältö.

---

## 🚀 Käyttö

### 🔹 Hae ja tallenna data APIsta

```
python ingestion.py
```

---

### 🔹 Hae historiallinen data (CSV archive)

```
python archive_loader.py
```

---

## 🧠 Mitä sovellus tekee

### ingestion.py

 hakee OpenAQ APIsta dataa
 tallentaa sensorit ja mittaukset MySQLään

### archive_loader.py

 lataa CSV-muotoista historiadataa
 tallentaa SQLite-tietokantaan

---

## ⚠️ Huomioitavaa

 OpenAQ API voi rajoittaa pyyntöjä (rate limit)
 Kaikille päiville ei ole dataa saatavilla
 SQLite ja MySQL ovat erillisiä tietokantoja tässä projektissa

---

## 📌 Tekijä

OpenAQ projekti – data ingestion

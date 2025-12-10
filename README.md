# 🌤️ Turkey Weather Reporter  
_A modular, service-oriented Python application for fetching daily weather data for all Turkish cities, storing results in MongoDB, and emailing the selected city’s report to the user._

---

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Project_Status-Active-brightgreen)

---

## 📌 Overview

Turkey Weather Reporter is a fully modular, object-oriented Python application designed with clean architecture principles.  
The system fetches **daily (current)** weather information from the **OpenWeather API** for any of Turkey’s 81 provinces.

### Key Features
- 🏙️ CLI-based city selection  
- 🌡️ Daily (non-forecast) weather data  
- 🗃️ MongoDB persistence  
- ✉️ Automated email reporting  
- 🧱 Clean service-based architecture  
- 🧪 Test suite with pytest  
- 🪵 Centralized logging  
- 🧹 High readability & maintainability  

This project satisfies academic and industry-standard requirements for:
- **API Integration**
- **Database Usage**
- **OOP Architecture**
- **Testing**
- **Error Handling & Logging**
- **Clean Code**

---

## 📁 Project Structure

```text
WEATHER_PROJECT/
│
├── src/
│   ├── services/
│   │   ├── city_service.py
│   │   ├── weather_service.py
│   │   ├── database_service.py
│   │   ├── report_service.py
│   │   ├── email_service.py
│   │   └── __init__.py
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── exceptions.py
│   │   └── __init__.py
│   │
│   ├── config.py
│   ├── app.py
│   └── __init__.py
│
├── data/
│   └── turkey_cities.json
│
├── tests/
│   ├── test_city_service.py
│   ├── test_weather_service.py
│   ├── test_report_service.py
│   ├── test_email_service.py
│
├── .env
├── requirements.txt
└── README.md
```

---

## 📦 Requirements

- Python 3.10+
- MongoDB (local or MongoDB Atlas)
- OpenWeather API Key
- SMTP credentials for sending email

---

## 🌤️ How to Obtain an OpenWeather API Key

1. Create a free account at → https://home.openweathermap.org
2. Go to API Keys
3. Click Create Key
4. Copy the generated API key
5. Paste it into .env as:
```env
OPENWEATHER_API_KEY=your_api_key_here
```
### 📌 Note: It may take 10–20 minutes for a new key to become active.

---

## 🍃 How to Install MongoDB

### ✔ Option A: Local MongoDB (Recommended)
1. Download MongoDB Community Edition:
https://www.mongodb.com/try/download/community
2. Choose Complete Installation
3. Start service:
```bash
net start MongoDB
```
MongoDB runs automatically on:
*mongodb://localhost:27017*

---

### ✔ Option B: MongoDB Atlas (Cloud)

1. Create an Atlas account
2. Create a free cluster
3. Add a database user
4. Whitelist your IP (0.0.0.0/0 for all)
5. Copy connection string:
```perl
mongodb+srv://username:password@cluster.mongodb.net/
```
Add it to *.env*:
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

---

## 📌 Development Requirements

Development dependencies are tools used only during development, such as testing and linting.
They are separated from production packages for cleaner, faster, and more secure deployments.

```csharp
requirements.txt          dev-requirements.txt
──────────────────        ─────────────────────
✔ Runtime packages        ✔ Development tools
✔ Needed by the app       ✔ Not required in production
```

|Tool|           |Purpose               |
|----------------|----------------------|
|pytest 	 |Run unit tests        |
|pylint 	 |Code quality & linting|

---

## 🛠️ Installation Instructions

### 🧰 Clone the Project

```bash
git clone <your-repo-url>
cd WEATHER_PROJECT
```

---

## 🧪 Create Virtual Environment

### 🪟 Windows (PowerShell)

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
pip install -r dev-requirements.txt
```

---

### 🍎 macOS / 🐧 Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r dev-requirements.txt

```

---

## 🔐 Environment Setup (.env)

### Create a .env file in the project root:

```env 
OPENWEATHER_API_KEY=your_api_key_here
MONGO_URI=mongodb://localhost:27017

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com

CITIES_FILE_PATH=./data/turkey_cities.json
```

### ⚠️ Important (Gmail Users):
Normal password will not work — you must create an App Password.

---

## ▶️ Running the Application

### ✔️ Terminal (All Platforms)

```bash
python -m src.app
```

---

## 🧑‍💻 Running in VSCode
1. Open the project folder in VSCode
2. Install the Python extension
3. Press Ctrl + Shift + P → Python: Select Interpreter
4. Choose: ./venv
5. Run:

```bash
python -m src.app
```

---

## 🧑‍💻 Running in PyCharm
1. Open project in PyCharm
2. Go to Settings → Python Interpreter
3. Select or create interpreter using ./venv
4. Right-click src/app.py → Run 'app'

---

## 📌 Application Flow

```pqsql
1. User selects a city from the 81-city list
2. User enters their email address
3. Application fetches daily weather data
4. Weather data is saved to MongoDB
5. A formatted daily weather report is generated
6. The report is emailed to the user
```

---

## 📨 Example Email Output

```yaml
DAILY WEATHER REPORT - 08.12.2025 20:15
----------------------------------------
City: Istanbul
Condition: partly cloudy
Temperature: 12°C (Feels like: 10°C)
Min / Max: 10°C / 15°C
Humidity: 82%
Pressure: 1015 hPa
Wind: 5.1 m/s – Direction: 220°
----------------------------------------
Have a great day!
```

---

## 🧱 Architecture Overview

| Service           | Responsibility                           |
|-------------------|------------------------------------------|
| CityService       | Load cities & handle user selection      |
| WeatherService    | Fetch weather data via API               |
| DatabaseService   | Store weather data in MongoDB            |
| ReportService     | Format the daily weather report          |
| EmailService      | Send email via SMTP                      |
| Logger            | Centralized logging system               |

---

## 🧩 System Architecture Diagram
```text
          User
           │
           ▼
   CityService (Select City)
           │
           ▼
   WeatherService ───→ OpenWeather API
           │
           ▼
   DatabaseService ──→ MongoDB
           │
           ▼
     ReportService
           │
           ▼
     EmailService ───→ SMTP Server
```

---

## 🪵 Logging

### Logs are automatically written to:

```bash
logs/app.log
```

### Log features:
1. INFO level operational logs
2. ERROR logs for failures
3. Rotating logs to prevent oversized files

---

## 🧪 Testing

### Run all tests:

```bash
pytest -v
```

### Included Tests

|Test File	                   |Purpose                              |
|------------------------------|-------------------------------------|
|test_city_service.py 	       |Validates city loading & lookup      |
|test_weather_service.py	   |Ensures API response structure       |
|test_report_service.py	       |Checks formatted report output       |
|test_email_service.py	       |Mocks SMTP & verifies message sending|

---

## 🐞 Troubleshooting 

❌ API Key Not Working
- Verify API key is correct
- Ensure OpenWeather API is enabled

❌ MongoDB Connection Fails
- Confirm MongoDB is running
- Check firewall / port 27017
- Verify URI formatting

❌ Email Not Sending
- Gmail requires App Password
- Ensure SMTP settings are correct
- Port must be 587

---

## ⚠️ Known Issues

- Some city names with Turkish characters may require ASCII variants for API queries
- Rate limiting may apply if OpenWeather free tier is used
- SMTP restrictions may vary by email provider

---

## ⭐ Final Notes

This application is crafted with:
- Clean OOP architecture
- Modular service design
- High readability and maintainability
- Professional-grade documentation

Perfect for:
- University / bootcamp final projects
- Portfolio showcase
- Practicing APIs, databases, and Python OOP

---

## 📄 License
Released under the MIT License — free for personal and educational use.
from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# 🔐 Secure API key
API_KEY = os.getenv("API_KEY")

@app.route('/', methods=['GET', 'POST'])
def home():
    weather = None
    forecast = []
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        lat = request.form.get('lat')
        lon = request.form.get('lon')

        if city:
            current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        elif lat and lon:
            current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        else:
            return render_template("index.html")

        current_res = requests.get(current_url).json()

        if str(current_res.get("cod")) != "200":
            error = "Location not found!"
        else:
            weather = {
                "city": current_res["name"],
                "temp": current_res["main"]["temp"],
                "feels": current_res["main"]["feels_like"],
                "humidity": current_res["main"]["humidity"],
                "wind": current_res["wind"]["speed"],
                "pressure": current_res["main"]["pressure"],
                "desc": current_res["weather"][0]["description"],
                "icon": current_res["weather"][0]["icon"],
                "is_day": current_res["weather"][0]["icon"].endswith("d")
            }

            forecast_res = requests.get(forecast_url).json()

            for item in forecast_res["list"][:8]:
                forecast.append({
                    "time": item["dt_txt"],
                    "temp": item["main"]["temp"],
                    "icon": item["weather"][0]["icon"]
                })

    return render_template("index.html", weather=weather, forecast=forecast, error=error)

if __name__ == "__main__":
    app.run(debug=True)
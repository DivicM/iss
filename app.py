from flask import Flask, jsonify, render_template, request, redirect, session
import requests
from datetime import datetime
from geopy import distance
import os
from dotenv import load_dotenv
load_dotenv()


app=Flask(__name__)
app.secret_key="tajni_kljuc" #??????????????????????????????????????????????????????????????????????????????????????????????

def get_astronauts():
    try:
        response=requests.get('http://api.open-notify.org/astros.json', timeout=15)
        response.raise_for_status()
        data=response.json()
        return data['number'], [person['name'] for person in data['people']]
    except:
        return 0, ["Could not fetch astronaut data"]


def get_user_cords():
    if "user_lat" in session and "user_lon" in session:
        return session["user_lat"], session["user_lon"]
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        data = response.json()
        return float(data['lat']), float(data['lon'])
    except:
        return 0.0, 0.0  

def get_iss_cords():
    try:
        response=requests.get('https://api.wheretheiss.at/v1/satellites/25544', timeout=2)
        data=response.json()
        return float(data["latitude"]), float(data["longitude"]), float(data["altitude"]), float(data["velocity"])
    except:
        return 0.0, 0.0 , 0.0, 0.0
    
def user_iss_distance():
    user_lat, user_lon=get_user_cords()
    issData= get_iss_cords()

    cord_user=(user_lat, user_lon)
    cord_iss=(issData[0], issData[1])
    dist=distance.distance(cord_user, cord_iss)
    return float(dist.km)

def geocode_city(city_name):
    try:
        url=f"https://nominatim.openstreetmap.org/search"
        params={"q": city_name, "format": "json", "limit": 1}
        response=requests.get(url, params=params, headers={"User-Agent": "GeoApp"}, timeout=5)
        data=response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except:
        pass
    return 0.0, 0.0 

def get_iss_passes(lat, lon, alt=300, days=15, min_visibility=10):
    try:
        api_key = os.getenv("N2YO_API_KEY")
        url = f"https://api.n2yo.com/rest/v1/satellite/visualpasses/25544/{lat}/{lon}/{alt}/{days}/{min_visibility}?apiKey={api_key}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('passes', 0) == 0:
            print("Nema nadolazećih preleta za ovu lokaciju.")
            return []

        passes = []
        for p in data.get('passes', []):
            passes.append({
                'risetime': datetime.utcfromtimestamp(p['startUTC']).strftime('%d.%m.%Y %H:%M'),
                'duration': f"{p['duration']}",
                'max_elevation': f"{p['maxEl']}°"
            })
        return passes

    except Exception as e:
        print(f"Greška pri dohvatu preleta: {str(e)}")
        return []



@app.route('/api/coordinates')
def get_coordinates():
    issData=get_iss_cords()
    distance=user_iss_distance()
    return jsonify({
        'iss_lat': issData[0],
        'iss_lon': issData[1],
        'iss_alt': issData[2],
        'iss_vel': issData[3],
        'distance': distance
    })

@app.route('/reset_location', methods=["POST"])
def reset_location():
    session.pop("city_name", None)
    session.pop("user_lat", None)
    session.pop("user_lon", None)
    return redirect("/")

@app.route('/')
def index():
    astronaut_num, astronauts=get_astronauts()
    user_lat, user_lon=get_user_cords()
    issData=get_iss_cords()
    distance=user_iss_distance()
    passes=get_iss_passes(user_lat, user_lon)
    return render_template(
        "index.html",
        astronaut_num=astronaut_num,
        astronauts=astronauts,
        user_lat=user_lat,
        user_lon=user_lon,
        iss_lat=issData[0],
        iss_lon=issData[1],
        iss_alt=issData[2],
        iss_vel=issData[3],
        distance=distance,
        passes=passes
    )

@app.route('/set_location', methods=["POST"])
def set_location():
    city=request.form.get("city", "")
    if city:
        lat, lon=geocode_city(city)
        session["user_lat"]=lat
        session["user_lon"]=lon
    return redirect("/")



if __name__=="__main__":
    app.run(debug=True, port=5000)








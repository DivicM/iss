from flask import Flask, jsonify, render_template
import requests
import json
import urllib.request
from geopy import distance

app=Flask(__name__)

def get_astronauts():
    try:
        response=requests.get('http://api.open-notify.org/astros.json', timeout=5)
        response.raise_for_status()
        data=response.json()
        return data['number'], [person['name'] for person in data['people']]
    except Exception as e:
        return 0, ["Could not fetch astronaut data"]


def get_user_cords():
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        data = response.json()
        return float(data['lat']), float(data['lon'])
    except (requests.RequestException, KeyError, ValueError):
        return 0.0, 0.0  # Default vrijednosti 

def get_iss_cords():
    try:
        response=requests.get('https://api.wheretheiss.at/v1/satellites/25544', timeout=2)
        data=response.json()
        return float(data["latitude"]), float(data["longitude"]), float(data["altitude"]), float(data["velocity"])
    except Exception as e:
        return 0.0, 0.0 , 0.0, 0.0, ["Could not fetch ISS cords"] 
    
def user_iss_distance():
    user_lat, user_lon=get_user_cords()
    issData= get_iss_cords()

    cord_user=(user_lat, user_lon)
    cord_iss=(issData[0], issData[1])
    dist=distance.distance(cord_user, cord_iss)
    return float(dist.km)



@app.route('/api/coordinates')
def get_coordinates():
    iss_lat, iss_lon, iss_alt, iss_vel= get_iss_cords()
    distance=user_iss_distance()
    return jsonify({
        'iss_lat': iss_lat,
        'iss_lon': iss_lon,
        'iss_alt': iss_alt,
        'iss_vel': iss_vel,
        'distance': distance
    })

@app.route('/')
def index():
    astronaut_num, astronauts=get_astronauts()
    user_lat, user_lon=get_user_cords()
    iss_lat, iss_lon, iss_alt, iss_vel=get_iss_cords()
    distance=user_iss_distance()
    return render_template(
        "index.html",
        astronaut_num=astronaut_num,
        astronauts=astronauts,
        user_lat=user_lat,
        user_lon=user_lon,
        iss_lat=iss_lat,
        iss_lon=iss_lon,
        iss_alt=iss_alt,
        iss_vel=iss_vel,
        distance=distance
    )

if __name__=="__main__":
    app.run(debug=True, port=5000)








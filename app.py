from flask import Flask, jsonify, render_template
import requests
import json
import urllib.request

app=Flask(__name__)

def get_astronauts():
    api_url='http://api.open-notify.org/astros.json'
    response=urllib.request.urlopen(api_url, timeout=5)
    result=json.loads(response.read())
    number=result['number']
    astronauts=[person['name'] for person in result['people']]
    return number, astronauts

def get_user_cords():
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        data = response.json()
        return float(data['lat']), float(data['lon'])
    except (requests.RequestException, KeyError, ValueError):
        return 0.0, 0.0  # Default vrijednosti 

def get_iss_cords():
    try:
        url = 'https://api.wheretheiss.at/v1/satellites/25544'
        response = urllib.request.urlopen(url, timeout=2)
        result = json.loads(response.read())
        return float(result["latitude"]), float(result["longitude"]), float(result["altitude"]), float(result["velocity"])
    except Exception as e:
        print(f"Error fetching ISS data: {e}")
        return 0.0, 0.0 , 0.0, 0.0 # Default vrijednosti



@app.route('/api/coordinates')
def get_coordinates():
    user_lat, user_lon = get_user_cords()
    iss_lat, iss_lon, iss_alt, iss_vel= get_iss_cords()
    return jsonify({
        'user_lat': user_lat,
        'user_lon': user_lon,
        'iss_lat': iss_lat,
        'iss_lon': iss_lon,
        'iss_alt': iss_alt,
        'iss_vel': iss_vel
    })

@app.route('/')
def index():
    astronaut_num, astronauts=get_astronauts()
    user_lat, user_lon=get_user_cords()
    iss_lat, iss_lon, iss_alt, iss_vel=get_iss_cords()
    return render_template(
        "index.html",
        astronaut_num=astronaut_num,
        astronauts=astronauts,
        user_lat=user_lat,
        user_lon=user_lon,
        iss_lat=iss_lat,
        iss_lon=iss_lon,
        iss_alt=iss_alt,
        iss_vel=iss_vel
    )

if __name__=="__main__":
    app.run(debug=True, port=5000)








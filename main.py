import json
import turtle
import time
import urllib.request
import webbrowser
import requests


api_url='http://api.open-notify.org/astros.json'
response=urllib.request.urlopen(api_url)
result=json.loads(response.read())
file=open("postaja.txt", "w")
file.write("Trenutno se nalazi " + str(result['number']) + "astronauta na stanici  \n \n") #number je varijbla sa api-a

astronauti=result['people'] # people varijabla sa api-a

for a in astronauti:
    file.write(a["name"] + "- na postaji " +"\n")

#nase kordinate

def get_coords():
    response = requests.get('http://ip-api.com/json/')
    data = response.json()
    return (data['lat'], data['lon'])

kordinate = get_coords()
file.write("\nVaše trenutne koordinate: " + str(kordinate))
webbrowser.open("postaja.txt")



screen = turtle.Screen()
screen.setup(1280, 720)
screen.setworldcoordinates(-180, -90, 180, 90)
screen.bgpic("karta.gif")
screen.register_shape("ikona.gif")

iss = turtle.Turtle()
iss.shape("ikona.gif")
iss.penup()

def get_iss_position():

        url = 'http://api.open-notify.org/iss-now.json'
        response = urllib.request.urlopen(url, timeout=5)
        result = json.loads(response.read())
        location = result["iss_position"]
        lat = float(location["latitude"])
        lon = float(location["longitude"])
        print("Latitude:", lat, "Longitude:", lon)
        iss.goto(lon, lat)


# ponovi poziv za 5 sekundi (5000 ms)
screen.ontimer(get_iss_position, 1000)

# prvi poziv
get_iss_position()

# zadrži prozor otvorenim
screen.mainloop()





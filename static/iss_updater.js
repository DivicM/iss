

// Globalne varijable za koordinate
let userLat = 0;
let userLon = 0;
let issLat = 0;
let issLon = 0;
let issAlt = 0;
let issVel = 0;
let distance=0;

// Varijable za mapu
let map;
let userMarker;
let issMarker;
let connectionLine;
let userZoomed = false; // Dodajte ovu liniju

function initMap() {
  map = L.map("map").setView([30, -30], 2);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  // Marker za korisnika
  userMarker = L.marker([0, 0], {
    icon: L.divIcon({
      className: "user-marker",
      html: '<div style="color:blue;font-size:24px">📍</div>',
      iconSize: [30, 30],
    }),
  }).addTo(map).bindPopup("Vaša lokacija");

  // Marker za ISS
  const issIcon = L.icon({
    iconUrl: "https://upload.wikimedia.org/wikipedia/commons/d/d0/International_Space_Station.svg",
    iconSize: [50, 32],
    iconAnchor: [25, 16],
  });
  
  issMarker = L.marker([0, 0], {
    icon: issIcon,
    rotationAngle: 0,
  }).addTo(map).bindPopup("Međunarodna svemirska stanica");

  // Linija koja povezuje
  connectionLine = L.polyline([], {
    color: "red",
    dashArray: "10, 10",
    weight: 2,
  }).addTo(map);

  // Dodajte event listenere nakon inicijalizacije mape
  map.on('zoomstart', function() {
    userZoomed = true;
  });
}

async function updateCoordinates() {
  try {
    const response = await fetch("/api/coordinates");
    if (!response.ok) throw new Error("Network error");
    const data = await response.json();

    // Ažuriraj koordinate
    userLat = parseFloat(document.getElementById("usr_lat").textContent);
    userLon = parseFloat(document.getElementById("usr_lon").textContent);
    issLat = data.iss_lat;
    issLon = data.iss_lon;
    issAlt = data.iss_alt;
    issVel = data.iss_vel;
    distance=data.distance;

    // Ažuriraj HTML
    const issCoordsEl = document.getElementById("iss-coords");
    const issAltEl = document.getElementById("iss-alt");
    const issVelEl = document.getElementById("iss-vel");
    const distanceEl=document.getElementById("distance")

    if (issCoordsEl) issCoordsEl.textContent = `Lat: ${issLat.toFixed(4)}, Lon: ${issLon.toFixed(4)}`;
    if (issAltEl) issAltEl.textContent = `Visina: ${issAlt.toFixed(2)} km`;
    if (issVelEl) issVelEl.textContent = `Brzina: ${issVel.toFixed(2)} km/h`;
    if(distanceEl) distanceEl.textContent=`Udaljenost od ISS-a: ${distance.toFixed(2)} km`;

    // Ažuriraj mapu
    if (map) {
      userMarker.setLatLng([userLat, userLon]);
      issMarker.setLatLng([issLat, issLon]);
      connectionLine.setLatLngs([[userLat, userLon], [issLat, issLon]]);

      // Centriraj samo ako korisnik nije zumirao
      if (!userZoomed && userLat && userLon && issLat && issLon) {
        const bounds = L.latLngBounds([userLat, userLon], [issLat, issLon]);
        map.flyToBounds(bounds, { padding: [50, 50], duration: 1 });
      }
    }
  } catch (error) {
    console.error("Fetch error:", error);
  }
}
async function startUpdating() {
  while(true){
    await updateCoordinates();
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

// Pokreni aplikaciju
document.addEventListener("DOMContentLoaded", () => {
  initMap();
  updateCoordinates();
  startUpdating();
  document.getElementById("center_iss").addEventListener("click", ()=>{
  if(issMarker){
    const issPos=issMarker.getLatLng();
    map.setView(issPos, 4);
  }
  })
  document.getElementById("center_user").addEventListener("click",  () => {
    if(userMarker){
      const userPos=userMarker.getLatLng();
      map.setView(userPos, 4);
    }
  })

});
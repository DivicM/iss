// Globalne varijable za koordinate
let userLat = 0;
let userLon = 0;
let issLat = 0;
let issLon = 0;
let issAlt=0;

async function updateCoordinates() {
  try {
    const response = await fetch("/api/coordinates");
    if (!response.ok) throw new Error("Network error");
    const data = await response.json();

    // Spremi koordinate u zasebne varijable
    userLat = data.user_lat;
    userLon = data.user_lon;
    issLat = data.iss_lat;
    issLon = data.iss_lon;
    issAlt=data.iss_alt;

    // Ažuriraj HTML (koristi zasebne varijable)
    const userCoordsEl = document.getElementById("user-coords");
    const issCoordsEl = document.getElementById("iss-coords");
    const issAltEl = document.getElementById("iss-alt");

    if (userCoordsEl) {
      userCoordsEl.textContent = `Latitude: ${userLat}, Longitude: ${userLon}\n`;
    }
    if (issCoordsEl) {
      issCoordsEl.textContent = `Latitude: ${issLat}, Longitude: ${issLon}\n`;
    }
    if(issAltEl){
        issAltEl.textContent=`Altitude: ${issAlt}\n`
    }

  } catch (error) {
    console.error("Fetch error:", error);
  }
}

// Pokreni odmah i ponavljaj svakih 5 sekundi
document.addEventListener("DOMContentLoaded", () => {
  updateCoordinates();
  setInterval(updateCoordinates, 2000);
});

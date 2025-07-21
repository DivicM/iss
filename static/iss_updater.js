// Globalne varijable za koordinate
let userLat = 0;
let userLon = 0;
let issLat = 0;
let issLon = 0;

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

    // Ažuriraj HTML (koristi zasebne varijable)
    const userCoordsEl = document.getElementById("user-coords");
    const issCoordsEl = document.getElementById("iss-coords");

    if (userCoordsEl) {
      userCoordsEl.textContent = `Lat: ${userLat}, Lon: ${userLon}`;
    }
    if (issCoordsEl) {
      issCoordsEl.textContent = `Lat: ${issLat}, Lon: ${issLon}`;
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

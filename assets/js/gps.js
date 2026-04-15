mapboxgl.accessToken = "SUA_MAPBOX_ACCESS_TOKEN_AQUI";

const GPSMap = {
  map: null,
  markerVan: null,
  markerCircle: null,
  rotaSimulada: [
    [-46.6333, -23.5505],
    [-46.6352, -23.5512],
    [-46.6370, -23.5520],
    [-46.6385, -23.5531],
    [-46.6400, -23.5538]
  ],
  indice: 0,
  intervalId: null,

  init: () => {
    if (!mapboxgl.accessToken || mapboxgl.accessToken === "SUA_MAPBOX_ACCESS_TOKEN_AQUI") {
      UIFeedback.showError("Configure seu Mapbox Access Token em assets/js/gps.js");
      return;
    }

    try {
      GPSMap.map = new mapboxgl.Map({
        container: "map",
        style: "mapbox://styles/mapbox/streets-v12",
        center: [-46.6333, -23.5505],
        zoom: 14
      });

      GPSMap.map.on("load", GPSMap.setupMarkers);
      GPSMap.map.on("error", (e) => {
        console.error("Erro ao carregar mapa:", e);
        UIFeedback.showError("Erro ao carregar o mapa. Verifique sua chave do Mapbox.");
      });
    } catch (error) {
      console.error("Erro ao inicializar mapa:", error);
      UIFeedback.showError("Erro ao inicializar o mapa.");
    }
  },

  setupMarkers: () => {
    GPSMap.map.addControl(new mapboxgl.NavigationControl(), "top-right");

    const popupCircle = document.createElement("div");
    popupCircle.style.width = "40px";
    popupCircle.style.height = "40px";
    popupCircle.style.borderRadius = "50%";
    popupCircle.style.border = "2px solid rgba(127, 63, 191, 0.3)";
    popupCircle.style.backgroundColor = "rgba(127, 63, 191, 0.15)";

    GPSMap.markerVan = new mapboxgl.Marker({ color: "#7f3fbf" })
      .setLngLat(GPSMap.rotaSimulada[0])
      .addTo(GPSMap.map);

    GPSMap.markerCircle = new mapboxgl.Marker({ element: popupCircle })
      .setLngLat(GPSMap.rotaSimulada[0])
      .addTo(GPSMap.map);

    GPSMap.startTracking();
    GPSMap.setupSearch();
  },

  startTracking: () => {
    GPSMap.intervalId = setInterval(() => {
      GPSMap.indice = (GPSMap.indice + 1) % GPSMap.rotaSimulada.length;
      const novaPosicao = GPSMap.rotaSimulada[GPSMap.indice];

      GPSMap.markerVan.setLngLat(novaPosicao);
      GPSMap.markerCircle.setLngLat(novaPosicao);

      GPSMap.map.easeTo({
        center: novaPosicao,
        duration: 1000
      });
    }, 2000);
  },

  setupSearch: () => {
    const campoPesquisa = document.getElementById("campo-pesquisa");
    if (!campoPesquisa) return;

    campoPesquisa.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        const query = Validators.sanitizeInput(campoPesquisa.value);
        if (query.length > 2) {
          console.log("Pesquisar por:", query);
        }
      }
    });
  },

  stop: () => {
    if (GPSMap.intervalId) {
      clearInterval(GPSMap.intervalId);
      GPSMap.intervalId = null;
    }
  }
};

document.addEventListener("DOMContentLoaded", GPSMap.init);
window.addEventListener("beforeunload", GPSMap.stop);

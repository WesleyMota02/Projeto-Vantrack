let socketRastreamento;
let mapInstance;
let marcadorVan;
let rotaAtual;

const RastreamentoRealtime = {
  inicializar: () => {
    const token = localStorage.getItem('auth_token');
    const usuarioID = localStorage.getItem('usuario_id');

    if (!token || !usuarioID) {
      console.error('Token ou usuário ID não encontrado');
      return;
    }

    socketRastreamento = io('http://localhost:5000/rastreamento', {
      query: {
        token: token,
        usuario_id: usuarioID
      },
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    });

    socketRastreamento.on('connect', RastreamentoRealtime.onConectado);
    socketRastreamento.on('disconnect', RastreamentoRealtime.onDesconectado);
    socketRastreamento.on('conectado', RastreamentoRealtime.onStatusConectado);
    socketRastreamento.on('localizacao_atualizada', RastreamentoRealtime.onLocalizacaoAtualizada);
    socketRastreamento.on('erro', RastreamentoRealtime.onErro);
  },

  inicializarMapa: () => {
    const container = document.getElementById('mapa-rastreamento');
    if (!container) return;

    mapInstance = L.map('mapa-rastreamento', {
      center: [-23.5505, -46.6333],
      zoom: 13,
      zoomControl: true,
      attributionControl: true
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19,
      minZoom: 5
    }).addTo(mapInstance);

    const vanIcon = L.divIcon({
      className: 'van-icon',
      html: '<i class="fas fa-van-shuttle" style="font-size: 24px; color: #0099ff;"></i>',
      iconSize: [30, 30],
      iconAnchor: [15, 15]
    });

    marcadorVan = L.marker([-23.5505, -46.6333], { icon: vanIcon })
      .addTo(mapInstance)
      .bindPopup('Van - Aguardando localização');
  },

  onConectado: () => {
    console.log('Conectado ao servidor de rastreamento');
    const statusEl = document.getElementById('status-conexao');
    if (statusEl) {
      statusEl.innerHTML = '<i class="fas fa-circle" style="color: #22c55e;"></i> Conectado';
    }

    RastreamentoRealtime.inicializarMapa();
    RastreamentoRealtime.inscreverRota();
  },

  onDesconectado: () => {
    console.log('Desconectado do servidor de rastreamento');
    const statusEl = document.getElementById('status-conexao');
    if (statusEl) {
      statusEl.innerHTML = '<i class="fas fa-circle" style="color: #ef4444;"></i> Desconectado';
    }
  },

  onStatusConectado: (data) => {
    console.log('Status:', data.status);
  },

  onLocalizacaoAtualizada: (data) => {
    if (!mapInstance || !marcadorVan) return;

    const { latitude, longitude, velocidade, timestamp } = data;

    marcadorVan.setLatLng([latitude, longitude]);
    mapInstance.panTo([latitude, longitude]);

    const popup = `<strong>Van</strong><br>
      Lat: ${latitude.toFixed(4)}<br>
      Lon: ${longitude.toFixed(4)}<br>
      Vel: ${velocidade || 0} km/h<br>
      Hora: ${new Date(timestamp).toLocaleTimeString()}`;
    marcadorVan.setPopupContent(popup);

    console.log('Localização atualizada:', latitude, longitude);
  },

  onErro: (data) => {
    console.error('Erro do servidor:', data.mensagem);
  },

  inscreverRota: () => {
    const usuarioJSON = localStorage.getItem('usuario_dados');
    if (!usuarioJSON) return;

    const usuario = JSON.parse(usuarioJSON);
    const rotaID = usuario.rota_id || 'default_rota';

    socketRastreamento.emit('inscrever_rota', { rota_id: rotaID });
    console.log('Inscrito na rota:', rotaID);
  },

  desinscreverRota: () => {
    const usuarioJSON = localStorage.getItem('usuario_dados');
    if (!usuarioJSON) return;

    const usuario = JSON.parse(usuarioJSON);
    const rotaID = usuario.rota_id || 'default_rota';

    socketRastreamento.emit('desinscrever_rota', { rota_id: rotaID });
    console.log('Desinscrito da rota:', rotaID);
  }
};

document.addEventListener('DOMContentLoaded', () => {
  RastreamentoRealtime.inicializar();
});

requireAuth();
if(!temPerfil('motorista')){mostrarNotificacao('Acesso apenas para motoristas','erro');setTimeout(()=>logout(),1500);}

let map=null,marker=null,watchId=null;
const mapContainer='mapa';

document.addEventListener('DOMContentLoaded',()=>{
    initMapa();
    document.getElementById('btn-registrar')?.addEventListener('click',registrarLocalizacao);
    document.getElementById('btn-atualizar')?.addEventListener('click',carregarHistorico);
    carregarHistorico();
});

function initMapa(){
    if(!document.getElementById(mapContainer))return;
    const defLat=-23.5505,defLng=-46.6333,defZoom=14;
    if(typeof mapboxgl!=='undefined'){
        mapboxgl.accessToken='YOUR_MAPBOX_TOKEN';
        map=new mapboxgl.Map({container:mapContainer,style:'mapbox://styles/mapbox/streets-v12',center:[defLng,defLat],zoom:defZoom});
        marker=new mapboxgl.Marker({color:'#ff0000'}).setLngLat([defLng,defLat]).addTo(map);
    }else{
        console.log('Mapbox não carregado, usando fallback');
        document.getElementById(mapContainer).innerHTML='<p>Mapa indisponível. Usando coordenadas numéricas.</p>';
    }
}

function registrarLocalizacao(){
    if(!navigator.geolocation){mostrarNotificacao('Geolocalização não disponível','erro');return;}
    const btn=document.getElementById('btn-registrar');btn.disabled=true;btn.textContent='Obtendo localização...';
    navigator.geolocation.getCurrentPosition(async pos=>{
        const lat=pos.coords.latitude,lng=pos.coords.longitude;
        if(!validarCoordenadas(lat,lng)){mostrarNotificacao('Coordenadas inválidas','erro');btn.disabled=false;btn.textContent='Registrar Localização';return;}
        try{
            const r=await fetchAPI('POST','/gps/registrar',{latitude:lat,longitude:lng,veiculo_id:document.getElementById('veiculo-id')?.value||1});
            if(r){mostrarNotificacao('Localização registrada!','sucesso');atualizarMapa(lat,lng);carregarHistorico();}
        }catch(e){mostrarNotificacao(e.message||'Erro ao registrar','erro');}finally{btn.disabled=false;btn.textContent='Registrar Localização';}
    },e=>{mostrarNotificacao('Erro ao obter localização: '+e.message,'erro');btn.disabled=false;btn.textContent='Registrar Localização';});
}

function atualizarMapa(lat,lng){
    if(map&&marker){
        const pt=[lng,lat];
        marker.setLngLat(pt);
        map.easeTo({center:pt,duration:500});
    }
}

async function carregarHistorico(){
    try{
        const vId=document.getElementById('veiculo-id')?.value||1;
        const r=await fetchAPI('GET',`/gps/${vId}/historico`);
        if(r&&r.localizacoes){
            const tb=document.getElementById('tabela-historico')||criarTabelaHistorico();
            const tbody=tb.querySelector('tbody');
            tbody.innerHTML='';
            r.localizacoes.slice(0,50).forEach(loc=>{
                const tr=document.createElement('tr');
                tr.innerHTML=`<td>${formatarData(loc.timestamp)}</td><td>${loc.latitude}</td><td>${loc.longitude}</td><td>${formatarHora(loc.timestamp)}</td>`;
                tbody.appendChild(tr);
            });
        }
    }catch(e){console.error('Erro histórico:',e);}
}

function criarTabelaHistorico(){
    const c=document.getElementById('container-historico')||document.body;
    const t=document.createElement('table');
    t.id='tabela-historico';
    t.innerHTML='<thead><tr><th>Data</th><th>Latitude</th><th>Longitude</th><th>Hora</th></tr></thead><tbody></tbody>';
    c.appendChild(t);
    return t;
}

document.addEventListener("DOMContentLoaded", GPSMap.init);
window.addEventListener("beforeunload", GPSMap.stop);

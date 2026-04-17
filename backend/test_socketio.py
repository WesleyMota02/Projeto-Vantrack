#!/usr/bin/env python3
"""
Script para testar Socket.IO - GPS Realtime e Chat
"""
import socketio
import time
import json
from threading import Thread
from uuid import uuid4

# Conectar ao servidor Socket.IO
sio = socketio.Client()

# Dados de teste
test_data = {
    "token": None,
    "usuario_id": None,
    "veiculo_id": str(uuid4()),
    "messages_received": []
}

print("="*70)
print("  TESTES SOCKET.IO - VANTRACK (GPS REALTIME + CHAT)")
print("="*70)

# ========== EVENTOS RASTREAMENTO ==========
@sio.on('conectado', namespace='/rastreamento')
def on_connect_rastreamento(data):
    print(f"\n[RASTREAMENTO] Conectado: {data}")

@sio.on('localizacao_atualizada', namespace='/rastreamento')
def on_localizacao_atualizada(data):
    print(f"\n[RASTREAMENTO] Localização atualizada:")
    print(f"  Latitude: {data.get('latitude')}")
    print(f"  Longitude: {data.get('longitude')}")
    print(f"  Velocidade: {data.get('velocidade')} km/h")

@sio.on('erro', namespace='/rastreamento')
def on_erro_rastreamento(data):
    print(f"\n[RASTREAMENTO] Erro: {data.get('mensagem')}")

@sio.on('disconnect', namespace='/rastreamento')
def on_disconnect_rastreamento():
    print(f"\n[RASTREAMENTO] Desconectado")

# ========== EVENTOS CHAT ==========
@sio.on('conectado_chat', namespace='/chat')
def on_connect_chat(data):
    print(f"\n[CHAT] Conectado: {data}")

@sio.on('mensagem_recebida', namespace='/chat')
def on_mensagem_recebida(data):
    print(f"\n[CHAT] Nova mensagem:")
    print(f"  De: {data.get('remetente_id')}")
    print(f"  Texto: {data.get('texto')}")
    test_data["messages_received"].append(data)

@sio.on('erro', namespace='/chat')
def on_erro_chat(data):
    print(f"\n[CHAT] Erro: {data.get('mensagem')}")

@sio.on('disconnect', namespace='/chat')
def on_disconnect_chat():
    print(f"\n[CHAT] Desconectado")

def test_socketio():
    try:
        # ========== TESTE 1: CONECTAR AO NAMESPACE RASTREAMENTO ==========
        print("\n" + "="*70)
        print("  1️⃣  CONECTANDO AO NAMESPACE /rastreamento")
        print("="*70)
        
        try:
            sio.connect(
                'http://localhost:5000',
                auth={'token': 'test_token', 'usuario_id': test_data["usuario_id"]},
                transports=['websocket'],
                namespaces=['/rastreamento']
            )
            print("✓ Conectado ao rastreamento")
        except Exception as e:
            print(f"✗ Erro ao conectar: {e}")
            return False
        
        time.sleep(1)
        
        # ========== TESTE 2: ENVIAR LOCALIZAÇÃO ==========
        print("\n" + "="*70)
        print("  2️⃣  ENVIANDO ATUALIZAÇÕES DE LOCALIZAÇÃO")
        print("="*70)
        
        for i in range(3):
            localizacao = {
                'veiculo_id': test_data["veiculo_id"],
                'latitude': -23.5505 + (i * 0.001),
                'longitude': -46.6333 + (i * 0.001),
                'velocidade': 50.5 + (i * 5),
                'direcao': 45 + (i * 10),
                'precisao': 10.5
            }
            
            print(f"\nEnviando localização {i+1}:")
            print(f"  Lat: {localizacao['latitude']}")
            print(f"  Lon: {localizacao['longitude']}")
            print(f"  Velocidade: {localizacao['velocidade']} km/h")
            
            sio.emit('atualizar_localizacao', localizacao, namespace='/rastreamento')
            time.sleep(1)
        
        # ========== TESTE 3: INSCREVER EM ROTA ==========
        print("\n" + "="*70)
        print("  3️⃣  INSCRIÇÃO EM ROTA")
        print("="*70)
        
        rota_id = str(uuid4())
        sio.emit('inscrever_rota', {'rota_id': rota_id}, namespace='/rastreamento')
        print(f"Inscrito na rota: {rota_id}")
        time.sleep(1)
        
        # ========== TESTE 4: CHAT MESSAGING ==========
        print("\n" + "="*70)
        print("  4️⃣  TESTE DE CHAT")
        print("="*70)
        
        # Desconectar de rastreamento e conectar ao chat
        sio.disconnect(namespace='/rastreamento')
        time.sleep(1)
        
        try:
            sio.connect(
                'http://localhost:5000',
                auth={'token': 'test_token', 'usuario_id': test_data["usuario_id"]},
                transports=['websocket'],
                namespaces=['/chat']
            )
            print("✓ Conectado ao chat")
        except Exception as e:
            print(f"Aviso ao conectar ao chat: {e}")
        
        time.sleep(1)
        
        # ========== TESTE 5: ENVIAR MENSAGEM ==========
        print("\n" + "="*70)
        print("  5️⃣  ENVIANDO MENSAGEM DE CHAT")
        print("="*70)
        
        mensagem = {
            'conversa_id': str(uuid4()),
            'texto': 'Olá! Esta é uma mensagem de teste do Socket.IO',
            'destinatario_id': str(uuid4())
        }
        
        print(f"Enviando: {mensagem['texto']}")
        sio.emit('enviar_mensagem', mensagem, namespace='/chat')
        time.sleep(2)
        
        # ========== TESTE 6: DESINSCREVER DE ROTA ==========
        print("\n" + "="*70)
        print("  6️⃣  DESINSCREVENDO DE ROTA")
        print("="*70)
        
        sio.emit('desinscrever_rota', {'rota_id': rota_id}, namespace='/rastreamento')
        print(f"Desiscrito da rota: {rota_id}")
        time.sleep(1)
        
        # ========== DESCONECTAR ==========
        print("\n" + "="*70)
        print("  ✅ TESTES CONCLUÍDOS")
        print("="*70)
        
        sio.disconnect()
        print("Desconectado")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("\n⚠️  Aviso: Socket.IO requer servidor rodando em http://localhost:5000")
    print("   Certifique-se de que o servidor está iniciado antes de rodar este teste.\n")
    
    input("Pressione ENTER para começar os testes...")
    
    test_socketio()

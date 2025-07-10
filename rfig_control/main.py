from libs.mfrc522 import MFRC522
import utime
import json
from umqtt.simple import MQTTClient
import network
from machine import Pin

# Configuração WiFi
WIFI_SSID = "Sua Rede WiFi"  # Substitua pelo SSID da sua rede WiFi
WIFI_PASSWORD = "Sua Senha WiFi"  # Substitua pela senha da sua rede WiFi

# Configuração MQTT
MQTT_SERVER = "Seu_IP_Assistant"  # IP do seu Home Assistant
MQTT_PORT = 1883
MQTT_USER = "Seu_Usuario_MQTT"  # Substitua pelo usuário MQTT
MQTT_PASSWORD = "Sua_Senha_MQTT"  # Substitua pela senha MQTT
MQTT_CLIENT_ID = "rfid_reader"

# Configuração do LED
led = Pin("LED", Pin.OUT)  # LED interno do Raspberry Pi Pico
led.off()  # LED desligado inicialmente

# Configuração do leitor RFID
reader = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)

def connect_wifi():
    """Conecta ao WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando ao WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            utime.sleep(1)
    print(f"WiFi conectado: {wlan.ifconfig()[0]}")

def connect_mqtt():
    """Conecta ao MQTT"""
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_SERVER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD)
        client.connect()
        print("MQTT conectado")
        
        # Liga o LED quando conectar ao MQTT
        print("Ligando LED...")
        led.on()
        print("LED ligado - Sistema conectado!")
        
        # Envia evento de sistema iniciado
        try:
            startup_payload = {
                "event_type": "system_startup",
                "device_id": "rfid_reader",
                "timestamp": utime.time(),
                "status": "online"
            }
            client.publish("homeassistant/event/rfid_reader/startup", json.dumps(startup_payload))
            client.publish("rfid_reader/status", "online")
            print("Evento de startup enviado")
        except:
            print("Erro ao enviar evento de startup")
        
        return client
    except Exception as e:
        print(f"Erro MQTT: {e}")
        print("Desligando LED por erro...")
        led.off()  # Garante que o LED fica desligado se houver erro
        return None

def send_to_home_assistant(client, card_id, text_data):
    """Envia dados para o Home Assistant"""
    if client:
        try:
            # Payload com os dados do cartão
            payload = {
                "card_id": card_id,
                "text": text_data,
                "timestamp": utime.time()
            }
            
            # Tópico para o sensor
            topic = "homeassistant/sensor/rfid_reader/state"
            client.publish(topic, json.dumps(payload))
            
            # Tópico específico para eventos
            event_topic = "homeassistant/event/rfid_reader/card_detected"
            event_payload = {
                "event_type": "card_detected",
                "card_id": card_id,
                "card_text": text_data,
                "timestamp": utime.time(),
                "device_id": "rfid_reader"
            }
            client.publish(event_topic, json.dumps(event_payload))
            
            # Tópico para o dispositivo MQTT
            device_topic = "rfid_reader/card"
            device_payload = {
                "id": card_id,
                "text": text_data,
                "time": utime.time()
            }
            client.publish(device_topic, json.dumps(device_payload))
            
            print(f"Enviado para HA: Card ID {card_id}, Text: '{text_data}'")
            
        except Exception as e:
            print(f"Erro ao enviar para HA: {e}")

def read_card_data(uid):
    """Lê dados do cartão"""
    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    sector = 8
    text_data = ""
    
    if reader.auth(reader.AUTHENT1A, sector, key, uid) == reader.OK:
        data = reader.read(sector)
        if data:
            # Converter para texto se possível
            try:
                if isinstance(data, tuple) and len(data) >= 2:
                    byte_data = data[1]
                else:
                    byte_data = data
                text = ''.join([chr(b) for b in byte_data if 32 <= b <= 126])
                if text:
                    print(f"Texto: '{text}'")
                    text_data = text
                else:
                    print("Nenhum texto encontrado")
                    text_data = ""
            except:
                print("Dados em formato binário")
                text_data = ""
        else:
            print("Erro ao ler dados")
    else:
        print("Erro de autenticação")
    
    return text_data

def wait_for_card(mqtt_client):
    """Aguarda um cartão e mostra informações"""
    print("Aproxime o cartão do leitor...")
    
    last_card = None
    
    while True:
        reader.init()
        stat, _ = reader.request(reader.REQIDL)
        
        if stat == reader.OK:
            stat, uid = reader.SelectTagSN()
            if stat == reader.OK:
                card_id = int.from_bytes(bytes(uid), "little")
                
                # Só mostra se for um cartão diferente
                if card_id != last_card:
                    last_card = card_id
                    print(f"\nCARD ID: {card_id}")
                    
                    # Sempre lê e mostra os dados da tag
                    text_data = read_card_data(uid)
                    
                    # Envia para o Home Assistant
                    send_to_home_assistant(mqtt_client, card_id, text_data)
                    
                    reader.stop_crypto1()
        else:
            # Cartão removido
            if last_card is not None:
                last_card = None
                print("Cartão removido - aproxime outro cartão...")
        
        utime.sleep_ms(100)

# Loop principal
print("=== Sistema RFID com Home Assistant ===")
print("Testando LED...")

# Teste inicial do LED
led.on()
utime.sleep(0.5)
led.off()
utime.sleep(0.5)
led.on()
utime.sleep(0.5)
led.off()
print("Teste do LED concluído")

print("Conectando ao WiFi e MQTT...")

try:
    # Conecta ao WiFi
    connect_wifi()
    
    # Conecta ao MQTT
    mqtt_client = connect_mqtt()
    
    if mqtt_client:
        print("Sistema pronto! Pressione Ctrl+C para sair")
        while True:
            wait_for_card(mqtt_client)
    else:
        print("Erro: Não foi possível conectar ao MQTT")
        
except KeyboardInterrupt:
    print("\nSaindo...")
    led.off()  # Desliga o LED ao sair
except Exception as e:
    print(f"Erro: {e}")
    led.off()  # Desliga o LED em caso de erro
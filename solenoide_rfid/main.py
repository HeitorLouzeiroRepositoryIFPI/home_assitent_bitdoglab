# rele_mqtt.py - Controle de Relé via MQTT na BitDogLab
# NOTA: Os relés usam lógica invertida (GPIO baixo = ligado, GPIO alto = desligado)

from machine import Pin
from umqtt.simple import MQTTClient
import network
import time
import json # Embora não estritamente necessário para comandos ON/OFF simples, pode ser útil para estados futuros

# --- Configurações do Usuário ---
WIFI_SSID = "SuaRedeWiFi"  # Ex: "rede"
WIFI_PASSWORD = "PasswordDaRede"  # Deixe em branco se não houver senha

# Configurações do Broker MQTT
MQTT_BROKER = "Ip_Home_Assitant"  # Ex: "192.168.1.100" ou "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_USER = "Seu_usuario"  # Deixe em branco se não houver autenticação
MQTT_PASSWORD = "Seu_Passoword" # Deixe em branco se não houver autenticação
MQTT_CLIENT_ID = "raspberry_pi_solenoid_rfid"  # Identificador único do cliente MQTT

# Pinos (conforme informado pelo usuário)
PIN_RELE_SETOR1 = 16
PIN_RELE_SETOR2 = 17

# Tópicos MQTT - Setor 1
MQTT_TOPIC_RELE_STATE_SETOR1 = "pico/solenoid/setor1/state"    # Publica o estado atual (ON/OFF)
MQTT_TOPIC_RELE_COMMAND_SETOR1 = "pico/solenoid/setor1/set"  # Recebe comandos (ON/OFF)
MQTT_TOPIC_RELE_AVAILABILITY_SETOR1 = "pico/solenoid/setor1/status"

# Tópicos MQTT - Setor 2
MQTT_TOPIC_RELE_STATE_SETOR2 = "pico/solenoid/setor2/state"    # Publica o estado atual (ON/OFF)
MQTT_TOPIC_RELE_COMMAND_SETOR2 = "pico/solenoid/setor2/set"  # Recebe comandos (ON/OFF)
MQTT_TOPIC_RELE_AVAILABILITY_SETOR2 = "pico/solenoid/setor2/status"
# --- Fim das Configurações do Usuário ---

# Configuração dos Pinos
rele_setor1 = Pin(PIN_RELE_SETOR1, Pin.OUT)
rele_setor2 = Pin(PIN_RELE_SETOR2, Pin.OUT)

# Estado inicial e variáveis de controle
rele_estado_atual_setor1 = 0  # 0 para OFF, 1 para ON
rele_estado_atual_setor2 = 0  # 0 para OFF, 1 para ON
# Lógica invertida: 1 no GPIO = desligado, 0 no GPIO = ligado
rele_setor1.value(1 - rele_estado_atual_setor1)
rele_setor2.value(1 - rele_estado_atual_setor2)

mqtt_client = None

def set_rele_state(setor, novo_estado, origem="script"):
    global rele_estado_atual_setor1, rele_estado_atual_setor2, mqtt_client
    
    if setor == 1:
        rele_estado_atual_setor1 = novo_estado
        # Lógica invertida: 1 no GPIO = desligado, 0 no GPIO = ligado
        rele_setor1.value(1 - rele_estado_atual_setor1)
        estado_str = "ON" if rele_estado_atual_setor1 == 1 else "OFF"
        print(f"Relé Setor 1 {estado_str} (Origem: {origem})")
        if mqtt_client:
            try:
                mqtt_client.publish(MQTT_TOPIC_RELE_STATE_SETOR1, estado_str.encode(), retain=True)
            except Exception as e:
                print(f"Erro ao publicar estado do relé setor 1: {e}")
    elif setor == 2:
        rele_estado_atual_setor2 = novo_estado
        # Lógica invertida: 1 no GPIO = desligado, 0 no GPIO = ligado
        rele_setor2.value(1 - rele_estado_atual_setor2)
        estado_str = "ON" if rele_estado_atual_setor2 == 1 else "OFF"
        print(f"Relé Setor 2 {estado_str} (Origem: {origem})")
        if mqtt_client:
            try:
                mqtt_client.publish(MQTT_TOPIC_RELE_STATE_SETOR2, estado_str.encode(), retain=True)
            except Exception as e:
                print(f"Erro ao publicar estado do relé setor 2: {e}")

def mqtt_callback(topic, msg, *args):
    global rele_estado_atual_setor1, rele_estado_atual_setor2
    print(f"Mensagem recebida - Tópico: {topic.decode()}, Mensagem: {msg.decode()}")
    comando = msg.decode().upper()
    
    if topic.decode() == MQTT_TOPIC_RELE_COMMAND_SETOR1:
        if comando == "ON" and rele_estado_atual_setor1 == 0:
            set_rele_state(1, 1, origem="mqtt")
        elif comando == "OFF" and rele_estado_atual_setor1 == 1:
            set_rele_state(1, 0, origem="mqtt")
        elif comando == "TOGGLE":
             novo_estado = 1 - rele_estado_atual_setor1
             set_rele_state(1, novo_estado, origem="mqtt_toggle")
        else:
            print(f"Comando MQTT inválido ou estado já é {comando} para Setor 1")
    elif topic.decode() == MQTT_TOPIC_RELE_COMMAND_SETOR2:
        if comando == "ON" and rele_estado_atual_setor2 == 0:
            set_rele_state(2, 1, origem="mqtt")
        elif comando == "OFF" and rele_estado_atual_setor2 == 1:
            set_rele_state(2, 0, origem="mqtt")
        elif comando == "TOGGLE":
             novo_estado = 1 - rele_estado_atual_setor2
             set_rele_state(2, novo_estado, origem="mqtt_toggle")
        else:
            print(f"Comando MQTT inválido ou estado já é {comando} para Setor 2")
    else:
        print(f"Mensagem recebida em tópico inesperado: {topic.decode()}")

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Conectando à rede {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout_wifi = 0
        while not wlan.isconnected() and timeout_wifi < 20:
            print(".", end="")
            time.sleep(1)
            timeout_wifi += 1
        if wlan.isconnected():
            print(f"\nConectado ao Wi-Fi! IP: {wlan.ifconfig()[0]}")
            return True
        else:
            print("\nFalha ao conectar ao Wi-Fi.")
            return False
    print(f"Já conectado ao Wi-Fi. IP: {wlan.ifconfig()[0]}")
    return True

def connect_and_subscribe_mqtt():
    global mqtt_client
    mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
    mqtt_client.set_callback(mqtt_callback)
    try:
        mqtt_client.connect()
        print(f"Conectado ao broker MQTT: {MQTT_BROKER}")
        
        # Subscrever aos tópicos de comando dos dois setores
        mqtt_client.subscribe(MQTT_TOPIC_RELE_COMMAND_SETOR1)
        mqtt_client.subscribe(MQTT_TOPIC_RELE_COMMAND_SETOR2)
        print(f"Inscrito no tópico de comando Setor 1: {MQTT_TOPIC_RELE_COMMAND_SETOR1}")
        print(f"Inscrito no tópico de comando Setor 2: {MQTT_TOPIC_RELE_COMMAND_SETOR2}")
        
        # Publica disponibilidade e estado inicial dos dois setores
        mqtt_client.publish(MQTT_TOPIC_RELE_AVAILABILITY_SETOR1, b"online", retain=True)
        mqtt_client.publish(MQTT_TOPIC_RELE_AVAILABILITY_SETOR2, b"online", retain=True)
        
        initial_state_str_setor1 = "ON" if rele_estado_atual_setor1 == 1 else "OFF"
        initial_state_str_setor2 = "ON" if rele_estado_atual_setor2 == 1 else "OFF"
        
        mqtt_client.publish(MQTT_TOPIC_RELE_STATE_SETOR1, initial_state_str_setor1.encode(), retain=True)
        mqtt_client.publish(MQTT_TOPIC_RELE_STATE_SETOR2, initial_state_str_setor2.encode(), retain=True)
        return True
    except OSError as e:
        print(f"Falha ao conectar ao broker MQTT: {e}")
        return False
    except Exception as e:
        print(f"Outro erro MQTT: {e}")
        return False

print("Iniciando controle de relé via MQTT...")
print(f"Relé Setor 1 (GPIO{PIN_RELE_SETOR1})")
print(f"Relé Setor 2 (GPIO{PIN_RELE_SETOR2})")

if not connect_wifi():
    print("Não foi possível conectar ao Wi-Fi. Verifique as configurações e reinicie.")
    # Poderia tentar um soft reset ou entrar em modo de espera
else:
    if not connect_and_subscribe_mqtt():
        print("Não foi possível conectar ao MQTT. Verifique as configurações e reinicie.")
        # Poderia tentar um soft reset ou entrar em modo de espera
    else:
        print("Sistema pronto. Aguardando comandos MQTT.")

        while True:
            try:
                # Verifica mensagens MQTT
                if mqtt_client:
                    mqtt_client.check_msg()
                
                time.sleep_ms(100) # Pequena pausa no loop

            except OSError as e:
                print(f"Erro de OSError no loop principal: {e}")
                print("Tentando reconectar ao MQTT...")
                time.sleep(5)
                if mqtt_client: 
                    try:
                        mqtt_client.disconnect() # Tenta desconectar antes de reconectar
                    except: pass # Ignora erros na desconexão
                if not connect_and_subscribe_mqtt():
                    print("Falha ao reconectar ao MQTT. Reiniciando em 30s...")
                    time.sleep(30)
                    # machine.reset() # Descomente para reiniciar em caso de falha persistente
                else:
                    print("Reconectado ao MQTT com sucesso.")
            except Exception as e:
                print(f"Erro inesperado no loop principal: {e}")
                time.sleep(10)
                # machine.reset() # Descomente para reiniciar em caso de erro grave


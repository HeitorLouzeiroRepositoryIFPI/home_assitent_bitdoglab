from machine import Pin, SoftI2C
from umqtt.simple import MQTTClient
import network
import time
import json
try:
    from ssd1306 import SSD1306_I2C
    DISPLAY_AVAILABLE = True
except ImportError:
    print("Display SSD1306 não disponível")
    DISPLAY_AVAILABLE = False

# --- Configurações do Usuário ---
WIFI_SSID = "rede"
WIFI_PASSWORD = "internet"

# Configurações do Broker MQTT
MQTT_BROKER = "192.168.0.100"  # Ex: "192.168.1.100" ou "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_USER = ""  # Deixe em branco se não houver autenticação
MQTT_PASSWORD = "" # Deixe em branco se não houver autenticação
MQTT_CLIENT_ID = "bitdoglab_dual_rele_controller"

# Pinos
PIN_BUTTON_A = 6   # Controla Relé A (GPIO 19)
PIN_BUTTON_B = 5   # Controla Relé B (GPIO 20)
PIN_RELE_A = 19    # Relé A
PIN_RELE_B = 20    # Relé B

# Configurações do Display OLED I2C
I2C_SDA = 14       # Pino SDA do display (conforme exemplo)
I2C_SCL = 15       # Pino SCL do display (conforme exemplo)
OLED_WIDTH = 128   # Largura do display
OLED_HEIGHT = 64   # Altura do display

# Tópicos MQTT - Relé A (GPIO 19)
MQTT_TOPIC_RELE_A_STATE = "bitdoglab/rele/gpio19/state"
MQTT_TOPIC_RELE_A_COMMAND = "bitdoglab/rele/gpio19/set"
MQTT_TOPIC_RELE_A_AVAILABILITY = "bitdoglab/rele/gpio19/status"

# Tópicos MQTT - Relé B (GPIO 20)
MQTT_TOPIC_RELE_B_STATE = "bitdoglab/rele/gpio20/state"
MQTT_TOPIC_RELE_B_COMMAND = "bitdoglab/rele/gpio20/set"
MQTT_TOPIC_RELE_B_AVAILABILITY = "bitdoglab/rele/gpio20/status"

# --- Fim das Configurações do Usuário ---

# Configuração dos Pinos
button_a = Pin(PIN_BUTTON_A, Pin.IN, Pin.PULL_UP)
button_b = Pin(PIN_BUTTON_B, Pin.IN, Pin.PULL_UP)
rele_a = Pin(PIN_RELE_A, Pin.OUT)
rele_b = Pin(PIN_RELE_B, Pin.OUT)

# Configuração do Display OLED
display = None
if DISPLAY_AVAILABLE:
    try:
        i2c = SoftI2C(scl=Pin(I2C_SCL), sda=Pin(I2C_SDA))
        display = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)
        print("Display OLED inicializado com sucesso")
    except Exception as e:
        print(f"Erro ao inicializar display: {e}")
        display = None

# Estados iniciais e variáveis de controle
rele_a_estado_atual = 0  # 0 para OFF, 1 para ON
rele_b_estado_atual = 0  # 0 para OFF, 1 para ON
rele_a.value(rele_a_estado_atual)
rele_b.value(rele_b_estado_atual)

last_button_a_press_time = 0
last_button_b_press_time = 0
DEBOUNCE_MS = 250

mqtt_client = None
wifi_status = "Desconectado"
mqtt_status = "Desconectado"

def set_rele_a_state(novo_estado, origem="script"):
    global rele_a_estado_atual, mqtt_client
    rele_a_estado_atual = novo_estado
    rele_a.value(1 - rele_a_estado_atual)  # Inverte a lógica: 0->1, 1->0
    estado_str = "ON" if rele_a_estado_atual == 1 else "OFF"
    print(f"Relé A (GPIO19) {estado_str} (Origem: {origem})")
    if mqtt_client:
        try:
            mqtt_client.publish(MQTT_TOPIC_RELE_A_STATE, estado_str.encode(), retain=True)
        except Exception as e:
            print(f"Erro ao publicar estado do relé A: {e}")

def set_rele_b_state(novo_estado, origem="script"):
    global rele_b_estado_atual, mqtt_client
    rele_b_estado_atual = novo_estado
    rele_b.value(1 - rele_b_estado_atual)  # Inverte a lógica: 0->1, 1->0
    estado_str = "ON" if rele_b_estado_atual == 1 else "OFF"
    print(f"Relé B (GPIO20) {estado_str} (Origem: {origem})")
    if mqtt_client:
        try:
            mqtt_client.publish(MQTT_TOPIC_RELE_B_STATE, estado_str.encode(), retain=True)
        except Exception as e:
            print(f"Erro ao publicar estado do relé B: {e}")

def toggle_rele_a():
    novo_estado = 1 - rele_a_estado_atual
    set_rele_a_state(novo_estado, origem="botao_a")

def toggle_rele_b():
    novo_estado = 1 - rele_b_estado_atual
    set_rele_b_state(novo_estado, origem="botao_b")

def mqtt_callback(topic, msg, *args):
    global rele_a_estado_atual, rele_b_estado_atual
    print(f"Mensagem recebida - Tópico: {topic.decode()}, Mensagem: {msg.decode()}")
    comando = msg.decode().upper()
    topic_str = topic.decode()
    
    # Controle do Relé A (GPIO 19)
    if topic_str == MQTT_TOPIC_RELE_A_COMMAND:
        if comando == "ON" and rele_a_estado_atual == 0:
            set_rele_a_state(1, origem="mqtt")
        elif comando == "OFF" and rele_a_estado_atual == 1:
            set_rele_a_state(0, origem="mqtt")
        elif comando == "TOGGLE":
            novo_estado = 1 - rele_a_estado_atual
            set_rele_a_state(novo_estado, origem="mqtt_toggle")
        else:
            print(f"Comando MQTT inválido ou Relé A já está {comando}")
    
    # Controle do Relé B (GPIO 20)
    elif topic_str == MQTT_TOPIC_RELE_B_COMMAND:
        if comando == "ON" and rele_b_estado_atual == 0:
            set_rele_b_state(1, origem="mqtt")
        elif comando == "OFF" and rele_b_estado_atual == 1:
            set_rele_b_state(0, origem="mqtt")
        elif comando == "TOGGLE":
            novo_estado = 1 - rele_b_estado_atual
            set_rele_b_state(novo_estado, origem="mqtt_toggle")
        else:
            print(f"Comando MQTT inválido ou Relé B já está {comando}")
    else:
        print(f"Mensagem recebida em tópico inesperado: {topic_str}")

def connect_wifi():
    global wifi_status
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wifi_status = "Conectando..."
        print(f"Conectando à rede {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout_wifi = 0
        while not wlan.isconnected() and timeout_wifi < 20:
            print(".", end="")
            time.sleep(1)
            timeout_wifi += 1
        if wlan.isconnected():
            wifi_status = "Conectado"
            print(f"\nConectado ao Wi-Fi! IP: {wlan.ifconfig()[0]}")
            return True
        else:
            wifi_status = "Erro"
            print("\nFalha ao conectar ao Wi-Fi.")
            return False
    wifi_status = "Conectado"
    print(f"Já conectado ao Wi-Fi. IP: {wlan.ifconfig()[0]}")
    return True

def connect_and_subscribe_mqtt():
    global mqtt_client, mqtt_status
    mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
    mqtt_client.set_callback(mqtt_callback)
    try:
        mqtt_status = "Conectando..."
        mqtt_client.connect()
        mqtt_status = "Conectado"
        print(f"Conectado ao broker MQTT: {MQTT_BROKER}")
        
        # Inscreve nos tópicos de comando dos dois relés
        mqtt_client.subscribe(MQTT_TOPIC_RELE_A_COMMAND)
        mqtt_client.subscribe(MQTT_TOPIC_RELE_B_COMMAND)
        print(f"Inscrito nos tópicos: {MQTT_TOPIC_RELE_A_COMMAND} e {MQTT_TOPIC_RELE_B_COMMAND}")
        
        # Publica disponibilidade e estados iniciais
        mqtt_client.publish(MQTT_TOPIC_RELE_A_AVAILABILITY, b"online", retain=True)
        mqtt_client.publish(MQTT_TOPIC_RELE_B_AVAILABILITY, b"online", retain=True)
        
        initial_state_a = "OFF" if rele_a_estado_atual == 0 else "ON"
        initial_state_b = "OFF" if rele_b_estado_atual == 0 else "ON"
        mqtt_client.publish(MQTT_TOPIC_RELE_A_STATE, initial_state_a.encode(), retain=True)
        mqtt_client.publish(MQTT_TOPIC_RELE_B_STATE, initial_state_b.encode(), retain=True)
        
        return True
    except OSError as e:
        mqtt_status = "Erro"
        print(f"Falha ao conectar ao broker MQTT: {e}")
        return False
    except Exception as e:
        mqtt_status = "Erro"
        print(f"Outro erro MQTT: {e}")
        return False

print("Iniciando controle de 2 relés com Botões A, B e MQTT...")
print(f"Botão A (GPIO{PIN_BUTTON_A}) -> Relé A (GPIO{PIN_RELE_A})")
print(f"Botão B (GPIO{PIN_BUTTON_B}) -> Relé B (GPIO{PIN_RELE_B})")

if not connect_wifi():
    print("Não foi possível conectar ao Wi-Fi. Verifique as configurações e reinicie.")
else:
    if not connect_and_subscribe_mqtt():
        print("Não foi possível conectar ao MQTT. Verifique as configurações e reinicie.")
    else:
        print("Sistema pronto. Pressione os Botões A/B ou envie comandos MQTT.")

        while True:
            try:
                # Verifica botão A (controla Relé A - GPIO 19)
                if button_a.value() == 0:
                    current_time = time.ticks_ms()
                    if time.ticks_diff(current_time, last_button_a_press_time) > DEBOUNCE_MS:
                        last_button_a_press_time = current_time
                        toggle_rele_a()
                        time.sleep_ms(DEBOUNCE_MS)
                
                # Verifica botão B (controla Relé B - GPIO 20)
                if button_b.value() == 0:
                    current_time = time.ticks_ms()
                    if time.ticks_diff(current_time, last_button_b_press_time) > DEBOUNCE_MS:
                        last_button_b_press_time = current_time
                        toggle_rele_b()
                        time.sleep_ms(DEBOUNCE_MS)
                
                # Verifica mensagens MQTT
                if mqtt_client:
                    mqtt_client.check_msg()
                
                time.sleep_ms(20)

            except OSError as e:
                print(f"Erro de OSError no loop principal: {e}")
                print("Tentando reconectar ao MQTT...")
                time.sleep(5)
                if mqtt_client: 
                    try:
                        mqtt_client.disconnect()
                    except: pass
                if not connect_and_subscribe_mqtt():
                    print("Falha ao reconectar ao MQTT. Reiniciando em 30s...")
                    time.sleep(30)
                else:
                    print("Reconectado ao MQTT com sucesso.")
            except Exception as e:
                print(f"Erro inesperado no loop principal: {e}")
                time.sleep(10)
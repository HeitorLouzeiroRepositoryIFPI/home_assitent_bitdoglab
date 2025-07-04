# Arquivo de configuração para o controlador de relés

# --- Configurações de Rede ---
WIFI_SSID = "You-name-wifi"
WIFI_PASSWORD = "you-password"

# --- Configurações do Broker MQTT ---
MQTT_BROKER = "you-ip"  # Ex: "192.168.1.100" ou "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_USER = "you-user-mqtt"  # Deixe em branco se não houver autenticação
MQTT_PASSWORD = "you-password-mqtt"  # Deixe em branco se não houver autenticação
MQTT_CLIENT_ID = "bitdoglab_dual_rele_controller"

# --- Configurações de Pinos ---
PIN_BUTTON_A = 6   # Controla Relé A (GPIO 19)
PIN_BUTTON_B = 5   # Controla Relé B (GPIO 20)
PIN_RELE_A = 19    # Relé A
PIN_RELE_B = 20    # Relé B

# --- Configurações do Display OLED I2C ---
I2C_SDA = 14       # Pino SDA do display
I2C_SCL = 15       # Pino SCL do display
OLED_WIDTH = 128   # Largura do display
OLED_HEIGHT = 64   # Altura do display

# --- Tópicos MQTT - Relé A (GPIO 19) ---
MQTT_TOPIC_RELE_A_STATE = "bitdoglab/rele/gpio19/state"
MQTT_TOPIC_RELE_A_COMMAND = "bitdoglab/rele/gpio19/set"
MQTT_TOPIC_RELE_A_AVAILABILITY = "bitdoglab/rele/gpio19/status"

# --- Tópicos MQTT - Relé B (GPIO 20) ---
MQTT_TOPIC_RELE_B_STATE = "bitdoglab/rele/gpio20/state"
MQTT_TOPIC_RELE_B_COMMAND = "bitdoglab/rele/gpio20/set"
MQTT_TOPIC_RELE_B_AVAILABILITY = "bitdoglab/rele/gpio20/status"

# --- Configurações de Debounce ---
DEBOUNCE_MS = 250

# --- Configurações de Timeouts ---
WIFI_TIMEOUT = 20
MQTT_RECONNECT_DELAY = 5
MQTT_RESTART_DELAY = 30
MAIN_LOOP_DELAY = 20
ERROR_DELAY = 10

"""
Controlador de Relé Individual

Esta classe gerencia um relé individual com botão físico e integração MQTT.
"""

from machine import Pin
import time
from config.config import DEBOUNCE_MS


class RelayController:
    """Classe para controlar um relé individual"""
    
    def __init__(self, pin_number, pin_button, mqtt_topic_state, mqtt_topic_command, mqtt_topic_availability, relay_name):
        self.pin_number = pin_number
        self.relay_name = relay_name
        self.relay_pin = Pin(pin_number, Pin.OUT)
        self.button_pin = Pin(pin_button, Pin.IN, Pin.PULL_UP)
        self.estado_atual = 0  # 0 para OFF, 1 para ON
        self.last_button_press_time = 0
        
        # Tópicos MQTT
        self.mqtt_topic_state = mqtt_topic_state
        self.mqtt_topic_command = mqtt_topic_command
        self.mqtt_topic_availability = mqtt_topic_availability
        
        # Inicializa o relé no estado OFF
        self.relay_pin.value(1)  # Lógica invertida: 1 = OFF, 0 = ON
        
    def set_state(self, novo_estado, origem="script", mqtt_client=None):
        """Define o estado do relé"""
        self.estado_atual = novo_estado
        self.relay_pin.value(1 - self.estado_atual)  # Inverte a lógica: 0->1, 1->0
        estado_str = "ON" if self.estado_atual == 1 else "OFF"
        print(f"Relé {self.relay_name} (GPIO{self.pin_number}) {estado_str} (Origem: {origem})")
        
        if mqtt_client:
            try:
                mqtt_client.publish(self.mqtt_topic_state, estado_str.encode(), retain=True)
            except Exception as e:
                print(f"Erro ao publicar estado do relé {self.relay_name}: {e}")
    
    def toggle(self, origem="button", mqtt_client=None):
        """Alterna o estado do relé"""
        novo_estado = 1 - self.estado_atual
        self.set_state(novo_estado, origem, mqtt_client)
    
    def check_button(self, mqtt_client=None):
        """Verifica se o botão foi pressionado"""
        if self.button_pin.value() == 0:
            current_time = time.ticks_ms()
            if time.ticks_diff(current_time, self.last_button_press_time) > DEBOUNCE_MS:
                self.last_button_press_time = current_time
                self.toggle(f"botao_{self.relay_name.lower()}", mqtt_client)
                time.sleep_ms(DEBOUNCE_MS)
                return True
        return False
    
    def handle_mqtt_command(self, comando, mqtt_client=None):
        """Processa comandos MQTT para este relé"""
        comando = comando.upper()
        
        if comando == "ON" and self.estado_atual == 0:
            self.set_state(1, "mqtt", mqtt_client)
        elif comando == "OFF" and self.estado_atual == 1:
            self.set_state(0, "mqtt", mqtt_client)
        elif comando == "TOGGLE":
            self.toggle("mqtt_toggle", mqtt_client)
        else:
            print(f"Comando MQTT inválido ou Relé {self.relay_name} já está {comando}")

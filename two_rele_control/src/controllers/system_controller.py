"""
Controlador Principal do Sistema

Esta classe coordena todos os componentes do sistema de controle de relés.
"""

import time
from .relay_controller import RelayController
from .display_controller import DisplayController
from ..managers.wifi_manager import WiFiManager
from ..managers.mqtt_manager import MQTTManager
from config import (
    PIN_BUTTON_A, PIN_BUTTON_B, PIN_RELE_A, PIN_RELE_B,
    MQTT_TOPIC_RELE_A_STATE, MQTT_TOPIC_RELE_A_COMMAND, MQTT_TOPIC_RELE_A_AVAILABILITY,
    MQTT_TOPIC_RELE_B_STATE, MQTT_TOPIC_RELE_B_COMMAND, MQTT_TOPIC_RELE_B_AVAILABILITY,
    MQTT_RECONNECT_DELAY, MQTT_RESTART_DELAY, MAIN_LOOP_DELAY, ERROR_DELAY
)


class SystemController:
    """Classe principal que coordena todo o sistema"""
    
    def __init__(self):
        print("Inicializando Sistema BitDogLab...")
        
        # Inicializa os controladores de relé
        self.relay_a = RelayController(
            PIN_RELE_A, PIN_BUTTON_A,
            MQTT_TOPIC_RELE_A_STATE, MQTT_TOPIC_RELE_A_COMMAND, MQTT_TOPIC_RELE_A_AVAILABILITY,
            "A"
        )
        
        self.relay_b = RelayController(
            PIN_RELE_B, PIN_BUTTON_B,
            MQTT_TOPIC_RELE_B_STATE, MQTT_TOPIC_RELE_B_COMMAND, MQTT_TOPIC_RELE_B_AVAILABILITY,
            "B"
        )
        
        # Inicializa os gerenciadores
        self.wifi_manager = WiFiManager()
        self.mqtt_manager = MQTTManager(self.relay_a, self.relay_b)
        self.display_controller = DisplayController()
        
        print("Componentes inicializados.")
    
    def initialize(self):
        """Inicializa o sistema"""
        print("Iniciando controle de 2 relés com Botões A, B e MQTT...")
        print(f"Botão A (GPIO{PIN_BUTTON_A}) -> Relé A (GPIO{PIN_RELE_A})")
        print(f"Botão B (GPIO{PIN_BUTTON_B}) -> Relé B (GPIO{PIN_RELE_B})")
        
        # Mostrar mensagem no display
        if self.display_controller.is_available():
            self.display_controller.show_message("Iniciando...", 0)
            self.display_controller.show_message("BitDogLab", 1)
        
        # Conectar WiFi
        if not self.wifi_manager.connect():
            print("Não foi possível conectar ao Wi-Fi. Verifique as configurações e reinicie.")
            if self.display_controller.is_available():
                self.display_controller.show_message("WiFi: Erro", 2)
            return False
        
        # Conectar MQTT
        if not self.mqtt_manager.connect():
            print("Não foi possível conectar ao MQTT. Verifique as configurações e reinicie.")
            if self.display_controller.is_available():
                self.display_controller.show_message("MQTT: Erro", 3)
            return False
        
        print("Sistema pronto. Pressione os Botões A/B ou envie comandos MQTT.")
        if self.display_controller.is_available():
            self.display_controller.show_message("Sistema Pronto!", 4)
        
        return True
    
    def update_display(self):
        """Atualiza o display com informações do sistema"""
        if self.display_controller.is_available():
            relay_a_state = "ON" if self.relay_a.estado_atual == 1 else "OFF"
            relay_b_state = "ON" if self.relay_b.estado_atual == 1 else "OFF"
            self.display_controller.update_display(
                self.wifi_manager.get_status(),
                self.mqtt_manager.get_status(),
                relay_a_state,
                relay_b_state
            )
    
    def handle_mqtt_reconnection(self):
        """Trata a reconexão MQTT"""
        print("Tentando reconectar ao MQTT...")
        time.sleep(MQTT_RECONNECT_DELAY)
        
        self.mqtt_manager.disconnect()
        if not self.mqtt_manager.connect():
            print(f"Falha ao reconectar ao MQTT. Reiniciando em {MQTT_RESTART_DELAY}s...")
            time.sleep(MQTT_RESTART_DELAY)
            return False
        else:
            print("Reconectado ao MQTT com sucesso.")
            return True
    
    def run(self):
        """Loop principal do sistema"""
        if not self.initialize():
            return
        
        print("Entrando no loop principal...")
        loop_counter = 0
        
        while True:
            try:
                # Verifica botões
                self.relay_a.check_button(self.mqtt_manager.client)
                self.relay_b.check_button(self.mqtt_manager.client)
                
                # Verifica mensagens MQTT
                self.mqtt_manager.check_messages()
                
                # Atualiza display a cada 50 loops (aproximadamente 1 segundo)
                if loop_counter % 50 == 0:
                    self.update_display()
                
                loop_counter += 1
                time.sleep_ms(MAIN_LOOP_DELAY)

            except OSError as e:
                print(f"Erro de OSError no loop principal: {e}")
                if not self.handle_mqtt_reconnection():
                    print("Falha crítica na reconexão MQTT.")
                    
            except Exception as e:
                print(f"Erro inesperado no loop principal: {e}")
                time.sleep(ERROR_DELAY)
    
    def shutdown(self):
        """Desliga o sistema de forma segura"""
        print("Desligando sistema...")
        
        # Desconectar MQTT
        self.mqtt_manager.disconnect()
        
        # Desconectar WiFi
        self.wifi_manager.disconnect()
        
        # Limpar display
        if self.display_controller.is_available():
            self.display_controller.clear()
        
        print("Sistema desligado.")
    
    def get_system_status(self):
        """Retorna o status completo do sistema"""
        return {
            'wifi': {
                'status': self.wifi_manager.get_status(),
                'connected': self.wifi_manager.is_connected(),
                'ip': self.wifi_manager.get_ip()
            },
            'mqtt': {
                'status': self.mqtt_manager.get_status(),
                'connected': self.mqtt_manager.is_connected
            },
            'relays': {
                'relay_a': {
                    'name': self.relay_a.relay_name,
                    'pin': self.relay_a.pin_number,
                    'state': self.relay_a.estado_atual
                },
                'relay_b': {
                    'name': self.relay_b.relay_name,
                    'pin': self.relay_b.pin_number,
                    'state': self.relay_b.estado_atual
                }
            },
            'display': {
                'available': self.display_controller.is_available()
            }
        }

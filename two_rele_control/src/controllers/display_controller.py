"""
Controlador de Display OLED

Esta classe gerencia o display OLED SSD1306 via I2C.
"""

from machine import Pin, SoftI2C
from config import I2C_SDA, I2C_SCL, OLED_WIDTH, OLED_HEIGHT

try:
    from ..drivers.ssd1306 import SSD1306_I2C
    DISPLAY_AVAILABLE = True
except ImportError:
    print("Display SSD1306 não disponível")
    DISPLAY_AVAILABLE = False


class DisplayController:
    """Classe para controlar o display OLED"""
    
    def __init__(self):
        self.display = None
        if DISPLAY_AVAILABLE:
            try:
                i2c = SoftI2C(scl=Pin(I2C_SCL), sda=Pin(I2C_SDA))
                self.display = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)
                print("Display OLED inicializado com sucesso")
            except Exception as e:
                print(f"Erro ao inicializar display: {e}")
                self.display = None
    
    def update_display(self, wifi_status, mqtt_status, relay_a_state, relay_b_state):
        """Atualiza o display com as informações do sistema"""
        if not self.display:
            return
        
        try:
            self.display.fill(0)
            self.display.text("BitDogLab Controller", 0, 0)
            self.display.text(f"WiFi: {wifi_status}", 0, 16)
            self.display.text(f"MQTT: {mqtt_status}", 0, 24)
            self.display.text(f"Rele A: {relay_a_state}", 0, 40)
            self.display.text(f"Rele B: {relay_b_state}", 0, 48)
            self.display.show()
        except Exception as e:
            print(f"Erro ao atualizar display: {e}")
    
    def show_message(self, message, line=0):
        """Exibe uma mensagem simples no display"""
        if not self.display:
            return
        
        try:
            if line == 0:
                self.display.fill(0)
            self.display.text(message, 0, line * 8)
            self.display.show()
        except Exception as e:
            print(f"Erro ao exibir mensagem no display: {e}")
    
    def clear(self):
        """Limpa o display"""
        if not self.display:
            return
        
        try:
            self.display.fill(0)
            self.display.show()
        except Exception as e:
            print(f"Erro ao limpar display: {e}")
    
    def is_available(self):
        """Verifica se o display está disponível"""
        return self.display is not None

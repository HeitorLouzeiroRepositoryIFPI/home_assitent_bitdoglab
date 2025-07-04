"""
Gerenciador de Conexão WiFi

Esta classe gerencia a conexão WiFi do sistema.
"""

import network
import time
from config.config import WIFI_SSID, WIFI_PASSWORD, WIFI_TIMEOUT


class WiFiManager:
    """Classe para gerenciar a conexão WiFi"""
    
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.status = "Desconectado"
    
    def connect(self):
        """Conecta ao WiFi"""
        self.wlan.active(True)
        if not self.wlan.isconnected():
            self.status = "Conectando..."
            print(f"Conectando à rede {WIFI_SSID}...")
            self.wlan.connect(WIFI_SSID, WIFI_PASSWORD)
            timeout_wifi = 0
            while not self.wlan.isconnected() and timeout_wifi < WIFI_TIMEOUT:
                print(".", end="")
                time.sleep(1)
                timeout_wifi += 1
            
            if self.wlan.isconnected():
                self.status = "Conectado"
                print(f"\nConectado ao Wi-Fi! IP: {self.wlan.ifconfig()[0]}")
                return True
            else:
                self.status = "Erro"
                print("\nFalha ao conectar ao Wi-Fi.")
                return False
        
        self.status = "Conectado"
        print(f"Já conectado ao Wi-Fi. IP: {self.wlan.ifconfig()[0]}")
        return True
    
    def disconnect(self):
        """Desconecta do WiFi"""
        if self.wlan.isconnected():
            self.wlan.disconnect()
        self.wlan.active(False)
        self.status = "Desconectado"
        print("Desconectado do Wi-Fi")
    
    def is_connected(self):
        """Verifica se está conectado ao WiFi"""
        return self.wlan.isconnected()
    
    def get_ip(self):
        """Retorna o IP atual"""
        if self.wlan.isconnected():
            return self.wlan.ifconfig()[0]
        return None
    
    def get_network_info(self):
        """Retorna informações completas da rede"""
        if self.wlan.isconnected():
            config = self.wlan.ifconfig()
            return {
                'ip': config[0],
                'subnet': config[1],
                'gateway': config[2],
                'dns': config[3]
            }
        return None
    
    def scan_networks(self):
        """Escaneia redes WiFi disponíveis"""
        self.wlan.active(True)
        networks = self.wlan.scan()
        available_networks = []
        
        for net in networks:
            ssid = net[0].decode('utf-8')
            rssi = net[3]
            available_networks.append({'ssid': ssid, 'rssi': rssi})
        
        return available_networks
    
    def get_status(self):
        """Retorna o status atual da conexão"""
        return self.status

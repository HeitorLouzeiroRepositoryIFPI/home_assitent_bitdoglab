"""
Gerenciador de Conexão MQTT

Esta classe gerencia a comunicação MQTT do sistema.
"""

from umqtt.simple import MQTTClient
from config import MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD, MQTT_CLIENT_ID


class MQTTManager:
    """Classe para gerenciar a conexão MQTT"""
    
    def __init__(self, relay_a, relay_b):
        self.client = None
        self.status = "Desconectado"
        self.relay_a = relay_a
        self.relay_b = relay_b
        self.is_connected = False
    
    def mqtt_callback(self, topic, msg, *args):
        """Callback para mensagens MQTT"""
        print(f"Mensagem recebida - Tópico: {topic.decode()}, Mensagem: {msg.decode()}")
        comando = msg.decode().upper()
        topic_str = topic.decode()
        
        # Controle do Relé A
        if topic_str == self.relay_a.mqtt_topic_command:
            self.relay_a.handle_mqtt_command(comando, self.client)
        # Controle do Relé B
        elif topic_str == self.relay_b.mqtt_topic_command:
            self.relay_b.handle_mqtt_command(comando, self.client)
        else:
            print(f"Mensagem recebida em tópico inesperado: {topic_str}")
    
    def connect(self):
        """Conecta ao broker MQTT"""
        try:
            self.client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
            self.client.set_callback(self.mqtt_callback)
            
            self.status = "Conectando..."
            self.client.connect()
            self.status = "Conectado"
            self.is_connected = True
            print(f"Conectado ao broker MQTT: {MQTT_BROKER}")
            
            # Inscreve nos tópicos de comando dos dois relés
            self.client.subscribe(self.relay_a.mqtt_topic_command)
            self.client.subscribe(self.relay_b.mqtt_topic_command)
            print(f"Inscrito nos tópicos: {self.relay_a.mqtt_topic_command} e {self.relay_b.mqtt_topic_command}")
            
            # Publica disponibilidade e estados iniciais
            self.publish_availability()
            self.publish_initial_states()
            
            return True
            
        except OSError as e:
            self.status = "Erro"
            self.is_connected = False
            print(f"Falha ao conectar ao broker MQTT: {e}")
            return False
        except Exception as e:
            self.status = "Erro"
            self.is_connected = False
            print(f"Outro erro MQTT: {e}")
            return False
    
    def publish_availability(self):
        """Publica disponibilidade dos relés"""
        if self.client and self.is_connected:
            try:
                self.client.publish(self.relay_a.mqtt_topic_availability, b"online", retain=True)
                self.client.publish(self.relay_b.mqtt_topic_availability, b"online", retain=True)
            except Exception as e:
                print(f"Erro ao publicar disponibilidade: {e}")
    
    def publish_initial_states(self):
        """Publica estados iniciais dos relés"""
        if self.client and self.is_connected:
            try:
                initial_state_a = "OFF" if self.relay_a.estado_atual == 0 else "ON"
                initial_state_b = "OFF" if self.relay_b.estado_atual == 0 else "ON"
                self.client.publish(self.relay_a.mqtt_topic_state, initial_state_a.encode(), retain=True)
                self.client.publish(self.relay_b.mqtt_topic_state, initial_state_b.encode(), retain=True)
            except Exception as e:
                print(f"Erro ao publicar estados iniciais: {e}")
    
    def check_messages(self):
        """Verifica mensagens MQTT"""
        if self.client and self.is_connected:
            try:
                self.client.check_msg()
            except Exception as e:
                print(f"Erro ao verificar mensagens MQTT: {e}")
                self.is_connected = False
                self.status = "Erro"
    
    def publish(self, topic, message, retain=False):
        """Publica uma mensagem MQTT"""
        if self.client and self.is_connected:
            try:
                if isinstance(message, str):
                    message = message.encode()
                self.client.publish(topic, message, retain=retain)
                return True
            except Exception as e:
                print(f"Erro ao publicar mensagem MQTT: {e}")
                return False
        return False
    
    def subscribe(self, topic):
        """Inscreve em um tópico MQTT"""
        if self.client and self.is_connected:
            try:
                self.client.subscribe(topic)
                print(f"Inscrito no tópico: {topic}")
                return True
            except Exception as e:
                print(f"Erro ao inscrever no tópico {topic}: {e}")
                return False
        return False
    
    def disconnect(self):
        """Desconecta do MQTT"""
        if self.client:
            try:
                # Publica offline antes de desconectar
                if self.is_connected:
                    self.client.publish(self.relay_a.mqtt_topic_availability, b"offline", retain=True)
                    self.client.publish(self.relay_b.mqtt_topic_availability, b"offline", retain=True)
                self.client.disconnect()
            except:
                pass
            self.client = None
        
        self.is_connected = False
        self.status = "Desconectado"
        print("Desconectado do broker MQTT")
    
    def get_status(self):
        """Retorna o status atual da conexão MQTT"""
        return self.status
    
    def reconnect(self):
        """Tenta reconectar ao MQTT"""
        print("Tentando reconectar ao MQTT...")
        self.disconnect()
        return self.connect()

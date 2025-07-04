# 🔌 Controlador de Relés BitDogLab

Sistema profissional de controle de 2 relés com botões físicos e integração MQTT, agora **completamente modular** para máxima manutenibilidade e extensibilidade.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Platform](https://img.shields.io/badge/platform-MicroPython-green)
![MQTT](https://img.shields.io/badge/MQTT-supported-orange)
![WiFi](https://img.shields.io/badge/WiFi-802.11-lightblue)

## 📁 Estrutura do Projeto

```
two_rele_control/
├── __init__.py              # Inicialização do pacote
├── main.py                  # Arquivo principal simplificado
├── config.py                # Configurações centralizadas
├── relay_controller.py      # Classe para controle de relés
├── display_controller.py    # Classe para display OLED
├── wifi_manager.py          # Classe para gerenciamento WiFi
├── mqtt_manager.py          # Classe para comunicação MQTT
├── system_controller.py     # Controlador principal do sistema
├── setup.py                 # Script de configuração inicial
├── README.md                # Esta documentação
├── CHANGELOG.md             # Histórico de versões
├── LICENSE                  # Licença MIT
├── configuration.yaml       # Config Home Assistant (opcional)
├── ssd1306.py               # Driver do display OLED
└── umqtt/                   # Biblioteca MQTT para MicroPython
    └── simple.py
```

## 🏗️ Arquitetura Modular

### **Módulos Principais**

#### 📦 `relay_controller.py`
**Classe**: `RelayController`
- Controla um relé individual
- Gerencia botão com debounce
- Publica estados via MQTT
- Processa comandos MQTT

#### 📦 `display_controller.py`
**Classe**: `DisplayController`
- Gerencia display OLED SSD1306
- Métodos para atualização e limpeza
- Verificação de disponibilidade
- Tratamento robusto de erros

#### 📦 `wifi_manager.py`
**Classe**: `WiFiManager`
- Conecta e monitora WiFi
- Escaneamento de redes
- Informações de rede completas
- Gerenciamento de status

#### 📦 `mqtt_manager.py`
**Classe**: `MQTTManager`
- Conecta ao broker MQTT
- Gerencia callbacks e mensagens
- Reconexão inteligente
- Publicação de disponibilidade

#### 📦 `system_controller.py`
**Classe**: `SystemController`
- Orquestra todos os componentes
- Loop principal otimizado
- Tratamento avançado de erros
- Status completo do sistema

#### 📦 `config.py`
**Configurações Centralizadas**
- Todas as constantes em um lugar
- Fácil personalização
- Valores organizados por categoria

## 🚀 Como Usar

### **Método 1: Execução Direta (Recomendado)**
```bash
# Upload dos arquivos para o microcontrolador
python main.py
```

### **Método 2: Uso Modular (Para Desenvolvedores)**
```python
# Importar apenas os componentes necessários
from relay_controller import RelayController
from wifi_manager import WiFiManager

# Usar individualmente
wifi = WiFiManager()
wifi.connect()

relay = RelayController(19, 6, "topic/state", "topic/cmd", "topic/avail", "A")
relay.set_state(1)  # Ligar relé
```

### **Método 3: Sistema Personalizado**
```python
from system_controller import SystemController

class MeuSistema(SystemController):
    def __init__(self):
        super().__init__()
        # Suas customizações aqui
    
    def run(self):
        # Lógica personalizada
        super().run()

# Usar sistema customizado
sistema = MeuSistema()
sistema.run()
```

## ⚙️ Configuração Rápida

### **1. Configurações de Rede**
Edite o arquivo `config.py` com suas credenciais:

```python
# Configurações de Rede WiFi
WIFI_SSID = "You-name-wifi"        # Substitua pelo nome da sua rede
WIFI_PASSWORD = "you-password"     # Substitua pela senha da sua rede

# Configurações do Broker MQTT  
MQTT_BROKER = "you-ip"             # IP do seu broker MQTT (ex: "192.168.1.100")
MQTT_PORT = 1883                   # Porta padrão MQTT
MQTT_USER = "you-user-mqtt"        # Usuário MQTT (ou "" se não usar auth)
MQTT_PASSWORD = "you-password-mqtt" # Senha MQTT (ou "" se não usar auth)
```

### **2. Configurações de Hardware**
Os pinos estão pré-configurados para a placa BitDogLab:

```python
# Pinos dos Relés
PIN_RELE_A = 19    # Relé A no GPIO 19
PIN_RELE_B = 20    # Relé B no GPIO 20

# Pinos dos Botões
PIN_BUTTON_A = 6   # Botão A no GPIO 6 (controla Relé A)
PIN_BUTTON_B = 5   # Botão B no GPIO 5 (controla Relé B)

# Display OLED I2C (opcional)
I2C_SDA = 14       # Pino SDA do display
I2C_SCL = 15       # Pino SCL do display
```

### **3. Tópicos MQTT Configurados**

#### **Relé A (GPIO 19)**
- 📤 **Comando**: `bitdoglab/rele/gpio19/set`
- 📥 **Estado**: `bitdoglab/rele/gpio19/state` 
- 🟢 **Status**: `bitdoglab/rele/gpio19/status`

#### **Relé B (GPIO 20)**
- 📤 **Comando**: `bitdoglab/rele/gpio20/set`
- 📥 **Estado**: `bitdoglab/rele/gpio20/state`
- 🟢 **Status**: `bitdoglab/rele/gpio20/status`

## 🔧 Funcionalidades

### **Controle Local**
- ✅ Botões físicos com debounce
- ✅ Estados visuais (LEDs/Display)
- ✅ Resposta instantânea

### **Controle MQTT**
- ✅ Comandos: `ON`, `OFF`, `TOGGLE`
- ✅ Estados em tempo real
- ✅ Disponibilidade (online/offline)
- ✅ Retain messages

### **Display OLED (Opcional)**
- ✅ Status WiFi e MQTT
- ✅ Estados dos relés
- ✅ Mensagens personalizadas
- ✅ Funciona sem display

### **Conectividade**
- ✅ WiFi com reconexão automática
- ✅ MQTT com recuperação inteligente
- ✅ Status detalhado de conexões

## 🎯 Vantagens da Arquitetura Modular

### **1. Manutenibilidade**
- 🔧 Cada módulo tem responsabilidade única
- 🐛 Debugging mais fácil e rápido
- 📝 Código bem documentado
- 🧪 Testes independentes

### **2. Extensibilidade**
```python
# Adicionar novo relé é simples:
relay_c = RelayController(21, 7, "topic3/state", "topic3/cmd", "topic3/avail", "C")

# Adicionar novo tipo de display:
class LCDController(DisplayController):
    def __init__(self):
        # Implementação para LCD
        pass
```

### **3. Reutilização**
- 📦 Módulos podem ser usados em outros projetos
- 🔄 Componentes intercambiáveis
- 🎛️ Configuração flexível

### **4. Flexibilidade**

### **4. Flexibilidade**
- 🔧 Use apenas os módulos necessários
- ⚡ Performance otimizada

### **5. Testabilidade**
```bash
# Executar o sistema principal
python main.py
```
- 🎨 Customização fácil

## 📊 Comandos MQTT

### **Comandos Disponíveis**
| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `ON` | Liga o relé | `mosquitto_pub -t "bitdoglab/rele/gpio19/set" -m "ON"` |
| `OFF` | Desliga o relé | `mosquitto_pub -t "bitdoglab/rele/gpio19/set" -m "OFF"` |
| `TOGGLE` | Alterna estado | `mosquitto_pub -t "bitdoglab/rele/gpio19/set" -m "TOGGLE"` |

### **Exemplos Práticos**

#### **Controlar via Mosquitto (Linux/Mac)**
```bash
# Ligar Relé A
mosquitto_pub -h you-ip -u you-user-mqtt -P you-password-mqtt \
  -t "bitdoglab/rele/gpio19/set" -m "ON"

# Desligar Relé B  
mosquitto_pub -h you-ip -u you-user-mqtt -P you-password-mqtt \
  -t "bitdoglab/rele/gpio20/set" -m "OFF"

# Alternar Relé A
mosquitto_pub -h you-ip -u you-user-mqtt -P you-password-mqtt \
  -t "bitdoglab/rele/gpio19/set" -m "TOGGLE"
```

#### **Monitorar Estados**
```bash
# Escutar estados dos relés
mosquitto_sub -h you-ip -u you-user-mqtt -P you-password-mqtt \
  -t "bitdoglab/rele/+/state"

# Escutar disponibilidade
mosquitto_sub -h you-ip -u you-user-mqtt -P you-password-mqtt \
  -t "bitdoglab/rele/+/status"
```

#### **Via Python (para automação)**
```python
import paho.mqtt.client as mqtt

def controlar_rele(host, user, password, rele, comando):
    client = mqtt.Client()
    client.username_pw_set(user, password)
    client.connect(host, 1883, 60)
    
    topic = f"bitdoglab/rele/gpio{rele}/set"
    client.publish(topic, comando)
    client.disconnect()

# Exemplos de uso
controlar_rele("you-ip", "you-user-mqtt", "you-password-mqtt", 19, "ON")
controlar_rele("you-ip", "you-user-mqtt", "you-password-mqtt", 20, "OFF")
```

## 🔄 Exemplos Avançados

### **Sistema com 3 Relés**
Para adicionar um terceiro relé, estenda a classe `SystemController` e `MQTTManager` seguindo o padrão dos relés existentes.

### **Sistema Customizado**
```python
class MeuSistema(SystemController):
    def __init__(self):
        super().__init__()
        self.contador = 0
    
    def run(self):
        # Implementação customizada
        pass
```

### **Monitoramento Avançado**
```python
# Obter status completo do sistema
status = system.get_system_status()
print(f"WiFi: {status['wifi']['ip']}")
print(f"MQTT: {status['mqtt']['connected']}")
print(f"Relés: A={status['relays']['relay_a']['state']}")
```

## 🧪 Testes e Debugging

### **Verificar Configuração**
```python
from config import *
print(f"WiFi: {WIFI_SSID}")
print(f"MQTT: {MQTT_BROKER}")
```

### **Debug Individual**
```python
# Testar apenas WiFi
from wifi_manager import WiFiManager
wifi = WiFiManager()
print(wifi.scan_networks())

# Testar apenas relé
from relay_controller import RelayController
relay = RelayController(19, 6, "test/state", "test/cmd", "test/avail", "Test")
relay.toggle()
```

## 🏠 Integração Home Assistant

### **Configuração Automática via MQTT Discovery**
O sistema é 100% compatível com Home Assistant. Adicione ao seu `configuration.yaml`:

```yaml
# Relé A (GPIO 19)
switch:
  - platform: mqtt
    name: "BitDogLab Relé A"
    state_topic: "bitdoglab/rele/gpio19/state"
    command_topic: "bitdoglab/rele/gpio19/set"
    availability_topic: "bitdoglab/rele/gpio19/status"
    payload_on: "ON"
    payload_off: "OFF"
    state_on: "ON"
    state_off: "OFF"
    optimistic: false
    qos: 0
    retain: true

  # Relé B (GPIO 20)  
  - platform: mqtt
    name: "BitDogLab Relé B"
    state_topic: "bitdoglab/rele/gpio20/state"
    command_topic: "bitdoglab/rele/gpio20/set"
    availability_topic: "bitdoglab/rele/gpio20/status"
    payload_on: "ON"
    payload_off: "OFF"
    state_on: "ON"
    state_off: "OFF"
    optimistic: false
    qos: 0
    retain: true
```

### **Automações Exemplo**
```yaml
# Automação: Ligar relé A ao pôr do sol
automation:
  - alias: "Ligar Relé A ao Pôr do Sol"
    trigger:
      platform: sun
      event: sunset
    action:
      service: switch.turn_on
      target:
        entity_id: switch.bitdoglab_rele_a

  # Automação: Desligar relé B após 30 minutos
  - alias: "Desligar Relé B após 30min"
    trigger:
      platform: state
      entity_id: switch.bitdoglab_rele_b
      to: 'on'
    action:
      - delay: '00:30:00'
      - service: switch.turn_off
        target:
          entity_id: switch.bitdoglab_rele_b
```

## 💾 Backup e Versionamento

### **Arquivos Importantes**
- `config.py` - Suas configurações
- `main.py` - Lógica principal
- Todos os módulos `.py`

### **Customizações**
- Crie novos módulos sem modificar os existentes
- Use herança para estender funcionalidades
- Mantenha configurações em `config.py`

## � Instalação e Setup

### **Pré-requisitos**
- **Hardware**: ESP32 ou similar com MicroPython
- **Software**: MicroPython firmware instalado
- **Rede**: WiFi 2.4GHz disponível
- **MQTT**: Broker MQTT configurado (Mosquitto, HiveMQ, etc.)
- **Opcional**: Display SSD1306 I2C 128x64

### **Passo a Passo**

#### **1. Preparar o Hardware**
```
ESP32 Connections:
├── GPIO 19 → Relé A (Sinal)
├── GPIO 20 → Relé B (Sinal)  
├── GPIO 6  → Botão A (Pull-up interno)
├── GPIO 5  → Botão B (Pull-up interno)
├── GPIO 14 → SDA Display (opcional)
├── GPIO 15 → SCL Display (opcional)
├── 3.3V    → VCC Display/Relés
└── GND     → GND Display/Relés
```

#### **2. Upload dos Arquivos**
```bash
# Copiar todos os arquivos para o ESP32
# Usando ampy, thonny, ou ferramenta similar:

ampy --port /dev/ttyUSB0 put config.py
ampy --port /dev/ttyUSB0 put main.py
ampy --port /dev/ttyUSB0 put relay_controller.py
ampy --port /dev/ttyUSB0 put display_controller.py
ampy --port /dev/ttyUSB0 put wifi_manager.py
ampy --port /dev/ttyUSB0 put mqtt_manager.py  
ampy --port /dev/ttyUSB0 put system_controller.py
ampy --port /dev/ttyUSB0 put ssd1306.py
ampy --port /dev/ttyUSB0 mkdir umqtt
ampy --port /dev/ttyUSB0 put umqtt/simple.py umqtt/simple.py
```

#### **3. Configurar Credenciais**
Edite `config.py` no ESP32:
```python
WIFI_SSID = "SUA_REDE_WIFI"
WIFI_PASSWORD = "SUA_SENHA_WIFI"
MQTT_BROKER = "IP_DO_SEU_BROKER"
MQTT_USER = "SEU_USUARIO_MQTT"
MQTT_PASSWORD = "SUA_SENHA_MQTT"
```

#### **4. Executar**
```python
# No ESP32 (via REPL ou boot.py):
import main
# ou simplesmente renomeie main.py para main.py se quiser autostart
```

## 📈 Performance

- ⚡ Loop principal otimizado (20ms)
- 🔄 Reconexão inteligente
- 💾 Uso eficiente de memória
- 🎯 Debounce configurável

## 🆘 Troubleshooting

### **Problemas Comuns**

#### **❌ Erro: "WiFi não conecta"**
```python
# Verificar configurações
from config import WIFI_SSID, WIFI_PASSWORD
print(f"SSID: {WIFI_SSID}")
print(f"Password: {'*' * len(WIFI_PASSWORD)}")

# Testar WiFi manualmente
from wifi_manager import WiFiManager
wifi = WiFiManager()
print(wifi.scan_networks())  # Ver redes disponíveis
```

**Soluções:**
- ✅ Verificar se o SSID está correto (case-sensitive)
- ✅ Confirmar senha do WiFi
- ✅ Verificar se a rede é 2.4GHz (ESP32 não conecta em 5GHz)
- ✅ Aproximar o ESP32 do roteador

#### **❌ Erro: "MQTT não conecta"**
```python
# Testar MQTT manualmente
from mqtt_manager import MQTTManager
from relay_controller import RelayController

relay_a = RelayController(19, 6, "test/state", "test/cmd", "test/avail", "Test")
relay_b = RelayController(20, 5, "test/state", "test/cmd", "test/avail", "Test")

mqtt = MQTTManager(relay_a, relay_b)
result = mqtt.connect()
print(f"MQTT conectado: {result}")
```

**Soluções:**
- ✅ Verificar IP do broker MQTT
- ✅ Confirmar porta (padrão: 1883)
- ✅ Verificar usuário e senha MQTT
- ✅ Testar broker com outro cliente (mosquitto_pub)
- ✅ Verificar firewall do broker

#### **❌ Erro: "Display não funciona"**
```python
# O sistema funciona sem display, mas para testar:
from display_controller import DisplayController
display = DisplayController()
print(f"Display disponível: {display.is_available()}")
```

**Soluções:**
- ✅ Sistema funciona normalmente sem display
- ✅ Verificar conexões I2C (SDA=14, SCL=15)
- ✅ Confirmar endereço I2C do display (0x3C padrão)
- ✅ Verificar alimentação do display (3.3V)

#### **❌ Erro: "Relés não funcionam"**
```python
# Testar relé individual
from relay_controller import RelayController
relay = RelayController(19, 6, "test/state", "test/cmd", "test/avail", "Test")
relay.toggle()
print(f"Estado do relé: {relay.estado_atual}")
```

**Soluções:**
- ✅ Verificar conexões GPIO (19 e 20)
- ✅ Confirmar alimentação dos módulos relé
- ✅ Testar com LED para verificar sinais GPIO
- ✅ Verificar se relés usam lógica invertida (padrão no código)

#### **❌ Erro: "Botões não respondem"**
```python
# Testar botão individual
from machine import Pin
button = Pin(6, Pin.IN, Pin.PULL_UP)
print(f"Estado do botão: {button.value()}")  # 1 = não pressionado, 0 = pressionado
```

**Soluções:**
- ✅ Verificar conexões dos botões (GPIO 5 e 6)
- ✅ Botões devem conectar GPIO ao GND quando pressionados
- ✅ Pull-up interno está habilitado no código
- ✅ Verificar debounce (250ms padrão)

### **Diagnóstico Automático**
```bash
# Execute o script de configuração para verificações
python setup.py
```

### **Logs Detalhados**
O sistema fornece logs detalhados:
```
Conectando à rede You-name-wifi...
Conectado ao Wi-Fi! IP: 192.168.1.100
Conectado ao broker MQTT: you-ip
Inscrito nos tópicos: bitdoglab/rele/gpio19/set e bitdoglab/rele/gpio20/set
Sistema pronto. Pressione os Botões A/B ou envie comandos MQTT.
```

### **Reset do Sistema**
```python
# Reset completo
import machine
machine.reset()

# Reset apenas do WiFi
from wifi_manager import WiFiManager
wifi = WiFiManager()
wifi.disconnect()
wifi.connect()
```

---

## 📞 Suporte e Contribuição

### **Suporte Técnico**
- 📧 **Email**: [Seu email de suporte]
- 📚 **Documentação**: Consulte o README.md e código fonte
- 🔧 **Debug**: Use logs detalhados do sistema
- 🐛 **Issues**: Reporte problemas com logs completos

### **Contribuir para o Projeto**
```bash
# Fork do projeto
git clone [seu-fork]
cd two_rele_control

# Fazer mudanças
# Criar branch para feature
git checkout -b minha-feature

# Commit e push
git commit -m "Adiciona nova funcionalidade"
git push origin minha-feature

# Abrir Pull Request
```

### **Roadmap Futuro**
- 🔄 Suporte a mais relés (3, 4, 8...)
- 📱 Interface web para configuração
- 🔔 Notificações push
- 📊 Histórico de acionamentos
- 🌡️ Integração com sensores
- � Agendamento de tarefas
- 🔐 Autenticação avançada

---

## ⭐ Como Ajudar

### **Dê uma Estrela** ⭐
Se este projeto te ajudou, considere dar uma estrela no repositório!

### **Compartilhe**
- 📢 Divulgue para outros desenvolvedores
- � Escreva tutoriais de uso
- 🎥 Crie vídeos explicativos

### **Melhore**
- 🐛 Reporte bugs encontrados
- 💡 Sugira novas funcionalidades
- 📖 Melhore a documentação
- 🧪 Adicione mais testes

---

## 📄 Licença

Este projeto está sob a licença **MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

```
MIT License

Copyright (c) 2025 BitDogLab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🏷️ Tags e Categorias

`#MicroPython` `#ESP32` `#MQTT` `#HomeAutomation` `#IoT` `#Relay` `#BitDogLab` `#HomeAssistant` `#WiFi` `#GPIO` `#Modular` `#OpenSource`

---

**Versão**: 2.0 - Modular  
**Última Atualização**: 3 de julho de 2025  
**Autor**: BitDogLab  
**Status**: ✅ Pronto para Produção

---

<div align="center">

### 🚀 **Sistema Profissional • Código Limpo • Documentação Completa** 🚀

*Feito com ❤️ pela comunidade BitDogLab*

</div>

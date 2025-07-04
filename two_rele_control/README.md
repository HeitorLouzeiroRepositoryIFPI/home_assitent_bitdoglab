# 🏠 Controlador de Relés BitDogLab - Home Assistant

<div align="center">

![BitDogLab](https://img.shields.io/badge/BitDogLab-2.0-blue?style=for-the-badge)
![MicroPython](https://img.shields.io/badge/MicroPython-3.4+-green?style=for-the-badge)
![MQTT](https://img.shields.io/badge/MQTT-Compatible-orange?style=for-the-badge)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Ready-red?style=for-the-badge)

</div>

Sistema profissional de controle de 2 relés com **MQTT**, **botões físicos** e **display OLED**, projetado para integração perfeita com **Home Assistant**.

---

## 📁 Estrutura do Projeto

```
two_rele_control/
├── 📂 src/                     # Código fonte principal
│   ├── 📂 controllers/         # Controladores do sistema
│   │   ├── __init__.py
│   │   ├── relay_controller.py     # Controle dos relés
│   │   ├── display_controller.py   # Controle do display OLED
│   │   └── system_controller.py    # Controlador principal
│   ├── 📂 managers/            # Gerenciadores de rede
│   │   ├── __init__.py
│   │   ├── wifi_manager.py         # Gerenciamento WiFi
│   │   └── mqtt_manager.py         # Gerenciamento MQTT
│   ├── 📂 drivers/             # Drivers de hardware
│   │   ├── __init__.py
│   │   └── ssd1306.py             # Driver display OLED
│   └── __init__.py
├── 📂 config/                  # Configurações
│   ├── __init__.py
│   ├── config.py                   # Configurações Python
│   └── configuration.yaml         # Config Home Assistant
├── 📂 lib/                     # Bibliotecas externas
│   └── umqtt/                      # Biblioteca MQTT
│       └── simple.py
├── 📂 docs/                    # Documentação
│   ├── README.md                   # Esta documentação
│   └── LICENSE                     # Licença MIT
├── main.py                     # Arquivo principal
├── boot.py                     # Script de inicialização MicroPython
└── test_imports.py             # Teste de imports (desenvolvimento)
```

---

## 🎯 Compatibilidade MicroPython

### **Imports Ajustados**
O projeto foi organizado para funcionar perfeitamente com **MicroPython**:

```python
# Imports absolutos (compatível com MicroPython)
from src.controllers.system_controller import SystemController
from config.config import WIFI_SSID, MQTT_BROKER
from lib.umqtt.simple import MQTTClient
```

### **Execução no MicroPython**
```python
# Opção 1: Direto
python main.py

# Opção 2: Via boot script  
python boot.py

# Opção 3: Teste de imports
python test_imports.py
```

---

## 🚀 Características

### **1. Arquitetura Modular**
- 🏗️ **Separação de responsabilidades** em módulos especializados
- 🔧 **Fácil manutenção** e extensibilidade
- 📦 **Imports organizados** com estrutura de pacotes Python
- 🎯 **Single Responsibility Principle** aplicado

### **2. Controle Inteligente**
- ⚡ **Duplo controle**: Botões físicos + MQTT
- 🔄 **Sincronização automática** entre físico e digital
- 🛡️ **Debounce** em botões físicos
- 📊 **Feedback visual** no display OLED

### **3. Conectividade Avançada**
- 📡 **WiFi** com reconexão automática
- 🔗 **MQTT** com tópicos organizados
- 🏠 **Home Assistant** ready com discovery automático
- 💾 **Configurações centralizadas**

### **4. Flexibilidade**
- 🔧 Use apenas os módulos necessários
- ⚡ Performance otimizada

### **5. Testabilidade**
```bash
# Executar o sistema principal
python main.py
```

---

## ⚙️ Configuração

### **1. Hardware**
```python
# Pinos dos relés
PIN_RELE_A = 4
PIN_RELE_B = 5

# Pinos dos botões
PIN_BUTTON_A = 14
PIN_BUTTON_B = 12

# Display I2C (opcional)
I2C_SDA = 21
I2C_SCL = 22
```

### **2. WiFi**
```python
# config/config.py
WIFI_SSID = "BitDogLab"
WIFI_PASSWORD = "sua_senha"
```

### **3. MQTT**
```python
# Broker
MQTT_BROKER = "192.168.1.100"
MQTT_PORT = 1883
MQTT_USER = "admin"
MQTT_PASSWORD = "admin"

# Tópicos organizados
MQTT_TOPIC_BASE = "bitdoglab/relay"
```

---

## 🏃‍♂️ Execução Rápida

### **1. Configurar**
```python
# Edite config/config.py com suas credenciais
nano config/config.py
```

### **2. Executar**
```bash
python main.py
```

### **3. Verificar Status**
O sistema exibirá no console e display:
- ✅ Status de conexão WiFi
- 🔗 Status de conexão MQTT  
- ⚡ Estado dos relés em tempo real

---

## 📋 Tópicos MQTT

### **Relé A**
```bash
# Estado atual
bitdoglab/relay/rele_a/state → "ON" | "OFF"

# Comando remoto  
bitdoglab/relay/rele_a/command ← "ON" | "OFF"

# Disponibilidade
bitdoglab/relay/rele_a/availability → "online" | "offline"
```

### **Relé B**
```bash
# Estado atual
bitdoglab/relay/rele_b/state → "ON" | "OFF"

# Comando remoto
bitdoglab/relay/rele_b/command ← "ON" | "OFF"

# Disponibilidade  
bitdoglab/relay/rele_b/availability → "online" | "offline"
```

---

## 🏠 Integração Home Assistant

### **1. Configuração Automática**
O sistema publica automaticamente a configuração dos dispositivos:

```yaml
# config/configuration.yaml (gerado automaticamente)
switch:
  - platform: mqtt
    name: "Relé A BitDogLab"
    state_topic: "bitdoglab/relay/rele_a/state"
    command_topic: "bitdoglab/relay/rele_a/command"
    availability_topic: "bitdoglab/relay/rele_a/availability"
    
  - platform: mqtt  
    name: "Relé B BitDogLab"
    state_topic: "bitdoglab/relay/rele_b/state"
    command_topic: "bitdoglab/relay/rele_b/command"
    availability_topic: "bitdoglab/relay/rele_b/availability"
```

### **2. Uso no Home Assistant**
- 🎛️ **Controle direto** via interface
- 🤖 **Automações** baseadas no estado dos relés
- 📊 **Histórico** completo de acionamentos
- 🔔 **Notificações** de mudança de estado

---

## 🛠️ Módulos Principais

### **SystemController** (`src/controllers/system_controller.py`)
- 🎛️ Orquestração de todos os componentes
- 🔄 Loop principal de execução
- ⚡ Gerenciamento de estado global

### **RelayController** (`src/controllers/relay_controller.py`)
- ⚡ Controle direto dos relés
- 🔘 Processamento de botões físicos
- 🛡️ Debounce e proteções

### **DisplayController** (`src/controllers/display_controller.py`)
- 📺 Gerenciamento do display OLED
- 📊 Exibição de status em tempo real
- 🎨 Interface visual organizada

### **WiFiManager** (`src/managers/wifi_manager.py`)
- 📡 Gerenciamento de conexão WiFi
- 🔄 Reconexão automática
- 📊 Monitoramento de sinal

### **MQTTManager** (`src/managers/mqtt_manager.py`)
- 🔗 Gerenciamento completo MQTT
- 📤 Publicação de estados
- 📥 Processamento de comandos

---

## 🔧 Desenvolvimento

### **Verificar Configuração**
```python
from config import *
print(f"WiFi: {WIFI_SSID}")
print(f"MQTT: {MQTT_BROKER}")
print(f"Relés: Pinos {PIN_RELE_A}, {PIN_RELE_B}")
```

### **Estrutura de Imports**
```python
# Imports organizados por módulo
from src.controllers import RelayController, DisplayController
from src.managers import WiFiManager, MQTTManager
from config import *
```

---

## 🆘 Troubleshooting

### **Problema: WiFi não conecta**
```bash
# Verificar credenciais
nano config/config.py

# Verificar sinal
# Status exibido no display e console
```

### **Problema: MQTT não conecta**
```bash
# Verificar broker
ping 192.168.1.100

# Verificar credenciais MQTT
nano config/config.py
```

### **Problema: Relés não respondem**
```bash
# Verificar pinagem
# Conferir config/config.py
# Testar botões físicos primeiro
```

### **Problema: Display não funciona**
```bash
# Verificar conexões I2C
# Sistema funciona sem display
# Erro exibido no console apenas
```

---

## 📞 Suporte

### **Comunidade BitDogLab**
- 🌐 **Site**: [bitdoglab.com](https://bitdoglab.com)
- 📧 **Email**: suporte@bitdoglab.com
- 💬 **Discord**: BitDogLab Community
- 📱 **Telegram**: @BitDogLab

### **Recursos Adicionais**
- 📖 **Wiki**: Documentação completa
- 🎥 **Tutoriais**: Canal no YouTube
- 🐛 **Issues**: GitHub Issues
- 💡 **Sugestões**: GitHub Discussions

---

## 📄 Licença

Projeto licenciado sob **MIT License**. Veja `docs/LICENSE` para detalhes.

---

## 🙏 Contribuindo

Contribuições são bem-vindas! Por favor:

1. 🍴 **Fork** o projeto
2. 🌿 **Crie** uma branch para sua feature
3. ✅ **Commit** suas mudanças
4. 📤 **Push** para a branch
5. 🔄 **Abra** um Pull Request

---

<div align="center">

**Desenvolvido com ❤️ pela comunidade BitDogLab**

[![BitDogLab](https://img.shields.io/badge/BitDogLab-Community-blue?style=social&logo=github)](https://github.com/bitdoglab)

</div>

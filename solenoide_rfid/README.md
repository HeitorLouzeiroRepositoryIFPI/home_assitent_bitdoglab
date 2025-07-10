# Controle de Solenoide RFID - Dois Setores

Este projeto implementa o controle de dois solenoides via MQTT para integração com Home Assistant.

## 🚀 Funcionalidades

- Controle de dois solenoides independentes (Setor 1 e Setor 2)
- Comunicação via MQTT
- Integração com Home Assistant
- Suporte a comandos ON/OFF/TOGGLE
- Reconexão automática em caso de falha
- Estados independentes para cada setor
- **LED interno indica status da conexão MQTT**

## 🔧 Hardware

- **Setor 1**: GPIO 16
- **Setor 2**: GPIO 17
- **LED Interno**: Indica status da conexão MQTT
- Raspberry Pi Pico W com conectividade Wi-Fi

## 📊 Tópicos MQTT

### Setor 1
- **Comando**: `pico/solenoid/setor1/set`
- **Estado**: `pico/solenoid/setor1/state`
- **Disponibilidade**: `pico/solenoid/setor1/status`

### Setor 2
- **Comando**: `pico/solenoid/setor2/set`
- **Estado**: `pico/solenoid/setor2/state`
- **Disponibilidade**: `pico/solenoid/setor2/status`

## ⚙️ Configuração

1. Configure suas credenciais Wi-Fi no arquivo `main.py`:
   ```python
   WIFI_SSID = "sua_rede"
   WIFI_PASSWORD = "sua_senha"
   ```

2. Configure o endereço do broker MQTT:
   ```python
   MQTT_BROKER = "192.168.0.100"
   MQTT_USER = "seu_usuario"
   MQTT_PASSWORD = "sua_senha"
   ```

3. Adicione a configuração do `configuration.yaml` no seu Home Assistant

4. Execute o script `main.py` no seu Raspberry Pi

## 💡 Indicadores Visuais

### LED Interno do Pico
- **Ligado**: Conectado ao broker MQTT
- **Desligado**: Desconectado do broker MQTT ou erro de conexão
- **Piscando**: Tentando reconectar (durante erros de rede)

O LED interno serve como indicador visual do status da conexão MQTT, facilitando o diagnóstico de problemas de conectividade.

## 🎮 Comandos Suportados

- `ON`: Liga o solenoide
- `OFF`: Desliga o solenoide
- `TOGGLE`: Inverte o estado atual

## 🏠 Home Assistant

O arquivo `configuration.yaml` contém a configuração completa para ambos os setores, criando dois switches independentes no Home Assistant:

- **Switch Setor 1**: `switch.raspberry_pi_solenoid_rfid_setor1`
- **Switch Setor 2**: `switch.raspberry_pi_solenoid_rfid_setor2`

## 📋 Estrutura do Projeto

```
solenoide_rfid/
├── main.py                    # Código principal do Raspberry Pi
├── configuration.yaml         # Configuração do Home Assistant
├── umqtt/
│   └── simple.py             # Biblioteca MQTT
├── README.md                 # Documentação original
└── README_DOIS_SETORES.md    # Esta documentação
```

## 🔄 Alterações Implementadas

### No `main.py`:
- Adicionado suporte ao segundo solenoide (GPIO 17)
- Criados tópicos MQTT independentes para cada setor
- Função `set_rele_state()` modificada para aceitar parâmetro de setor
- Callback MQTT atualizado para processar comandos de ambos os setores
- Inicialização e publicação de estado para ambos os setores

### No `configuration.yaml`:
- Duas entidades switch independentes
- Tópicos MQTT específicos para cada setor
- Configuração de dispositivo unificada
- Identificação única para cada switch

## 🐛 Solução de Problemas

### LED Interno Como Diagnóstico
- **LED sempre desligado**: Problema de conexão Wi-Fi ou MQTT
- **LED liga e desliga**: Conexão instável, verifique rede
- **LED ligado mas switches não funcionam**: Problema nos tópicos MQTT

### Dispositivo Não Aparece
1. Verifique se o LED interno está ligado (indica conexão MQTT)
2. Verifique se o broker MQTT está funcionando
3. Confirme se as credenciais estão corretas
4. Verifique os logs do Home Assistant
5. Teste a conectividade MQTT com um cliente como MQTT Explorer

### Apenas Um Setor Funciona
1. Verifique se ambos os GPIOs estão conectados corretamente
2. Confirme se os tópicos MQTT estão diferentes para cada setor
3. Teste enviando comandos manualmente via MQTT para cada setor

### Switches Não Respondem
1. Verifique se o dispositivo está online
2. Confirme se os tópicos de comando estão corretos
3. Teste enviando comandos manualmente via MQTT
4. Verifique os logs do console do Raspberry Pi

## 📝 Exemplo de Uso via MQTT

```bash
# Ligar Setor 1
mosquitto_pub -h 192.168.0.100 -t "pico/solenoid/setor1/set" -m "ON"

# Desligar Setor 1
mosquitto_pub -h 192.168.0.100 -t "pico/solenoid/setor1/set" -m "OFF"

# Ligar Setor 2
mosquitto_pub -h 192.168.0.100 -t "pico/solenoid/setor2/set" -m "ON"

# Desligar Setor 2
mosquitto_pub -h 192.168.0.100 -t "pico/solenoid/setor2/set" -m "OFF"
```

## 🔍 Monitoramento

Para monitorar os estados dos setores:

```bash
# Monitorar estado Setor 1
mosquitto_sub -h 192.168.0.100 -t "pico/solenoid/setor1/state"

# Monitorar estado Setor 2
mosquitto_sub -h 192.168.0.100 -t "pico/solenoid/setor2/state"

# Monitorar todos os tópicos
mosquitto_sub -h 192.168.0.100 -t "pico/solenoid/+/+"
```

## 📞 Suporte

Para problemas específicos:
1. Verifique os logs do Home Assistant
2. Teste a conectividade MQTT
3. Confirme se o dispositivo está executando o código correto
4. Verifique se todas as configurações de rede estão corretas
5. Teste cada setor individualmente

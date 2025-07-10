# Configuração Home Assistant - Solenoide RFID

Este arquivo contém a configuração completa para integrar o solenoide controlado via MQTT ao Home Assistant.

## 📋 Pré-requisitos

1. Home Assistant instalado e funcionando
2. Broker MQTT configurado e acessível
3. Dispositivo ESP32/Raspberry Pi Pico executando o código `main.py`

## 🔧 Instalação

### Opção 1: Adicionar ao configuration.yaml principal

1. Abra o arquivo `configuration.yaml` do seu Home Assistant
2. Copie e cole o conteúdo do arquivo `configuration.yaml` deste projeto
3. Ajuste as configurações conforme necessário (IP do broker, credenciais, etc.)
4. Reinicie o Home Assistant

### Opção 2: Usar includes (recomendado)

1. Crie uma pasta `packages` na pasta de configuração do Home Assistant
2. Copie o arquivo `configuration.yaml` para `packages/solenoide_rfid.yaml`
3. Adicione no `configuration.yaml` principal:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
4. Reinicie o Home Assistant

## 🎛️ Entidades Criadas

### Switch
- **switch.solenoide_setor_1**: Controla o solenoide (ON/OFF)

### Sensor
- **sensor.solenoide_setor_1_status**: Monitora o status de conectividade

### Input Controls
- **input_number.irrigacao_duracao_setor1**: Define duração da irrigação
- **input_boolean.irrigacao_automatica_setor1**: Habilita/desabilita automação

### Scripts
- **script.irrigar_setor1**: Irriga por 1 minuto
- **script.irrigar_setor1_personalizado**: Irriga por tempo personalizado

### Automações
- **Ativar Solenoide por RFID**: Ativa quando cartão autorizado é detectado
- **Desativar Solenoide por RFID Não Autorizado**: Notifica acesso negado

## 📊 Tópicos MQTT Utilizados

- **Estado**: `pico/solenoid/setor1/state`
- **Comando**: `pico/solenoid/setor1/set`
- **Disponibilidade**: `pico/solenoid/setor1/status`
- **RFID** (opcional): `pico/rfid/setor1/card_detected`

## 🚀 Como Usar

### Controle Manual
1. Vá para a página inicial do Home Assistant
2. Encontre o switch "Solenoide Setor 1"
3. Clique para ligar/desligar

### Controle por Script
1. Vá para **Ferramentas do Desenvolvedor** > **Serviços**
2. Selecione `script.irrigar_setor1` ou `script.irrigar_setor1_personalizado`
3. Execute o script

### Automação por RFID
1. Configure o dispositivo para enviar dados RFID via MQTT
2. A automação será executada automaticamente quando um cartão for detectado

## 🔧 Personalização

### Alternar Tempo de Irrigação Padrão
```yaml
script:
  irrigar_setor1:
    sequence:
      - service: switch.turn_on
        target:
          entity_id: switch.solenoide_setor_1
      - delay: "00:02:00"  # Altere para 2 minutos
      - service: switch.turn_off
        target:
          entity_id: switch.solenoide_setor_1
```

### Adicionar Mais Setores
Para adicionar mais setores, duplique as configurações alterando:
- Tópicos MQTT (ex: `pico/solenoid/setor2/state`)
- Nomes das entidades (ex: `solenoide_setor_2`)
- Pinos no código do dispositivo

### Personalizar Ícones
```yaml
switch:
  - platform: mqtt
    name: "Solenoide Setor 1"
    icon: "mdi:sprinkler"  # Ou outro ícone de sua preferência
```

## 🐛 Solução de Problemas

### Dispositivo Não Aparece
1. Verifique se o broker MQTT está funcionando
2. Confirme se as credenciais estão corretas
3. Verifique os logs do Home Assistant
4. Teste a conectividade MQTT com um cliente como MQTT Explorer

### Automação Não Funciona
1. Verifique se os tópicos MQTT estão corretos
2. Teste manualmente enviando mensagens MQTT
3. Verifique os logs de automação no Home Assistant

### Switch Não Responde
1. Verifique se o dispositivo está online
2. Confirme se os tópicos de comando estão corretos
3. Teste enviando comandos manualmente via MQTT

## 📝 Logs Úteis

Para debugar problemas, habilite logs detalhados:

```yaml
logger:
  default: info
  logs:
    homeassistant.components.mqtt: debug
    homeassistant.components.switch.mqtt: debug
```

## 🔄 Backup e Restauração

Sempre faça backup do seu `configuration.yaml` antes de fazer alterações:

```bash
cp configuration.yaml configuration.yaml.backup
```

## 📞 Suporte

Para problemas específicos:
1. Verifique os logs do Home Assistant
2. Teste a conectividade MQTT
3. Confirme se o dispositivo está executando o código correto
4. Verifique se todas as configurações de rede estão corretas

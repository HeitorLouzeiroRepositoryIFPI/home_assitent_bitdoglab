"""
Controlador de Relés BitDogLab - Arquivo Principal

Sistema de controle de 2 relés com botões físicos e integração MQTT.
Agora organizado em módulos separados para melhor manutenibilidade.
"""

import sys
import os

# Adicionar os caminhos ao sys.path para importações
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from src.controllers.system_controller import SystemController


def main():
    """Função principal do programa"""
    print("=== Controlador de Relés BitDogLab ===")
    print("Versão: 2.0 - Modular")
    print("Autor: BitDogLab")
    print("=====================================\n")
    
    try:
        # Criar e executar o sistema
        system = SystemController()
        system.run()
        
    except KeyboardInterrupt:
        print("\nInterrupção detectada...")
        if 'system' in locals():
            system.shutdown()
        print("Programa finalizado pelo usuário.")
        
    except Exception as e:
        print(f"Erro crítico no programa principal: {e}")
        if 'system' in locals():
            system.shutdown()
        print("Programa finalizado devido a erro crítico.")


if __name__ == "__main__":
    main()
"""
Boot script para MicroPython
Configura os caminhos antes de executar o main.py
"""

import gc

# Executa garbage collection
gc.collect()

print("Sistema BitDogLab iniciando...")
print("Memória livre:", gc.mem_free())

# Importa e executa o main
try:
    import main
    main.main()
except Exception as e:
    print(f"Erro na inicialização: {e}")
    import sys
    sys.print_exception(e)

from libs.mfrc522 import MFRC522
import utime

# Configuração do leitor RFID
reader = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)

# Chave padrão para autenticação
DEFAULT_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

def read_card_data(uid, sector=8):
    """Lê dados de um setor específico do cartão"""
    if reader.auth(reader.AUTHENT1A, sector, DEFAULT_KEY, uid) == reader.OK:
        data = reader.read(sector)
        if data:
            print(f"Dados lidos do setor {sector}: {data}")
            
            # Extrair os bytes da tupla retornada
            if isinstance(data, tuple) and len(data) >= 2:
                byte_data = data[1]  # Os dados estão no segundo elemento da tupla
            else:
                byte_data = data
            
            # Converter bytes para texto
            text = ''.join([chr(b) for b in byte_data if isinstance(b, int) and b != 0 and 32 <= b <= 126])
            if text:
                print(f"Texto: '{text}'")
            else:
                print("Nenhum texto legível encontrado")
            return data
        else:
            print(f"Erro ao ler dados do setor {sector}")
    else:
        print(f"Erro de autenticação no setor {sector}")
    return None

def write_card_data(uid, text, sector=8):
    """Escreve texto em um setor específico do cartão"""
    if reader.auth(reader.AUTHENT1A, sector, DEFAULT_KEY, uid) == reader.OK:
        data = list(text.encode('utf-8')[:16])
        data.extend([0] * (16 - len(data)))
        
        stat = reader.write(sector, data)
        if stat == reader.OK:
            print(f"Dados escritos com sucesso no setor {sector}: '{text}'")
            return True
        else:
            print(f"Erro ao escrever dados no setor {sector}")
    else:
        print(f"Erro de autenticação no setor {sector}")
    return False

def show_menu():
    """Exibe o menu de opções"""
    print("\n=== RFID Reader/Writer ===")
    print("Escolha uma opção:")
    print("a - Apenas mostrar ID")
    print("r - Ler dados do cartão") 
    print("w - Escrever dados no cartão")
    print("q - Sair")
    return input("Digite sua opção (a/r/w/q): ").lower().strip()

def get_write_text():
    """Solicita o texto a ser escrito"""
    return input("Digite o texto para escrever (máx 16 caracteres): ")

def process_card_action(uid, action):
    """Processa a ação selecionada para o cartão"""
    if action == 'r':
        print("\nLendo dados do cartão...")
        read_card_data(uid)
    elif action == 'w':
        text_to_write = get_write_text()
        print(f"\nEscrevendo: '{text_to_write}'")
        if write_card_data(uid, text_to_write):
            print("Verificando escrita...")
            read_card_data(uid)
    elif action == 'a':
        print("Exibindo apenas o ID do cartão")
    else:
        print("Ação inválida!")

def wait_for_card(action):
    """Aguarda um cartão ser aproximado"""
    print(f"\nAguardando cartão... (Ação: {action.upper()})")
    print("Aproxime o cartão do leitor...")
    
    last_card = None
    
    while True:
        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                card = int.from_bytes(bytes(uid), "little")
                
                if card != last_card:
                    last_card = card
                    print(f"\nCARD ID: {card}")
                    print(f"UID: {[hex(i) for i in uid]}")
                    
                    # Processa a ação
                    process_card_action(uid, action)
                    reader.stop_crypto1()
                    
                    # Pergunta se quer continuar
                    continuar = input("\nDeseja fazer outra operação com este cartão? (s/n): ").lower()
                    if continuar != 's':
                        return
        else:
            if last_card is not None:
                last_card = None
                print("Cartão removido.")
                return
        
        utime.sleep_ms(100)

# Loop principal
print("=== Sistema RFID Interativo ===")

while True:
    action = show_menu()
    
    if action == 'q':
        print("Saindo...")
        break
    elif action in ['a', 'r', 'w']:
        wait_for_card(action)
    else:
        print("Opção inválida! Use a, r, w ou q.")
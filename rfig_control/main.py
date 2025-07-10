from libs.mfrc522 import MFRC522
import utime

# Configuração do leitor RFID
reader = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)

def read_card_data(uid):
    """Lê dados do cartão"""
    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    sector = 8
    
    if reader.auth(reader.AUTHENT1A, sector, key, uid) == reader.OK:
        data = reader.read(sector)
        if data:
            # Converter para texto se possível
            try:
                if isinstance(data, tuple) and len(data) >= 2:
                    byte_data = data[1]
                else:
                    byte_data = data
                text = ''.join([chr(b) for b in byte_data if 32 <= b <= 126])
                if text:
                    print(f"Texto: '{text}'")
                else:
                    print("Nenhum texto encontrado")
            except:
                print("Dados em formato binário")
        else:
            print("Erro ao ler dados")
    else:
        print("Erro de autenticação")

def wait_for_card():
    """Aguarda um cartão e mostra informações"""
    print("Aproxime o cartão do leitor...")
    
    last_card = None
    
    while True:
        reader.init()
        stat, _ = reader.request(reader.REQIDL)
        
        if stat == reader.OK:
            stat, uid = reader.SelectTagSN()
            if stat == reader.OK:
                card_id = int.from_bytes(bytes(uid), "little")
                
                # Só mostra se for um cartão diferente
                if card_id != last_card:
                    last_card = card_id
                    print(f"\nCARD ID: {card_id}")
                    
                    # Sempre lê e mostra os dados da tag
                    read_card_data(uid)
                    
                    reader.stop_crypto1()
        else:
            # Cartão removido
            if last_card is not None:
                last_card = None
                print("Cartão removido - aproxime outro cartão...")
        
        utime.sleep_ms(100)

# Loop principal
print("=== Sistema RFID===")
print("Pressione Ctrl+C para sair")

try:
    while True:
        wait_for_card()
except KeyboardInterrupt:
    print("\nSaindo...")
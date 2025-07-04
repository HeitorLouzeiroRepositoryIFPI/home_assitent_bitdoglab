from rfid_control.mfrc522 import MFRC522
import utime
import gc

# Configuração com tratamento de erro
try:
    reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)
    print("MFRC522 inicializado com sucesso!")
except Exception as e:
    print("Erro ao inicializar MFRC522:", e)
    raise

print("Bring TAG closer...")
print("Pressione Ctrl+C para parar")
print("")

try:
    while True:
        try:
            reader.init()
            (stat, tag_type) = reader.request(reader.REQIDL)
            if stat == reader.OK:
                (stat, uid) = reader.SelectTagSN()
                if stat == reader.OK:
                    card = int.from_bytes(bytes(uid),"little",False)
                    print("CARD ID: "+str(card))
                    # Pequena pausa adicional após leitura bem-sucedida
                    utime.sleep_ms(1000)
                else:
                    # Pausa menor quando não consegue ler o UID
                    utime.sleep_ms(100)
            else:
                # Pausa muito pequena quando não detecta cartão
                utime.sleep_ms(50)
            
            # Limpeza de memória periódica
            gc.collect()
            
        except Exception as e:
            print("Erro na leitura:", e)
            utime.sleep_ms(1000)
            
except KeyboardInterrupt:
    print("\nPrograma interrompido pelo usuário")
except Exception as e:
    print("Erro geral:", e)
finally:
    print("Finalizando programa...") 
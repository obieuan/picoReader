from mfrc522 import MFRC522
import machine
import os
from handleJson import post_asistencia

led_onboard = machine.Pin(0, machine.Pin.OUT)
prev_card  = ""
    
def dump_card_data(reader, uid):
    # Define the key for authentication (default is FFFFFFFFFFFFh)
    keyA = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    keyB = None  # Assuming no KeyB is set, or you can define it similarly

    # Dump all data from the card
    status = reader.MFRC522_DumpClassic1K(uid, keyA=keyA, keyB=keyB)
    if status == reader.ERR:
        print("Error dumping card data")
 
def read_data():
    global prev_card

    reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)
 
    #print("Bring TAG closer...")
    #print("")
    # Verificar si hay una tarjeta RFID presente
    (stat, tag_type) = reader.request(reader.REQIDL)
    
    if stat == reader.OK:
        led_onboard.value(1)
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            
            card = int.from_bytes(bytes(uid), "little", False)
            #print("New CARD ID: " + str(card))
            if prev_card != card:
                print("New CARD ID: " + str(card))
                prev_card = card
                codigo = post_asistencia(str(card))
                if codigo == -1:
                    prev_card = ""
                #print(codigo)
                return True
                # Process the new card scan (e.g., post_asistencia(str(card)))
            else:
                print("Duplicate Scan Ignored")
                # Handle the duplicate scan case if needed
    

# Leer la tarjeta RFID y mostrar el UID

read_data()

if __name__ == "__main__":    
    read_data()
    


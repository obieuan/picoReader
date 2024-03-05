from mfrc522 import MFRC522
import network
import urequests as requests
import ujson
import machine
import os
from secrets import ssid, password, tokenSalon, urlSalon

led_onboard = machine.Pin(0, machine.Pin.OUT)
prev_card  = ""

def post_json(url, json_data):
    """Envía un POST con JSON a una URL.

    Args:
        url: La URL a la que se enviará la solicitud.
        json_data: Los datos JSON a enviar.

    Returns:
        La respuesta de la solicitud.
    """

    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, json=json_data)  # Use json parameter to send JSON data
    except Exception as e:
        print("Error sending JSON request:", str(e))
        return None
    return response

def post_asistencia(card):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    json_data = {
        "TokenSalon": tokenSalon,
        "TarjetaAlumno": card,
        "Comando": "Ping"
        }
    # Enviar la solicitud de ping
    response = post_json(urlSalon, json_data)
    print("PING CARD")
    print(response.status_code)
    
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
            # Print the raw UID bytes
            print("Raw UID bytes:", uid)

            # Convert UID bytes to integer with big endian
            card_big_endian = int.from_bytes(bytes(uid), "big", False)
            print("Card ID (big endian):", card_big_endian)

            # Convert UID bytes to a hexadecimal string using direct conversion
            card_hex = ''.join('{:02x}'.format(x) for x in uid)
            print("Card ID (hexadecimal):", card_hex.upper())

            # Your existing logic...
            card = int.from_bytes(bytes(uid), "little", False)
            print("Card ID (little endian):", card)
            
            # Convert hexadecimal string to integer
            card_hex_int = int(card_hex, 16)
            print("Card ID (hex to int):", card_hex_int)
            
                    # Check for partial matches or different portions
            print("Last 4 digits of card (hex):", card_hex[-4:])
            print("Last 4 digits of card (int):", card_big_endian % 10000)
            
                        # Reverse the UID bytes
            uid_reversed = uid[::-1]

            # Convert reversed UID bytes to integer with big endian
            card_reversed_big_endian = int.from_bytes(bytes(uid_reversed), "big", False)
            print("Reversed Big Endian Card ID:", card_reversed_big_endian)


            # Dump all data from the card
            #dump_card_data(reader, uid)
            
            #card = int.from_bytes(bytes(uid), "little", False)
            if prev_card != card:
                print("New CARD ID: " + str(card))
                prev_card = card
                post_asistencia(str(card))
                #return True
                # Process the new card scan (e.g., post_asistencia(str(card)))
            #else:
                #print("Duplicate Scan Ignored")
                # Handle the duplicate scan case if needed
    

# Leer la tarjeta RFID y mostrar el UID

read_data()

if __name__ == "__main__":    
    read_data()
    


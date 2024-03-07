import os
import time
from ping import ping_routine
from data_read import read_data
from secrets import retraso
from machine import Pin

# Estados posibles
PING_STATE = 0
READ_DATA_STATE = 1

ledRed = Pin(0, Pin.OUT)
ledGreen = Pin(1, Pin.OUT)
ledBlue = Pin(2, Pin.OUT)

current_state = PING_STATE  # Estado inicial

def main():
    global current_state
    ping_timer = time.ticks_ms()

    
    # Lazo principal
    while True:
        print(current_state)
        if current_state == PING_STATE:  #Si current_state = 0
            
            # Ejecutar la rutina de ping cada tiempo de retraso en secrets
            if time.ticks_diff(time.ticks_ms(), ping_timer) >= retraso:
                print("ping")
                ledRed.on()
                ping_routine()
                ledRed.off()
                ping_timer = time.ticks_ms()
            
            # Cambiar al estado de lectura de datos si se detecta una tarjeta RFID
            if read_data():                
                current_state = READ_DATA_STATE
                
                
        
        elif current_state == READ_DATA_STATE: #Si current_state = 1
            # Realizar acciones relacionadas con la lectura de datos aquí
            print("rutina")            
            # Volver al estado de ping después de la lectura
            current_state = PING_STATE

if __name__ == "__main__":
    ledRed.off()
    ledGreen.off()
    ledBlue.off()
    main()






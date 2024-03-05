import serial


Rpi= serial.Serial(port = "COM5", baudrate=115200)

try:
    Rpi.Open()
    print("Conectado")
except:
 #   Rpi.close()
    if(Rpi.isOpen()):
        print("Conectado")
    else:
        print("No conectado")

while True :
    if (Rpi.isOpen()):
        xs=Rpi.readline() #Esto se recibe en bytes.
        x = xs.decode('UTF-8') #Conversión de Byte a String
        print(x)
        Rpi.close()
             
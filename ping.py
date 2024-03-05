# ping.py
import network
import urequests as requests
import ujson
import os
from secrets import ssid, password, tokenPanelPico, urlPanelPico
from handleJson import post_json

def download_and_save_file(file_url, file_name):
    """Descarga un archivo desde una URL y lo guarda en la Raspberry Pi Pico W.

    Args:
        file_url: La URL del archivo a descargar.
        file_name: El nombre del archivo en el sistema de la Raspberry Pi Pico W.
    """

    response = requests.get(file_url)
    #print(response.content)
    if response.status_code == 200:
        with open(file_name, 'wt') as file:
            file.write(response.content)

def ping_routine():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    json_data = {
        "TokenDispositivo": tokenPanelPico,
        "Comando": "ping",
    }

    # Enviar la solicitud de ping
    try:            
        response = post_json(urlPanelPico, json_data)        
        print(response)
        print(response.status_code)
        
        
        #Procesar la respuesta del server
        if response is not None and response.status_code == 200:
            response_json = response.json()  # Parsear la respuesta JSON
            actualizacion = response_json.get("Actualizacion:")  # Obtener el valor "Actualizacion" (por defecto 0)
            #print(response_json)
            
            if actualizacion == 1:
                # Enviar los datos JSON de actualización
                update_json_data = {
                    "TokenDispositivo": tokenPanelPico,
                    "Comando": "actualizar",
                }
                update_response = post_json(urlPanelPico, update_json_data)
                print("RESPONSE UPDATE")
                print(update_response.status_code)

                # Procesar las actualizaciones y descargar archivos si es necesario
                try:
                    response_json = update_response.json()
                    actualizaciones = response_json.get("Actualizaciones", [])
                    tipo_actualizacion = response_json.get("TipoActualizacion", 0)
                    file_ids = []

                    for update in actualizaciones:
                        file_name = update.get("Nombre_archivo")
                        file_url = update.get("url_archivo")
                        file_id = update.get("id_actualizacion")

                        file_ids.append(file_id)

                        if file_name and file_url:
                            #file_url = file_url.replace("192.168.1.73","192.168.1.73:1234")
                            download_and_save_file(file_url, file_name)
                            print(f"File '{file_name}' downloaded and saved successfully.")
                            #print(file_url)

                    actualizaciones_list = [{"id_actualizacion": file_id} for file_id in file_ids]

                except Exception as e:
                    print("Error parsing JSON response:", str(e))

                # Enviar la confirmación de finalización
                print("SENDING ALL DONE")
                update_json_data = {
                    "TokenDispositivo": tokenPanelPico,
                    "Comando": "finalizar",
                    "TipoActualizacion": tipo_actualizacion,
                    "Actualizaciones": actualizaciones_list
                }
                update_response = post_json(urlPanelPico, update_json_data)
                print("RESPONSE UPDATE")
                print(update_response.status_code)

    except Exception as e:
        print("Error parsing JSON response:", str(e))
        print("Servidor caido... saliendo",str(e))

if __name__ == "__main__":
    ping_routine()

import network
import urequests as requests  # Use urequests as requests
import ujson
import os

# Connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Fill in your network name (ssid) and password here:
ssid = 'Millenium Falcon'
password = '9991732560'
wlan.connect(ssid, password)
token = '2y10k0vi6PxfhzZ3o1Q1uMIR..f93W95sxdS9YDy0r2W9p23u5mFof9.'

def post_json(url, json_data):
    """Envía un POST con JSON a una URL.

    Args:
        url: La URL a la que se enviará la solicitud.
        json_data: Los datos JSON a enviar.

    Returns:
        La respuesta de la solicitud.
    """

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=json_data)  # Use json parameter to send JSON data
    return response

def download_and_save_file(file_url, file_name):
    """Descarga un archivo desde una URL y lo guarda en la Raspberry Pi Pico W.

    Args:
        file_url: La URL del archivo a descargar.
        file_name: El nombre del archivo en el sistema de la Raspberry Pi Pico W.
    """

    response = requests.get(file_url)    
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)

if __name__ == "__main__":
    url = "http://192.168.1.73:8000/api/v1/consulta"
    json_data = {
        "TokenDispositivo": token,
        "Comando": "ping",
    }
    response = post_json(url, json_data)
    print("PING")
    print(response.status_code)
    #print(response.text)

    try:
        response_json = response.json()  # Parse the JSON response
        actualizacion = response_json.get("Actualizacion", 0)  # Get the "Actualizacion" value (default to 0)
        
        if actualizacion == 1:
            # Send the update JSON data
            update_json_data = {
                "TokenDispositivo": token,
                "Comando": "actualizar",
            }
            update_response = post_json(url, update_json_data)
            print("RESPONSE UPDATE")
            print(update_response.status_code)
            #print(update_response.text)
            
            print("UPDATING RASPBERRY PI")
            try:
                response_json = update_response.json()
                actualizaciones = response_json.get("Actualizaciones", [])
                tipo_actualizacion = response_json.get("TipoActualizacion", 0)  # Get the "Actualizacion" value (default to 0)
                file_ids = []

                for update in actualizaciones:
                    file_name = update.get("Nombre_archivo")
                    file_url = update.get("url_archivo")
                    file_id = update.get("id_actualizacion")
                    
                    file_ids.append(file_id)
                    
                    #print(f"File '{file_name}' trying with URL: '{file_url}'.")

                    if file_name and file_url:
                        download_and_save_file(file_url, file_name)
                        print(f"File '{file_name}' downloaded and saved successfully.")
                        
                        # Print the current working directory
                        #print("Current working directory:", os.getcwd())
                    
                    actualizaciones_list = [{"id_actualizacion": file_id} for file_id in file_ids]
    
            except Exception as e:
                print("Error parsing JSON response:", str(e))
                
            
            print("SENDING ALL DONE")
            # Send the ALL DONE JSON data
            update_json_data = {
                "TokenDispositivo": token,
                "Comando": "finalizar",
                "TipoActualizacion": tipo_actualizacion,
                "Actualizaciones": actualizaciones_list
            }
            #print(update_json_data)
            update_response = post_json(url, update_json_data)
            print("RESPONSE UPDATE")
            print(update_response.status_code)
            #print(update_response.text)
            
        
    except Exception as e:
        print("Error parsing JSON response:", str(e))

import network
import urequests as requests
import ujson
from secrets import ssid, password, tokenSalon, urlSalon



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
    #print(card)

    json_data = {
        "TokenSalon": tokenSalon,
        "TarjetaAlumno": card,
        "Comando": "Asistencia"
        }
    # Enviar la solicitud de ping
    response = post_json(urlSalon, json_data)
    if response is not None and response.status_code == 200:  #hay json y contestó OK
        response_json = response.json()  # Parsear la respuesta JSON directamente a un diccionario Python
        codigo = response_json.get('Codigo:')
        #print(codigo)
        print(response_json)
        return codigo
    if response is None or response.status_code != 200:
        return -1        
    #print("PING CARD")     
    #print(response)

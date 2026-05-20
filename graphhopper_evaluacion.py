# EVALUACION 2 GRAPHHOPPER ULLOA VEGA #

import requests
import urllib.parse

# URLs base Graphhopper
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"

# KEY DEL GRAPHH #
key = "e9ad5f12-d5db-44a7-bd06-b729fa2e1c1e" 

# Rendimiento promedio de combustible
RENDIMIENTO_KM_L = 12.0

def geocoding(location, key):
    while location == "":
        location = input("Vuelve a ingresar la ubicación: ")
    
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    
    if json_status == 200 and len(json_data.get("hits", [])) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
            
        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de la API Geocode: " + str(json_status) + "\nMensaje de error: " + json_data.get("message", "Error desconocido"))
    
    return json_status, lat, lng, new_loc

while True:
    print("\n" + "="*50)
    # Solicitud de Ciudad de Origen y salida con 'q'
    loc1 = input("Ciudad de Origen (o ingrese 'q' para salir): ")
    if loc1.lower() in ["q", "quit"]:
        print("Saliendo del programa...")
        break
    orig = geocoding(loc1, key)
    
    # Solicitud de Ciudad de Destino y salida con 'q'
    loc2 = input("Ciudad de Destino (o ingrese 'q' para salir): ")
    if loc2.lower() in ["q", "quit"]:
        print("Saliendo del programa...")
        break
    dest = geocoding(loc2, key)
    
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        # Armado de la URL de Routing
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": "car"}) + op + dp
        
        reply = requests.get(paths_url)
        paths_status = reply.status_code
        paths_data = reply.json()
        
        if paths_status == 200:
            # 1. Distancia en km 
            distancia_m = paths_data["paths"][0]["distance"]
            km = distancia_m / 1000
            
            # 2. Duración en horas, minutos y segundos
            tiempo_ms = paths_data["paths"][0]["time"]
            sec = int(tiempo_ms / 1000 % 60)
            minutos = int(tiempo_ms / 1000 / 60 % 60)
            hr = int(tiempo_ms / 1000 / 60 / 60)
            
            # 3. Combustible requerido en litros
            litros_combustible = km / RENDIMIENTO_KM_L
            
            print(f"Ruta desde {orig[3]} hasta {dest[3]}")
            print("=================================================")
            # Impresión con formato de 2 decimales
            print("Distancia del viaje: {:.2f} km".format(km))
            print("Duración del viaje: {:02d}:{:02d}:{:02d}".format(hr, minutos, sec))
            print("Combustible requerido: {:.2f} litros".format(litros_combustible))
            print("=================================================")
            
            # 4. Narrativa del viaje (Instrucciones)
            print("NARRATIVA DEL VIAJE:")
            print("=================================================")
            for instruccion in paths_data["paths"][0]["instructions"]:
                texto = instruccion["text"]
                distancia_paso = instruccion["distance"] / 1000
                print("{} ( {:.2f} km )".format(texto, distancia_paso))
                
            print("=================================================")
        else:
            print("Error de Routing API. Mensaje: " + paths_data.get("message", "Ruta no encontrada"))
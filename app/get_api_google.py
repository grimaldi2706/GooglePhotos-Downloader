import os
import csv
import pickle
from google.oauth2.credentials import Credentials # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from google.auth.transport.requests import Request  # type: ignore
from googleapiclient.discovery import build  # type: ignore
import requests
from app.tools import *
from flask import jsonify

def get_credentials(scopes, service_name):
    creds = None
    token_path = f'uploads/token_{service_name}.json'
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'uploads/credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_service(service_type, version, scopes):
    try:
        creds = get_credentials(scopes, service_type)
        service = build(
            service_type,
            version,
            credentials=creds,
            static_discovery=False
        )
        return service
    except Exception as e:
        print(f"Error al obtener el servicio {service_type}: {e}")
        print(f"Detalles del error: Scopes: {scopes}, Service Type: {service_type}, Version: {version}")
        return None

def get_photos(year):
    photos_scopes = ['https://www.googleapis.com/auth/photoslibrary']
    service = get_service('photoslibrary', 'v1', photos_scopes)
    if service:
        items = response_services(service,year)
        os.makedirs('download', exist_ok=True)
        media_ids_para_album = []
        for item in items:
                save_photo = safe_photo(item)
                """
                return save_photo
                base_url = item['baseUrl']
                filename = item['filename']
                mime_type = item.get('mimeType', '')
                media_id = item['id']
                creationTime = item['mediaMetadata']['creationTime']
                data_file = [
                    {'filename': filename,'mimeType': mime_type,'creationTime': creationTime,}
                ]
                
                safe_csv(data_file)
                
                media_type = '=d' if 'image' in mime_type else '=dv' if 'video' in mime_type else ''
                
                if media_type:
                    full_url = base_url + media_type
                    try:
                        r = requests.get(full_url)
                        if r.status_code == 200:
                            with open(os.path.join('download', filename), 'wb') as f:
                                f.write(r.content)
                            print(f"Descargado: {filename}")
                            media_ids_para_album.append(media_id)
                        else:
                            print(f"Error al descargar {filename}: status {r.status_code}")   
                    except Exception as e:
                        print(f"Error al descargar {filename}: {e}")
                """
        if len(items) == 0:
            data = [{'cantidad':0, 'data':'No se han encontrado Fotos', 'response': 'no_data'}]
        else:
            photos = [{'filename': i['filename'], 'url': i['baseUrl']} for i in items]
            data = [{'cantidad':len(photos), 'data':photos, 'response': 'success'}]
        return data
    else:
        data = [{'cantidad':0, 'data':'Erro al obtener fotos', 'response': 'error'}]
        return data
    
def safe_csv(data_file):
    ruta = "download/files_download_data.csv"
    os.makedirs('download', exist_ok=True)

    # Verifica si el archivo ya existe para no repetir encabezados
    archivo_existe = os.path.exists(ruta)
    campos = data_file[0].keys()

    with open(ruta, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        if not archivo_existe:
            writer.writeheader()
        writer.writerows(data_file)

    print(f"Fila añadida al CSV: {ruta}")
    return "Fila guardada correctamente"

def response_services(service,year):

    if not service:
        return []
    
    all_photos = []
    next_page_token = None

    while True:
        body = {
            "pageSize": 100,
            "filters": {
                "dateFilter": {
                    "dates": [
                        {
                            "year": year,
                            #"month": 11,
                        }
                    ]
                }
            }
        }

        if next_page_token:
            body["pageToken"] = next_page_token

        response = service.mediaItems().search(body=body).execute()

        media_items = response.get('mediaItems', [])
        all_photos.extend(media_items)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    #return jsonify({"count": len(all_photos)})
    return all_photos

def safe_photo(item):
    os.makedirs('download', exist_ok=True)
    media_ids_para_album = []
    base_url = item['baseUrl']
    filename = item['filename']
    mime_type = item.get('mimeType', '')
    media_id = item['id']
    creationTime = item['mediaMetadata']['creationTime']
    # Extraer año y mes de creationTime (formato: 'YYYY-MM-DDTHH:MM:SSZ')
    year = creationTime[:4]
    month = creationTime[5:7]
    # Crear carpeta por año y mes
    folder_path = os.path.join('download', year, month)
    os.makedirs(folder_path, exist_ok=True)
    # Guardar la ruta relativa en el CSV
    data_file = [
        {'filename': filename, 'mimeType': mime_type, 'creationTime': creationTime, 'folder': f'{year}/{month}'}
    ]
    safe_csv(data_file)
    media_type = '=d' if 'image' in mime_type else '=dv' if 'video' in mime_type else ''
    if media_type:
        full_url = base_url + media_type
        try:
            r = requests.get(full_url)
            if r.status_code == 200:
                with open(os.path.join(folder_path, filename), 'wb') as f:
                    f.write(r.content)
                print(f"Descargado: {filename} en {folder_path}")
                media_ids_para_album.append(media_id)
            else:
                print(f"Error al descargar {filename}: status {r.status_code}")   
        except Exception as e:
            print(f"Error al descargar {filename}: {e}")
    return "Archivo guardado correctamente"
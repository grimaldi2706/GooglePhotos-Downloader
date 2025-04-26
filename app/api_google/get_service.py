from googleapiclient.discovery import build
from api_google.serviceGoogle import get_credentials  # tu función get_credentials()
from api_google.get_service import *
from tools import *

def get_service(service_type, version, scopes):
    try:
        creds = get_credentials(scopes, service_type)
        service = build(service_type, version, credentials=creds)
        return service
    except Exception as e:
        print(f"Error al obtener el servicio {service_type}: {e}")
        return None
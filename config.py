import os

class Config:
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    SECRET_KEY = 'una_clave_secreta_segura'
    ALLOWED_EXTENSIONS = {'json'}

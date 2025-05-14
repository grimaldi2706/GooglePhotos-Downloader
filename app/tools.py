import os
from flask import Flask, request, redirect, url_for, flash, render_template, current_app
from werkzeug.utils import secure_filename

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'json'}

def allowed_file(filename):
    """Comprueba que el archivo tenga extensión .json"""
    return (
        '.' in filename 
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def savefile(request):
    """
    Guarda en disco el archivo subido bajo el campo 'archivo'.
    Retorna True si guardó correctamente, False en caso contrario.
    """
    # 1) Verifica que venga el campo 'archivo'
    if 'archivo' not in request.files:
        return False

    archivo = request.files['archivo']

    # 2) Verifica que el usuario haya seleccionado un archivo
    if archivo.filename == '':
        return False

    # 3) Valida extensión y guarda
    if archivo and allowed_file(archivo.filename):
        filename = 'credentials.json'
        destino = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        archivo.save(destino)
        return True
    # 4) Si no pasó la validación de extensión
    return False


def dd(text):
    print(text)
    exit()


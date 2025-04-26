import os
from flask import Blueprint, render_template, request
from app.tools import *

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/', methods=['GET', 'POST'])
def index():
    saveFile = savefile(request)
    if(saveFile):
        flash('Archivo subido exitosamente')

    return render_template('index.html')
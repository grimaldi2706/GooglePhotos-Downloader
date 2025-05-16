import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.tools import *
from app.get_api_google import *

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/', methods=['GET', 'POST'])
def index():
    saveFile = savefile(request)
    if(saveFile):
        flash('Archivo subido exitosamente')
    return render_template('index.html')

@main.route('/authGoogle', methods=['GET', 'POST'])
def authGoogle():
    year = request.form.get('year')
    return get_photos(year)

@main.route('/createfile', methods=['GET', 'POST'])
def createFile():
    return safe_csv("hola")
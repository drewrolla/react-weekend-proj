from app import app
from flask import render_template

from .models import User

import requests

@app.route('/')
def index():
    return render_template('index.html')

    
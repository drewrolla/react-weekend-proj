from flask_login import current_user
from app import app
from flask import render_template, request, redirect, url_for, flash

from .models import User

import requests

@app.route('/')
def index():
    return render_template('index.html')

    
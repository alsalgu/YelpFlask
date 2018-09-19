from flask import render_template, current_app
from flask import request
from app.main import bp

@bp.route('/')
def index():
    return render_template('index.html')
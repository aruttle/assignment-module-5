
from app import create_app, db
from flask_migrate import upgrade
from app.models import *  

app = create_app()

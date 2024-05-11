import os

from flask import Flask 

from flask_cors import CORS
from flask_migrate import Migrate

from .user.routes import user_bp

from .extensions import db

from myapp.celery_utils import make_celery

import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def is_running_in_docker():
    local_ip = get_local_ip()
    return local_ip.startswith("172.") or local_ip.startswith("192.168.") or local_ip.startswith("10.")


def create_app():
    app = Flask(__name__,
                )

    app.register_blueprint(user_bp) # Registra as rotas do Blueprint
    
    CORS(app) # Habilita o CORS para a aplicação

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql://user:hash@db.com/name")
    app.config["SECRET_KEY"] = "Oz8Z7Iu&DwoQKdw3#-46vy0n" # Chave secreta para uso do Flask

    if is_running_in_docker():
        app.config["CELERY_CONFIG"] = {"broker_url": "redis://redis", "result_backend": "redis://redis"}
    else:
        app.config["CELERY_CONFIG"] = {"broker_url": "redis://127.0.0.1:6379", "result_backend": "redis://127.0.0.1:6379"}

    db.init_app(app)
    
    migrate = Migrate(app, db)  # Possibilidade de migração de banco de dados adicionando novas entidades 
    
    celery = make_celery(app)
    celery.set_default()
    return app, celery
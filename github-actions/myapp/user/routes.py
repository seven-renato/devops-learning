from flask import Blueprint, jsonify

from myapp.user.tasks import redis_example

from ..models import User

user_bp = Blueprint('user_bp', __name__)

    
@user_bp.route("/collect/teste", methods=["GET"])
def teste_get():
    try:
        users = User.query.all()
        for user in users:
            redis_example.delay("/tmp", user.id) # Enviar para uma fila de processamento onde serão escritos os dados em um arquivo JSON
        # Tratamento todo feito com a utilização de multiplos workers em background o que poderia gerar concorrência para escrita em arquivo
        return jsonify({"message": "All user files created"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
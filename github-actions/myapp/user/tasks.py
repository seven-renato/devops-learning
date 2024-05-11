from celery import shared_task, group

from flask import jsonify

from ..extensions import db
from ..models import User


import json
import time
import fcntl

    
@shared_task(bind=True)
def add_to_queue(self, location, user_id):

    # Fila com controle de concorrência para escrita em arquivo
    filename = f'{location}/{user_id}.json'
    
    try:
        with open(filename, 'r+') as file:  
            fcntl.lockf(file, fcntl.LOCK_EX)
            
            try:
                # Tenta carregar o JSON existente no arquivo
                try:
                    json_data = json.load(file)  # Lê o conteúdo do arquivo
                except json.JSONDecodeError:
                    json_data = {"result": []}  # Se vazio ou corrompido, inicia um novo

                # Verifica se "result" é uma lista
                if not isinstance(json_data.get("result"), list):
                    json_data["result"] = []  # Corrige para uma lista, se necessário

                # Adiciona o novo dado
                user = User.query.get(user_id)
                if user:
                    json_data["result"].append(user)

                # Reescreve o arquivo com as alterações
                file.seek(0)  # Volta ao início do arquivo
                file.truncate()  # Limpa o arquivo antes de escrever
                json.dump(json_data, file, indent=4)  # Salva o novo conteúdo
                
            finally:
                fcntl.lockf(file, fcntl.LOCK_UN)  # Libera o bloqueio
        
        return True
    
    except Exception as e:
        return {"error": str(e)}

@shared_task(bind=True)
def redis_example(self, location, user_id):
    add_to_queue(location, user_id) # Enviar para uma fila de processamento onde serão escritos os dados em um arquivo JSON
    time.sleep(10)
    print("Fazendo algumas coisas...")
    time.sleep(10)
    return True
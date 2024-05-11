from myapp import create_app

app, celery = create_app() # Cria a aplicação e o Celery
app.app_context().push()  # Push do contexto da aplicação para o app, para que o Celery possa acessar o banco de dados

if __name__ == '__main__':
    app.runserver(host='0.0.0.0')
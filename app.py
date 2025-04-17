from flask import Flask, render_template, request, url_for, redirect, flash, session
import database

database.criar_tabelas()

app = Flask(__name__)
app.secret_key = "chave_muito_segura"

@app.route('/') #rota para a página inicial
def index():
    return render_template('index.html')

# Cria um dicionário e usuários e senha, SERÁ MIGRADO PARA O BANCO DE DADOS
@app.route("/home")
def home():
    email = session.get("usuario")  # agora está correto
    if not email:
        return redirect(url_for('login'))

    celulares = database.obter_celulares_usuario(email)
    return render_template("home.html", celulares=celulares)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form  # Coletando os dados do formulário de login
        # Chamando a função 'login' do arquivo database para verificar a senha
        if database.login(form) == True:
            session['usuario'] = form['email'] # Armazena o email do usuário na sessão
            return redirect(url_for('home'))
        else:
            return "Ocorreu um erro ao fazer o login do usuário"  # Caso contrário, exibe mensagem de erro
    else:
        return render_template('login.html')  # Se for GET, renderiza o formulário de login
    
@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        form = request.form  # Coletando os dados do formulário de cadastro
        if database.criar_usuario(form) == True:
            return render_template('login.html')  # Se cadastro for bem-sucedido, redireciona para o login
        else:
            return "Ocorreu um erro ao cadastrar usuário"  # Caso contrário, exibe mensagem de erro
    else:
        return render_template('cadastro.html')  # Se for GET, renderiza o formulário de cadastro

if __name__ == '__main__':
    app.run(debug=True) 
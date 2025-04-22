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
    
@app.route('/excluir_usuario')
def excluir_usuario():
    email = session['usuario']
    
    if database.excluir_usuario(email):
        return redirect(url_for('login'))
    else:
        return "Ocorreu um erro ao excluir o usuário"

@app.route('/novo_celular', methods=["GET", "POST"])
def nova_musica():
    if request.method == "POST":
        form = request.form
        if database.novo_celular(form):
            return redirect(url_for('home'))  # redireciona para a função `home`
        else:
            return "Ocorreu um erro ao registrar o celular"
    else:
        return render_template('novo_celular.html')
    
@app.route('/editar_celular/<int:id>', methods=["GET", "POST"])
def editar_celular(id):
    email = session.get("usuario")
    if not email:
        return redirect(url_for('login'))

    if request.method == "POST":
        form = request.form
        form = dict(form)
        form['id'] = id
        if database.editar_celular(form):
            return redirect(url_for('home'))
        else:
            return "Erro ao editar celular"
    else:
        celular = database.obter_celular_por_id(id, email)
        if not celular:
            return "celular não encontrado"
        return render_template('editar_celular.html', celular=celular)

@app.route("/excluir_celular/<int:id>")
def excluir_celular(id):
    email = session.get("usuario")
    if not email:
        return redirect(url_for("login"))

    database.excluir_celular(id)
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True) 
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

def conectar_banco():
    conexao = sqlite3.connect("celulares.db")
    return conexao
# Função para criar as tabelas do banco de dados, caso não existam
def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Criando a tabela de usuários
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                   (email TEXT PRIMARY KEY, nome TEXT, senha TEXT)''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS celulares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT,
            modelo TEXT,
            processador TEXT,
            armazenamento TEXT,
            ram TEXT,
            caminho_capa TEXT,
            email_usuario TEXT,
            FOREIGN KEY(email_usuario) REFERENCES usuarios(email))
    ''')
    conexao.commit()
    
def criar_usuario(formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Verificando se o e-mail já está cadastrado
    cursor.execute('''SELECT COUNT(email) FROM usuarios WHERE email=?''', (formulario['email'],))
    conexao.commit()
    
    quantidade_de_emails = cursor.fetchone()
    print(quantidade_de_emails)
    
    # Se o e-mail já existir, retorna False
    if quantidade_de_emails[0] > 0:
        print("E-mail já cadastrado! Tente novamente")
        return False
    
    # Criptografando a senha do usuário
    senha_criptografada = generate_password_hash(formulario['senha'])
    
    # Inserindo os dados do novo usuário no banco
    cursor.execute('''INSERT INTO usuarios(email, nome, senha) 
                   VALUES (?, ?, ?)''', (formulario['email'], formulario['usuario'], senha_criptografada))
    
    conexao.commit()
    return True

def login(formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Verificando se o e-mail existe no banco de dados
    cursor.execute('''SELECT COUNT(email) FROM usuarios WHERE email=?''', (formulario['email'],))
    conexao.commit()
    
    quantidade_de_emails = cursor.fetchone()
    print(quantidade_de_emails)
    
    # Se o e-mail não estiver cadastrado, retorna False
    if quantidade_de_emails[0] == 0:
        print("E-mail não cadastrado! Tente novamente")
        return False
    
    # Obtendo a senha criptografada do usuário no banco
    cursor.execute('''SELECT senha FROM usuarios WHERE email=?''', (formulario['email'],))
    conexao.commit()
    senha_criptografada = cursor.fetchone()
    
    # Verificando se a senha fornecida corresponde à senha armazenada
    return check_password_hash(senha_criptografada[0], formulario['senha'])

def obter_celulares_usuario(email_usuario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute('''
    SELECT id, marca, modelo, processador, armazenamento, ram, caminho_capa
    FROM celulares
    WHERE email_usuario=?
''', (email_usuario,))

    celulares = cursor.fetchall()
    return celulares

def excluir_usuario(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute('''DELETE FROM celulares WHERE email_usuario=?''', (email,))
    cursor.execute('''DELETE FROM usuarios WHERE email=?''', (email,))
    conexao.commit()
    return True
    
def novo_celular(formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        INSERT INTO celulares (marca, modelo, processador, armazenamento, ram, caminho_capa, email_usuario)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        formulario['marca'],
        formulario['modelo'],
        formulario['processador'],
        formulario['armazenamento'],
        formulario['ram'],
        formulario.get('caminho_capa', '/static/img/celular_generico.png'),  # valor padrão se não tiver capa
        session.get('usuario') # pega o email do usuário logado
    ))

    conexao.commit()
    return True

def obter_celular_por_id(id, email_usuario):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        SELECT id, marca, modelo, processador, armazenamento, ram, caminho_capa
        FROM celulares
        WHERE id=? AND email_usuario=?
    ''', (id, email_usuario))

    return cursor.fetchone()

def excluir_celular(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("DELETE FROM celulares WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()

def editar_celular(formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        UPDATE celulares
        SET marca=?, modelo=?, processador=?, armazenamento=?, ram=?, caminho_capa=?
        WHERE id=? AND email_usuario=?
    ''', (
        formulario['marca'],
        formulario['modelo'],
        formulario['processador'],
        formulario['armazenamento'],
        formulario['ram'],
        formulario['caminho_capa'],
        formulario['id'],
        session.get('usuario')
    ))

    conexao.commit()
    conexao.close()
    return True


if __name__ == '__main__':
   criar_tabelas()
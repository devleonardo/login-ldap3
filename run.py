from flask import Flask, render_template, request
from ldap3 import Server, Connection, SIMPLE, ALL
from config import *

app = Flask(__name__)

def ldap_authenticate(username, password):
    # Cria um objeto de servidor com as informações de conexão
    server = Server(LDAP_HOST, use_ssl=False ,get_info=ALL)
    # Cria uma conexão com o servidor LDAP
    conn = Connection(server, user=LDAP_USER_DN, password=LDAP_USER_PASSWORD, authentication=SIMPLE, auto_bind=True)

    # Faz uma busca LDAP para encontrar a entrada do usuário
    search_filter = f'(&(objectClass=user)(sAMAccountName={username})(memberOf={LDAP_GROUP_DN}))'
    conn.search(LDAP_BASE_DN, search_filter)

    # Verifica se a entrada do usuário foi encontrada
    if conn.entries:
        entry = conn.entries[0]
        # Tenta autenticar o usuário com a senha fornecida
        conn = Connection(server, user=entry.entry_dn, password=password, authentication=SIMPLE)
        if conn.bind():
            print(conn)
            # A autenticação foi bem sucedida
            return True
    # A autenticação falhou
    return False

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if ldap_authenticate(username, password):
            return render_template('home.html')
        else:
            error_message = f"*** A autenticação falhou. ***"
            return render_template("error.html", error_message=error_message)
    
    return render_template('login.html')
    
if __name__ == '__main__':
    app.run('0.0.0.0')

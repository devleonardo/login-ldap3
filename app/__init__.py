from flask import Flask, render_template, request, redirect, url_for, Blueprint, session
from ldap3 import Server, Connection, SIMPLE, ALL
from app.config import *
from flask_session import Session

app = Flask(__name__)
app.secret_key = '{LDAP_USER_PASSWORD}'

# Configura a sessão para usar o armazenamento do sistema de arquivos
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def ldap_authenticate(username, password):
    # Cria um objeto de servidor com as informações de conexão
    server = Server(LDAP_HOST, use_ssl=False ,get_info=ALL)
    # Cria uma conexão com o servidor LDAP
    conn = Connection(server, user=LDAP_USER_DN, password=LDAP_USER_PASSWORD, authentication=SIMPLE, auto_bind=True)

    # Faz uma busca LDAP para encontrar a entrada do usuário e se ele faz parte de um determinado grupo
    search_filter = f'(&(objectClass=user)(sAMAccountName={username})(memberOf={LDAP_GROUP_DN}))'
    conn.search(LDAP_BASE_DN, search_filter)

    # Verifica se a entrada do usuário foi encontrada
    if conn.entries:
        entry = conn.entries[0]
        # Tenta autenticar o usuário com a senha fornecida
        conn = Connection(server, user=entry.entry_dn, password=password, authentication=SIMPLE)
        if conn.bind():
            # A autenticação foi bem sucedida
            return True
    # A autenticação falhou
    return False

@app.route('/login', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if ldap_authenticate(username, password):
            # guarda a sessão do usuario quando logado
            session['logged_in'] = True
            return redirect(url_for('rdns.dashboard'))
        else:
            error_message = "Verifique se digitou corretamente o nome de usuário e senha ou contate um administrador do sistema."
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')
        
# renderiza a pagina de login em duas rotas / (raiz) e /login       
@app.route('/')
@app.route('/login')
def index():
    return render_template('login.html')
    
if __name__ == '__main__':
    app.run('0.0.0.0')

# Importa e registra o blueprint rdns
from app.rdns import app as rdns_app
app.register_blueprint(rdns_app)
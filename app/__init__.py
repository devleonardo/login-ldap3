from flask import Flask, render_template, request, redirect, url_for, Blueprint, session
from ldap3 import Server, Connection, SIMPLE, ALL, Attribute, MODIFY_REPLACE
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
            # Faz uma busca LDAP para obter os atributos da entrada do usuário
            conn.search(entry.entry_dn,
                        '(objectclass=*)',
                        attributes=['mail', 'displayName', 'description', 'givenName', 'userPrincipalName']
            )

            print(conn.password)

            if conn.entries:
                user_attributes = conn.entries[0].entry_attributes_as_dict
                # Lista de atributos
                first_name = user_attributes.get('givenName', [''])[0]
                user_id = user_attributes.get('userPrincipalName', [''])[0]
                displayName = user_attributes.get('displayName', [''])[0]
                description = user_attributes.get('description', [''])[0]
                mail = user_attributes.get('mail', [''])[0]
                # Filtrando dados
                userName = user_id.split('@')[0]
                domain = user_id.split('@')[1]
                # Armazene o primeiro nome do usuário na sessão
                session['first_name'] = first_name
                session['userName'] = userName
                session['displayName'] = displayName
                session['description'] = description
                session['mail'] = mail
                session['domain'] = domain
            # A autenticação foi bem sucedida
            # Exibir todas as informações do usuário
            return True
    # A autenticação falhou
    return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if ldap_authenticate(username, password):
            # Store the username in the session
            session['username'] = username
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

@app.route('/logout')
def logout():
    # Remove the 'logged_in' key from the session
    session.pop('logged_in', None)
    return render_template('login.html')

    
if __name__ == '__main__':
    app.run(debug=True)

# Importa e registra o blueprint rdns
from app.rdns import app as rdns_app
app.register_blueprint(rdns_app)
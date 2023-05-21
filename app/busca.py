from app.config import *
from flask import Flask, render_template, request, redirect, url_for, Blueprint, session
from ldap3 import Server, Connection, SIMPLE, ALL, Attribute, MODIFY_REPLACE
from flask_session import Session
import subprocess

app = Blueprint('busca', __name__)
busca = Blueprint('busca', __name__)

##################################################################################################################

@app.route('/busca')
def dashboard():
    # chega se o usuário esta logado, caso contrario, retorna a pagina de login
    if not session.get('logged_in'):
        return render_template('login.html')
    # Get the username from the session
    username = session.get('username')
    # caso logado, renderiza a pagina dashboard
    return render_template('busca.html')

##################################################################################################################

@app.route('/busca', methods=['GET', 'POST'])
def search_users():
    if not session.get('logged_in'):
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('busca.login'))

    if request.method == 'POST':
        search_query = request.form['search_query']
        
        # Perform the user search on the server
        server = Server(LDAP_HOST, use_ssl=False, get_info=ALL)
        conn = Connection(server, user=LDAP_USER_DN, password=LDAP_USER_PASSWORD, authentication=SIMPLE, auto_bind=True)
        search_filter = f'(&(objectClass=user)(|(sAMAccountName=*{search_query}*)(displayName=*{search_query}*)(mail=*{search_query}*)(memberOf=*{search_query}*)))'
        conn.search(LDAP_BASE_DN, search_filter, attributes=['mail', 'displayName', 'description', 'sAMAccountName', 'userPrincipalName', 'memberOf'])
        
        # Store the search results in a list
        search_results = []
        for entry in conn.entries:
            user_attributes = conn.entries[0].entry_attributes_as_dict
            # Lista de atributos
            
            grupo = user_attributes.get('memberOf', [''])
            group = subprocess.getoutput(f"less {grupo} | awk -F '=' '{{print $2}}' | awk -F ',' '{{print $1}}'")
            groupps = group.split()

            #########

            username = entry.sAMAccountName.value
            display_name = entry.displayName.value if 'displayName' in entry else ''
            description = entry.description.value if 'description' in entry else ''
            email = entry.mail.value if 'mail' in entry else ''
            # memberOf = entry.memberOf.value if 'memberOf' in entry else ''
            search_results.append((username, display_name, description, email, groupps))
        
        return render_template('busca.html', search_results=search_results)
    return render_template('busca.html')

##################################################################################################################

@app.route('/<username>', methods=['GET', 'POST'])
def user_details(username):
    if not session.get('logged_in'):
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('busca.login'))
    # Retrieve the user details from the LDAP server based on the username
    server = Server(LDAP_HOST, use_ssl=False, get_info=ALL)
    conn = Connection(server, user=LDAP_USER_DN, password=LDAP_USER_PASSWORD, authentication=SIMPLE, auto_bind=True)
    search_filter = f'(sAMAccountName={username})'
    conn.search(LDAP_BASE_DN, search_filter, attributes=['mail', 'displayName', 'description', 'sAMAccountName', 'userPrincipalName', 'memberOf'])
    
    # Check if a user with the given username exists
    if len(conn.entries) == 0:
        return render_template('user_not_found.html')
    
    # Retrieve the user attributes
    entry = conn.entries[0]
    user_attributes = entry.entry_attributes_as_dict
    
    # Extract the required user information
    username = entry.sAMAccountName.value
    display_name = entry.displayName.value if 'displayName' in entry else ''
    description = entry.description.value if 'description' in entry else ''
    email = entry.mail.value if 'mail' in entry else ''
    member_of = user_attributes.get('memberOf', [''])
    
    # Process the memberOf attribute to extract the groups
    groups = []
    for group in member_of:
        group_name = subprocess.getoutput(f"less {group} | awk -F '=' '{{print $2}}' | awk -F ',' '{{print $1}}'")
        groups.append(group_name)

    # Render the user details template
    return render_template('usuario.html', username=username, display_name=display_name, description=description, email=email, groups=groups)

##################################################################################################################

# Register the Blueprint
app.register_blueprint(busca)
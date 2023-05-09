from flask import Flask

app = Flask(__name__)

# CONFIGURAÇÃO DE ACESSO AO SERVIDOR LDAP
LDAP_HOST = 'ldap://localhost:389'
LDAP_BASE_DN = 'dc=exemplo,dc=com'
LDAP_USER_DN = 'userAdmin'
LDAP_USER_PASSWORD = 'senhaAdmin'
LDAP_GROUP_DN = 'CN=GRUPO,OU=UNIDADE_ORGANIZADORA,DC=exemplo,DC=com'

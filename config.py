from flask import Flask

app = Flask(__name__)
LDAP_HOST = 'ldap://localhost:389'
LDAP_BASE_DN = 'dc=exemplo,dc=com'
LDAP_USER_DN = 'admin'
LDAP_USER_PASSWORD = 'senhaAdmin'
LDAP_GROUP_DN = 'CN=GRUPO,OU=UNIDADE_ORGANIZADORA,DC=exemplo,DC=com'

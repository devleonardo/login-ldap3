from flask import Flask

app = Flask(__name__)
LDAP_HOST = 'ldap://192.168.101.243:389'
LDAP_BASE_DN = 'dc=intranet,dc=leste'
LDAP_USER_DN = 'glpi2'
LDAP_USER_PASSWORD = 'Leste@2023'
LDAP_GROUP_DN = 'CN=USERS_STI,OU=SISTEMASTI,DC=intranet,DC=leste'
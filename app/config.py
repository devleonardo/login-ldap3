from flask import Flask

app = Flask(__name__)
LDAP_HOST = 'ldap://localhost:389'
LDAP_BASE_DN = 'dc=exemplo,dc=com'
LDAP_USER_DN = 'admin'
LDAP_USER_PASSWORD = 'admin_password'
LDAP_GROUP_DN = 'CN=USERS_STI,OU=SISTEMASTI,DC=exemplo,DC=com'

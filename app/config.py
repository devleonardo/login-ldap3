from flask import Flask
from flask import Flask, render_template

app = Flask(__name__)
LDAP_HOST = 'ldap://localhost:389'
LDAP_BASE_DN = 'dc=exemplo,dc=com'
LDAP_USER_DN = 'user_admin'
LDAP_USER_PASSWORD = 'admin_password'
LDAP_GROUP_DN = 'CN=GROUP,OU=OU,DC=exemplo,DC=com'
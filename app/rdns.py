import dns.resolver
import ping3
from flask import Flask, render_template, request, Blueprint, redirect, url_for, session
import subprocess
from os import system

app = Blueprint('rdns', __name__)

# renderiza a pagina html
@app.route('/dashboard')
def dashboard():
    # chega se o usuário esta logado, caso contrario, retorna a pagina de login
    if not session.get('logged_in'):
        return render_template('login.html')
    # caso logado, renderiza a pagina dashboard
    return render_template('dashboard.html')

# Lista predefinida de servidores DNS
dns_servers = {
    "GOOGLE": "8.8.8.8",
    "OPEN-DNS": "208.67.222.222",
    "RDNS-ITB-01": "186.211.32.10",
    "RDNS-ITB-02": "200.202.111.10",
    "RDNS-MRC-01": "186.211.32.11",
    "RDNS-MRC-02": "200.202.111.11",
    "RDNS-NIT-01": "186.211.32.12",
    "RDNS-NIT-02": "200.202.111.12",
    "RDNS01": "186.211.32.58",
    "RDNS02": "186.211.32.98",
    "RDNS03": "186.211.32.59",
    "RDNS04": "186.211.32.56",
    "RDNS05": "200.202.111.58",
    "RDNS06": "200.202.111.98",
}

@app.route('/dashboard', methods=['POST','GET'])
def resolve_domain():
    # verificar se o uruario esta logado
    if not session.get('logged_in'):
        return redirect(url_for('rdns.login'))
    
    # recebe o domínio digitado no input do front
    domain = request.form['domain']
    results = []
    for dns_server_name, dns_server_ip in dns_servers.items():
        try:
            # retorna o ping
            ping_time = ping3.ping(dns_server_ip, timeout=3) * 1000 if ping3.ping(dns_server_ip, timeout=3) else None
            # resolve o domínio e tempo de resolução
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [dns_server_ip]
            # tempo para cada resposta
            resolver.timeout = 5
            resolver.lifetime = 5
            answer = resolver.query(domain, rdtype='A', rdclass='IN').response.to_text()

            # escreve as mensagens - sucesso, falha, timeout e erro
            results.append(f"<div class='alert alert-light' role='alert'><b>{dns_server_name}</b>: {domain}  <br><sucesso>Resolução de DNS bem-sucedida.</sucesso> <br><ping>Tempo de resolução: {round(ping_time)} ms</ping></div>")
        except dns.resolver.NXDOMAIN:
            results.append(f"<div class='alert alert-danger' role='alert'><b>{dns_server_name}</b>: {domain}  <br><falha>Não foi possível resolver o nome do domínio.</falha></div>")
        except dns.exception.Timeout:
            results.append(f"<div class='alert alert-warning' role='alert'><b>{dns_server_name}</b>: {domain}  <br><timeout>Tempo limite de consulta atingido.</timeout> <br><ping>Tempo de resolução: {round(ping_time)} ms</ping></div>")
        except dns.resolver.NoAnswer:
            results.append(f"<div class='alert alert-secondary' role='alert'><b>{dns_server_name}</b>: {domain}  <br><sem>Não foi possível obter uma resposta para a consulta.</sem> <br><ping>Tempo de resolução: {round(ping_time)} ms</ping></div>")
        except dns.exception.DNSException as e:
            results.append(f"<div class='alert alert-danger' role='alert'><b>{dns_server_name}</b>: {domain}  <br><errodns>Ocorreu um erro na consulta DNS</errodns></div>")

    # não exibe ping nem converte a saida para float ao dar erro 
    try:
        # expressão regular para retorna a média do ping
        output = subprocess.getoutput(f"ping -c 4 {domain} | awk -F '/' '{{print $5}}'")
        # converte o resultado em ponto flutuante
        convertFloat = float(output)
    except (ValueError, TypeError):
        # retornar o valor 0.0, caso haja erro no teste de ping devido a timaout ou bloqueios
        convertFloat = 0.0

    # retorna a lista ordenada em HTML
    ordered_list = '<ul class="container row">' + ''.join([f'<li class="col-4">{result}</li>' for result in results]) + '</ul>'
    # retorna o teste de ping no topo da página
    ordemPing = '<div class="ping container">' + 'Latência média ' +'<vfinal>'+ ''.join([f'{round(convertFloat, 1)}']) +'</vfinal>'+ ' ms' + '</div>'
    # imprime os testes na pagina renderizada
    return f"{dashboard()}{ordemPing}{ordered_list}"
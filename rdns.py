import dns.resolver
import ping3
from flask import Flask, render_template, request
import subprocess
from os import system

app = Flask(__name__)

# Lista predefinida de servidores DNS
dns_servers = {
    "GOOGLE": "8.8.8.8",
    "OPEN-DNS": "208.67.222.222",
}

# renderiza a pagina html
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST','GET'])
def resolve_domain():
    domain = request.form['domain'] # recebe o domínio digitado no input do front
    results = []
    
    #convertFloat = 0.0
    for dns_server_name, dns_server_ip in dns_servers.items():
        try:
                        # retorna o tempo de resolução de dominio
            ping_time = ping3.ping(dns_server_ip, timeout=3) * 1000 if ping3.ping(dns_server_ip, timeout=3) else None
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [dns_server_ip]
            resolver.timeout = 5
            resolver.lifetime = 5
            answer = resolver.query(domain, rdtype='A', rdclass='IN').response.to_text()


            # escreve as mensagens - sucesso, falha, timeout e erro
            results.append(f"<div class='alert alert-success' role='alert'><b>{dns_server_name}</b>: {domain}  <br><sucesso>Resolução de DNS bem-sucedida.</sucesso> <br><ping>Tempo de resolução: {round(ping_time)} ms</ping></div>")
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
        # retorna o ping
        output = subprocess.getoutput(f"ping -c 4 {domain} | awk -F '/' '{{print $5}}'")
        convertFloat = float(output)
    except (ValueError, TypeError):
        convertFloat = 0.0

    # retorna a lista ordenada em HTML
    ordered_list = '<ul class="container row">' + ''.join([f'<li class="col-4">{result}</li>' for result in results]) + '</ul>'
    # retorna o teste de ping no topo da página
    ordemPing = '<div class="ping container">' + 'Latência média ' +'<vfinal>'+ ''.join([f'{round(convertFloat, 1)}']) +'</vfinal>'+ ' ms' + '</div>'
    return f"{home()}{ordemPing}{ordered_list}"

# inicia a aplicação nos ip's disponíveis (127.0.0.1 ou 192.168.100.232)
if __name__ == '__main__':
    app.run('0.0.0.0')
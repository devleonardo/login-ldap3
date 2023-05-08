
# Autenticação via LDAP
Tela de login em Python com Flask e autenticação via ldap.
- **Biblioteca:** ldap3

>     def ldap_authenticate(username, password):
>         server = Server(LDAP_HOST, use_ssl=False ,get_info=ALL)
>         conn = Connection(server, user=LDAP_USER_DN, password=LDAP_USER_PASSWORD, authentication=SIMPLE, auto_bind=True)
>     
>         search_filter = f'(&(objectClass=user)(sAMAccountName={username})(memberOf={LDAP_GROUP_DN}))'
>         conn.search(LDAP_BASE_DN, search_filter)
>     
>         if conn.entries:
>             entry = conn.entries[0]
>             conn = Connection(server, user=entry.entry_dn, password=password, authentication=SIMPLE)
>             if conn.bind():
>                 print(conn)
>             return True
>         return False

Testes de resolução de nome com lista predefinida de dns, com tempo de resolução para cada dns e ping para o domínio resolvido.
- **Bibliotecas:** dns.resolver, ping3

>     def resolve_domain():
>          domain = request.form['domain'] 
>          results = []
>          for dns_server_name, dns_server_ip in dns_servers.items():
>               try:
>                    ping_time = ping3.ping(dns_server_ip, timeout=3) * 1000 if
>                    ping3.ping(dns_server_ip, timeout=3) else None 
>                    resolver = dns.resolver.Resolver()
>                    resolver.nameservers = [dns_server_ip]
>                    resolver.timeout = 5
>                    resolver.lifetime = 5
>                    answer = resolver.query(domain, rdtype='A', rdclass='IN').response.to_text()

Regex para deolver somente o avg:
***

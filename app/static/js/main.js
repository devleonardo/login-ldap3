// Seleciona o formulário
const form = document.querySelector('form');
// Adiciona um ouvinte de eventos ao evento "submit" do formulário
form.addEventListener('submit', function(event) {
    // Seleciona o campo de entrada
    const input1 = document.querySelector('input[name="domain"]');
    const input2 = document.querySelector('input[name="username"]');
    // Remove os espaços em branco do valor do campo de entrada
    input1.value = input1.value.trim();
    input2.value = input2.value.trim();
});


// Salvar login e senha no LocalStorage
function saveLoginData() {
    // Obtém os valores dos campos de login e senha
    var username = document.getElementsByName('username')[0].value;
    var password = document.getElementsByName('password')[0].value;

    // Verifica se o checkbox está marcado
    var rememberMe = document.getElementById('rememberMe').checked;

    if (rememberMe) {
        // Salva os dados de login no LocalStorage
        localStorage.setItem('username', username);
        localStorage.setItem('password', password);
    } else {
        // Remove os dados de login do LocalStorage
        localStorage.removeItem('username');
        localStorage.removeItem('password');
    }
}

// Função para carregar os dados de login do LocalStorage, se existirem
function loadLoginData() {
    var username = localStorage.getItem('username');
    var password = localStorage.getItem('password');

    if (username && password) {
        // Preenche os campos de login e senha com os valores do LocalStorage
        document.getElementsByName('username')[0].value = username;
        document.getElementsByName('password')[0].value = password;
    }
}

// Chama a função para carregar os dados de login quando a página é carregada
window.onload = loadLoginData;
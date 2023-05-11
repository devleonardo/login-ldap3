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
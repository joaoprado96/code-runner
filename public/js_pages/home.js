document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevenir envio padrão do formulário
    
    var RACF = document.getElementById('username').value;
    var SENHA = document.getElementById('password').value;
    
    // Armazenar no LocalStorage (NÃO é seguro para dados sensíveis)
    localStorage.setItem('RACF', RACF);
    localStorage.setItem('SENHA', SENHA);

    window.location.href = "sandbox.html";
});
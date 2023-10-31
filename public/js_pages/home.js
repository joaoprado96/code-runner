document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault(); // Prevenir envio padrão do formulário
    
    var RACF = document.getElementById('username').value;
    var SENHA = document.getElementById('password').value;
    
    // Armazenar no LocalStorage (NÃO é seguro para dados sensíveis)
    localStorage.setItem('RACF', RACF);
    localStorage.setItem('SENHA', SENHA);
    await Login(RACF,SENHA);
    window.location.href = "sandbox.html";
});


async function Login(racf,senha){
    const response = await fetch('/codes/ambiente_login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({usuario: racf, senha: senha})
        });
        const login = await response.json();
        return login;
}
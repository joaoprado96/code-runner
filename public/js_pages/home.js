document.addEventListener('DOMContentLoaded', function() {
    const configButton = document.getElementById('configButton');

    // Função para obter o token e redirecionar
    function getTokenAndRedirect() {
        fetch('/authorization') // Substitua '/authorization' pelo endpoint correto
            .then(response => {
                if (!response.ok) {
                    throw new Error('Falha ao obter o token');
                }
                return response.json();
            })
            .then(data => {
                const token = data.token;
                window.location.href = `admin.html?token=${token}`;
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Erro ao obter o token. Verifique o console para mais detalhes.');
            });
    }

    // Adiciona o evento de clique ao botão
    configButton.addEventListener('click', function(event) {
        event.preventDefault();
        getTokenAndRedirect();
    });
});

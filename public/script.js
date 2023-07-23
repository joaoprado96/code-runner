var modal = document.getElementById("myModal");
var btn = document.getElementById("myButton");
var span = document.getElementsByClassName("close")[0];
var modalContent = document.getElementById("modal-content"); // supõe-se que este é o elemento onde você deseja exibir o conteúdo do arquivo .txt

btn.onclick = async function() {
  // Faz uma solicitação GET para o arquivo .txt
  const response = await fetch('/regressive/1.txt');
  // Lê o texto da resposta
  const text = await response.text();
  // Insere o texto na div modal
  modalContent.textContent = text;

  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

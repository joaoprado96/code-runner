function criarNavbar() {
    var navbarHTML = `
    <nav class="nav">
        <i class="uil uil-bars navOpenBtn"></i>
        <a href="#" class="logo">Code Runner</a>

        <ul class="nav-links">
            <i class="uil uil-times navCloseBtn"></i>
            <li><a href="/home">home</a></li>
            <li><a href="/estabelecimentos">estabelecimentos</a></li>
            <li><a href="/informacoes">informacoes</a></li>
            <li><a href="/contato">contato</a></li>

        </ul>

        <i class="uil uil-search search-icon" id="searchIcon"></i>
        <div class="search-box">
            <i class="uil uil-search search-icon"></i>
            <input type="text" placeholder="Search here..." />
        </div>

        <div class="user-icon-container">
            <img src="icons/icon-usuariorx.png" alt="Usuário" class="user-icon">
            <div class="user-submenu">
            <a href="/login">login</a>
                <a href="/usuario">novo usuário</a>
                <a href="/perfil">minha conta</a>
                <a href="/destaques">destaques</a>
                <a href="/cadastro">cadastro</a>
            </div>
        </div>
    </nav>
    `;

    // Adiciona o navbar ao documento
    document.body.insertAdjacentHTML('afterbegin', navbarHTML);

    // Agora, inicialize os event listeners do navbar
    const nav = document.querySelector(".nav"),
        searchIcon = document.querySelector("#searchIcon"),
        navOpenBtn = document.querySelector(".navOpenBtn"),
        navCloseBtn = document.querySelector(".navCloseBtn");

    searchIcon.addEventListener("click", () => {
        nav.classList.toggle("openSearch");
        nav.classList.remove("openNav");
        if (nav.classList.contains("openSearch")) {
            return searchIcon.classList.replace("uil-search", "uil-times");
        }
        searchIcon.classList.replace("uil-times", "uil-search");
    });

    navOpenBtn.addEventListener("click", () => {
        nav.classList.add("openNav");
        nav.classList.remove("openSearch");
        searchIcon.classList.replace("uil-times", "uil-search");
    });

    navCloseBtn.addEventListener("click", () => {
        nav.classList.remove("openNav");
    });
}
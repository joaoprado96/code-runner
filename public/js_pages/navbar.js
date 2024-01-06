function criarNavbar() {
    var navbarHTML = `
    <nav class="nav">
        <i class="uil uil-bars navOpenBtn"></i>
        <img src="css/icons/logo6.png" alt="Usuário" class="user-icon">
        <a href="#" class="logo">coderunner</a>

        <ul class="nav-links">
            <i class="uil uil-times navCloseBtn"></i>
            <li><a href="/page/home">home</a></li>
            <li><a href="/page/admin">panel</a></li>
            <li><a href="/page/regressiverunner">regressive</a></li>
            <li><a href="/page/versionrunner">version</a></li>

        </ul>

        <i class="uil uil-search search-icon" id="searchIcon"></i>
        <div class="search-box">
            <i class="uil uil-search search-icon"></i>
            <input type="text" placeholder="Search here..." />
        </div>

        <div class="user-icon-container">
            <img src="css/icons/userxx.png" alt="Usuário" class="user-icon">
            <div class="user-submenu">
            <a href="/page/home">...</a>

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
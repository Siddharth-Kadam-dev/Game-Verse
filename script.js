const hamburger = document.querySelector(".hamburger");
const navbar = document.querySelector(".navbar");

hamburger.addEventListener("click", () => {
    navbar.classList.toggle("active");
});

// searching

const searchInput = document.getElementById("searchInput");

searchInput.addEventListener("input", function () {

    const searchText = this.value.toLowerCase();

    const games = document.querySelectorAll(".game-card");

    games.forEach(function (game) {

        const gameName = game.textContent.toLowerCase();

        if (gameName.includes(searchText)) {
            game.style.display = "";
        } else {
            game.style.display = "none";
        }

    });
});
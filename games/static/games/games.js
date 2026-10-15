document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const gameCards = document.querySelectorAll(".game-card");

    searchInput.addEventListener("input", (e) => {
        const value = e.target.value.toLowerCase();

        gameCards.forEach((card) => {
            const name = card.querySelector(".game-name").textContent.toLowerCase();
            const category = card.querySelector(".game-category").textContent.toLowerCase();

            if (name.includes(value) || category.includes(value)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    });
});
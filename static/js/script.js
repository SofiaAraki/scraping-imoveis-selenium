document.getElementById("search-form").addEventListener("submit", async function(e) {
    e.preventDefault();

    const location = document.getElementById("location").value.trim();
    const resultsDiv = document.getElementById("results");

    const response = await fetch(`/api/imoveis`);
    const data = await response.json();

    resultsDiv.innerHTML = "";
    data.forEach(item => {
        resultsDiv.innerHTML += `
            <div>
                <h3>${item.title}</h3>
                <p>Preço: ${item.price}</p>
                <p>Localização: ${item.location}</p>
            </div>
        `;
    });
});

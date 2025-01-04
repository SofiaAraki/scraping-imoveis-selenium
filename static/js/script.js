document.getElementById("search-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const resultsDiv = document.getElementById("results");
    const location = document.getElementById("location").value.trim();

    const baseUrl = "http://localhost:5000";
    let apiUrl = `${baseUrl}/api/imoveis`;

    if (location) {
        apiUrl += `?location=${encodeURIComponent(location)}`;
    }

    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error("Erro ao buscar dados da API");
        }

        const data = await response.json();
        renderResultsDivs(data, resultsDiv);
    } catch (error) {
        resultsDiv.innerHTML = `<p>Erro: ${error.message}</p>`;
    }
});

function renderResultsDivs(items, resultsDiv) {
    resultsDiv.innerHTML = "";
    if (items.length === 0) {
        resultsDiv.innerHTML = "<p>Nenhum imóvel encontrado.</p>";
        return;
    }

    items.forEach((item) => {
        const itemDiv = document.createElement("div");
        itemDiv.innerHTML = `
            <h3>${escapeHTML(item.title)}</h3>
            <p>Preço: ${escapeHTML(item.price)}</p>
            <p>Localização: ${escapeHTML(item.location)}</p>
        `;
        resultsDiv.appendChild(itemDiv);
    });
}

function escapeHTML(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

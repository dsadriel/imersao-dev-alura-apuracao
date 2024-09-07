let data = [];
let currentPage = 1;
const rowsPerPage = 30;
const tableBody = document.querySelector("#results-table tbody");
const pageIndicator = document.getElementById("pageIndicator");

document.addEventListener("DOMContentLoaded", () => {
    fetchCSVData();
});

async function fetchCSVData() {
    try {
        const response = await fetch('apuracao.csv');
        const csvText = await response.text();
        document.getElementById('ultima-atualizacao').innerText = csvText.split('\n')[0].replace('#', '');
        parseCSV(csvText);
        displayPage(1);
    } catch (error) {
        console.error("Erro ao carregar o arquivo CSV:", error);
    }
}

function parseCSV(csvText) {
    const rows = csvText.split('\n').filter(r => !r.startsWith('#') && r.trim() !== '').slice(1); // Remove linhas vazias e comentários
    data = rows.map(row => {
        const [Posição, Votos, Nome, GitHub] = row.split(',');
        return { Posição, Votos, Nome, GitHub };
    });
}

function displayPage(page) {
    tableBody.innerHTML = "";
    const startIndex = (page - 1) * rowsPerPage;
    const endIndex = Math.min(startIndex + rowsPerPage, data.length);

    for (let i = startIndex; i < endIndex; i++) {
        const row = data[i];
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row.Posição}</td>
            <td>${row.Votos}</td>
            <td>${row.Nome}</td>
            <td><a href="${row.GitHub}" target="_blank">${row.GitHub}</a></td>
        `;
        tableBody.appendChild(tr);
    }

    currentPage = page;
    pageIndicator.textContent = `Página ${currentPage}/${Math.ceil(data.length / rowsPerPage)}`;
}

function prevPage() {
    if (currentPage > 1) {
        displayPage(currentPage - 1);
    }
}

function nextPage() {
    if (currentPage * rowsPerPage < data.length) {
        displayPage(currentPage + 1);
    }
}

function searchParticipant() {
    const searchQuery = document.getElementById('search').value.toLowerCase();
    const filteredData = data.filter(row => row.Nome.toLowerCase().includes(searchQuery));

    if (filteredData.length > 0) {
        tableBody.innerHTML = "";
        filteredData.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.Posição}</td>
                <td>${row.Votos}</td>
                <td>${row.Nome}</td>
                <td><a href="${row.GitHub}" target="_blank">${row.GitHub}</a></td>
            `;
            tableBody.appendChild(tr);
        });
        document.querySelector("#pageIndicator").textContent = `Exibindo ${filteredData.length} resultado(s)`;
    } else {
        tableBody.innerHTML = "<tr><td colspan='4'>Nenhum participante encontrado. Tente novamente.</td></tr>";
    }
}

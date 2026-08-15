// Elements
const searchContainer = document.getElementById('search-container');
const searchBox = document.getElementById('search-box');
const searchInput = document.getElementById('search-input');
const resultsList = document.getElementById('results-list');

// Backend API URL
const BACKEND_URL = "/api/search";

// Event Listeners
searchInput.addEventListener('input', handleInput);
searchBox.addEventListener('click', () => searchInput.focus());
document.addEventListener('click', handleClickOutside);

// Function to handle typing in the search bar
async function handleInput(e) {
    const query = e.target.value.trim();

    if (query.length > 0) {
        searchContainer.classList.add('active');

        try {
            const response = await fetch(`${BACKEND_URL}?query=${encodeURIComponent(query)}`);

            if (response.ok) {
                const data = await response.json();
                const backendResults = data.matches || [];
                renderResults(backendResults, query);
            } else {
                console.error("Error from backend");
                renderResults([], query);
            }
        } catch (error) {
            console.error("Connection Error:", error);
            resultsList.innerHTML = `<li><span class="material-symbols-outlined" style="color:red;">error</span> <div class="result-content"><span class="result-text" style="color:#ff6b6b;">Cannot connect to backend. Is FastAPI running?</span></div></li>`;
        }
    } else {
        closeDropdown();
    }
}

// Function to render the filtered results to the DOM
function renderResults(results, query) {
    resultsList.innerHTML = '';

    if (results.length > 0) {
        results.forEach(resultObj => {
            const li = document.createElement('li');

            // Icon
            const icon = document.createElement('span');
            icon.className = 'material-symbols-outlined';
            icon.textContent = resultObj.type === 'history' ? 'history' : 'description';

            // Content Container
            const contentDiv = document.createElement('div');
            contentDiv.className = 'result-content';

            // Title and Score wrapper
            const titleWrap = document.createElement('div');
            titleWrap.className = 'result-title-wrap';

            // Text Title
            const textSpan = document.createElement('span');
            textSpan.className = 'result-text';
            textSpan.textContent = resultObj.title;

            titleWrap.appendChild(textSpan);

            // Score Tag (if document)
            if (resultObj.type === 'document') {
                const scoreSpan = document.createElement('span');
                scoreSpan.className = 'result-score';
                scoreSpan.textContent = `Score: ${resultObj.score}`;
                titleWrap.appendChild(scoreSpan);
            }

            contentDiv.appendChild(titleWrap);

            // Snippet
            if (resultObj.snippet) {
                const snippetSpan = document.createElement('span');
                snippetSpan.className = 'result-snippet';
                snippetSpan.textContent = resultObj.snippet;
                contentDiv.appendChild(snippetSpan);
            }

            li.appendChild(icon);
            li.appendChild(contentDiv);

            // Click to submit
            li.addEventListener('click', () => {
                searchInput.value = resultObj.title;
                closeDropdown();
                fetch(`${BACKEND_URL}?query=${encodeURIComponent(resultObj.title)}&is_submit=true`)
                    .catch(e => console.error("Could not save to history", e));
            });

            resultsList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.innerHTML = `<span class="material-symbols-outlined">search</span> <div class="result-content"><span class="result-text">No results for "${query}"</span></div>`;
        resultsList.appendChild(li);
    }
}

function closeDropdown() {
    searchContainer.classList.remove('active');
}

function handleClickOutside(e) {
    if (!searchContainer.contains(e.target)) {
        closeDropdown();
    }
}

searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const query = searchInput.value.trim();
        if (query) {
            closeDropdown();
            fetch(`${BACKEND_URL}?query=${encodeURIComponent(query)}&is_submit=true`)
                .catch(err => console.error("Error saving history:", err));
        }
    }
});



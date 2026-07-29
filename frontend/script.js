// Elements
const searchContainer = document.getElementById('search-container');
const searchBox = document.getElementById('search-box');
const searchInput = document.getElementById('search-input');
const resultsList = document.getElementById('results-list');

// Backend API URL
const BACKEND_URL = "http://127.0.0.1:8000/search";

// Event Listeners
searchInput.addEventListener('input', handleInput);
searchBox.addEventListener('click', () => searchInput.focus());
document.addEventListener('click', handleClickOutside);

// Function to handle typing in the search bar
async function handleInput(e) {
    const query = e.target.value.trim();
    
    if (query.length > 0) {
        // Show dropdown
        searchContainer.classList.add('active');
        
        try {
            // Fetch results from the FastAPI backend!
            // is_submit defaults to false here because they are just typing
            const response = await fetch(`${BACKEND_URL}?query=${encodeURIComponent(query)}`);
            
            if (response.ok) {
                const data = await response.json();
                // Get the "matches" list that Python returned
                const backendResults = data.matches || [];
                
                // Render the results to the screen
                renderResults(backendResults, query);
            } else {
                console.error("Error from backend");
                renderResults([], query);
            }
        } catch (error) {
            console.error("Connection Error:", error);
            // Show a friendly error if the backend isn't running
            resultsList.innerHTML = `<li><span class="material-symbols-outlined" style="color:red;">error</span> <span class="result-text" style="color:#ff6b6b;">Cannot connect to backend. Is FastAPI running?</span></li>`;
        }
        
    } else {
        // Hide dropdown if input is empty
        closeDropdown();
    }
}

// Function to render the filtered results to the DOM
function renderResults(results, query) {
    resultsList.innerHTML = '';
    
    if (results.length > 0) {
        results.forEach(result => {
            const li = document.createElement('li');
            
            // Icon
            const icon = document.createElement('span');
            icon.className = 'material-symbols-outlined';
            icon.textContent = 'search';
            
            // Text
            const textSpan = document.createElement('span');
            textSpan.className = 'result-text';
            textSpan.textContent = result;
            
            li.appendChild(icon);
            li.appendChild(textSpan);
            
            // Click on a result to fill the search bar and close
            li.addEventListener('click', () => {
                searchInput.value = result;
                closeDropdown();
                
                // When clicking a result, we count that as a "submit" too!
                fetch(`${BACKEND_URL}?query=${encodeURIComponent(result)}&is_submit=true`)
                    .catch(e => console.error("Could not save to history", e));
            });
            
            resultsList.appendChild(li);
        });
    } else {
        // No results found state
        const li = document.createElement('li');
        li.innerHTML = `<span class="material-symbols-outlined">search</span> <span class="result-text">No results for "${query}"</span>`;
        resultsList.appendChild(li);
    }
}

// Function to close the dropdown
function closeDropdown() {
    searchContainer.classList.remove('active');
}

// Close dropdown if clicked outside of the search container
function handleClickOutside(e) {
    if (!searchContainer.contains(e.target)) {
        closeDropdown();
    }
}

// Handle Enter key for search
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const query = searchInput.value.trim();
        if (query) {
            closeDropdown();
            
            // Explicitly tell the backend this is a submission!
            fetch(`${BACKEND_URL}?query=${encodeURIComponent(query)}&is_submit=true`)
                .then(() => console.log("Saved to history:", query))
                .catch(err => console.error("Error saving history:", err));
        }
    }
});

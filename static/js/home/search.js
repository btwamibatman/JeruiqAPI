// search.js
import { showToast } from './utils.js';
import { addLocationToMap, performPhotonSearch } from './map.js'; // Import map search function and addLocationToMap

let searchErrorContainer = null;
let homeSearchListbox = null; // Reference to the suggestions listbox
let debounceTimer; // For debouncing input

function clearSearchError() {
    if (searchErrorContainer) {
        searchErrorContainer.style.display = 'none';
        searchErrorContainer.textContent = '';
    }
}
function displaySearchError(message) {
    if (searchErrorContainer) {
        searchErrorContainer.textContent = message;
        searchErrorContainer.style.display = 'none';
        setTimeout(() => {
            if (searchErrorContainer.textContent === message) {
                searchErrorContainer.style.display = 'none';
                searchErrorContainer.textContent = '';
            }
        }, 5000);
    } else {
        console.warn('Search error message container not found. Error:', message);
    }
}

// Function to fetch suggestions from Photon
async function fetchPhotonSuggestions(query, inputElement, mapInstance) {
    if (query.length < 3) {
        homeSearchListbox.innerHTML = '';
        homeSearchListbox.classList.add('hidden');
        return;
    }

    clearSearchError();

    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
        // Kazakhstan bounding box: minLon, minLat, maxLon, maxLat
        const bbox = [46.50, 40.95, 87.35, 55.95].join(',');
        const url = `https://photon.komoot.io/api/?q=${encodeURIComponent(query)}&lang=en&limit=20&bbox=${bbox}`;

        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            // Photon returns features in data.features
            // Filter by country: Kazakhstan (country code 'KZ')
            const filtered = data.features.filter(f =>
                f.properties.countrycode === 'KZ'
            );
            // Convert to Nominatim-like format for your displaySuggestions
            const suggestions = filtered.map(f => ({
                display_name: f.properties.name + (f.properties.city ? ', ' + f.properties.city : '') + (f.properties.country ? ', ' + f.properties.country : ''),
                lat: f.geometry.coordinates[1],
                lon: f.geometry.coordinates[0],
                type: f.properties.osm_value || '',
                class: f.properties.osm_key || ''
            }));
            displaySuggestions(suggestions, inputElement, mapInstance);
        } catch (error) {
            console.error('Error fetching Photon suggestions:', error);
            displaySearchError('Error fetching search suggestions.');
            homeSearchListbox.classList.add('hidden');
        }
    }, 300);
}

// Function to display suggestions in the listbox
function displaySuggestions(suggestions, inputElement, mapInstance) {
    homeSearchListbox.innerHTML = '';

    if (!suggestions || suggestions.length === 0) {
        homeSearchListbox.classList.add('hidden');
        return;
    }

    // --- CATEGORY FILTER BUTTONS ---
    const categoryTypeMap = {
        city: ['city', 'municipality', 'town', 'locality', 'administrative'],
        nature: ['natural', 'peak', 'mountain', 'lake', 'river', 'forest', 'valley', 'park'],
        village: ['village', 'hamlet', 'suburb'],
        region: ['region', 'state', 'province', 'oblast', 'district', 'area']
    };
    const categories = [
        { key: 'all', label: 'All' },
        { key: 'city', label: 'City' },
        { key: 'nature', label: 'Nature' },
        { key: 'village', label: 'Village' },
        { key: 'region', label: 'Region' }
    ];

    let activeCategory = 'all';

    // Create filter buttons container
    const filterContainer = document.createElement('div');
    filterContainer.className = 'flex gap-2 p-2';

    categories.forEach(cat => {
        const btn = document.createElement('button');
        btn.textContent = cat.label;
        btn.className = 'category-filter px-3 py-1 rounded-full text-base' + (cat.key === 'all' ? ' active-category' : '');
        btn.onclick = () => {
            activeCategory = cat.key;
            filterContainer.querySelectorAll('button').forEach(b => b.classList.remove('active-category'));
            btn.classList.add('active-category');
            renderList();
        };
        filterContainer.appendChild(btn);
    });

    homeSearchListbox.appendChild(filterContainer);

    // --- SUGGESTIONS LIST ---
    const listContainer = document.createElement('div');
    homeSearchListbox.appendChild(listContainer);

    function renderList() {
        listContainer.innerHTML = '';
        let filtered = suggestions;

        // Filter by category
        if (activeCategory !== 'all') {
            const types = categoryTypeMap[activeCategory] || [];
            filtered = suggestions.filter(place => {
                const type = (place.type || '').toLowerCase();
                const className = (place.class || '').toLowerCase();
                // Match if type or class matches any in the category's type list
                return types.some(t =>
                    type.includes(t) ||
                    className.includes(t)
                );
            });
        }

        // Filter by input value (partial match, case-insensitive)
        const query = inputElement.value.trim().toLowerCase();
        if (query.length > 0) {
            filtered = filtered.filter(place =>
                place.display_name && place.display_name.toLowerCase().includes(query)
            );
        }

        filtered.forEach(place => {
            const item = document.createElement('div');
            item.classList.add('home-search-listbox-option', 'p-1', 'cursor-pointer', 'hover:bg-[var(--bg-medium-dark)]', 'text-white', 'text-sm', 'flex', 'flex-col');
            const [main, ...secondaryParts] = place.display_name.split(',');
            const secondary = secondaryParts.join(',').trim();
            const mainSpan = document.createElement('span');
            mainSpan.textContent = main.trim();
            mainSpan.style.fontWeight = '600';
            mainSpan.style.fontSize = '1rem';
            const secondarySpan = document.createElement('span');
            secondarySpan.textContent = secondary;
            secondarySpan.classList.add('address-secondary-line');
            item.appendChild(mainSpan);
            if (secondary) item.appendChild(secondarySpan);
            item.dataset.lat = place.lat;
            item.dataset.lon = place.lon;
            item.dataset.name = place.display_name;
            item.addEventListener('click', () => {
                inputElement.value = place.display_name;
                homeSearchListbox.classList.add('hidden');
                addLocationToMap(mapInstance, parseFloat(place.lat), parseFloat(place.lon), place.display_name);
                clearSearchError();
            });
            listContainer.appendChild(item);
        });
        // If no results for category
        if (filtered.length === 0) {
            listContainer.innerHTML = '<div class="text-gray-400 text-base p-2">No results for this category.</div>';
        }
    }

    renderList();
    homeSearchListbox.classList.remove('hidden');
}

// Function to show sidebar of results 
function showSearchSidebar(results) {
    // Create or select a sidebar element inside main-content
    let sidebar = document.getElementById('search-sidebar');
    if (!sidebar) {
        sidebar = document.createElement('div');
        sidebar.id = 'search-sidebar';
        sidebar.className = 'absolute top-0 right-0 w-96 h-full bg-[var(--bg-dark)] z-50 p-6 overflow-y-auto shadow-lg';
        document.getElementById('main-content').appendChild(sidebar);
    }
    sidebar.innerHTML = `
        <h3 class="text-xl font-bold mb-4 mt-2">Search Results</h3>
        <button id="close-search-sidebar" class="mb-4 mt-2" style="
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: transparent;
            color: #fff;
            font-size: 1.5rem;
            border: none;
            cursor: pointer;
            z-index: 10;
        " aria-label="Close sidebar">&times;</button>
    `;
    results.forEach(place => {
        sidebar.innerHTML += `
            <div class="mb-4 p-4 bg-[var(--bg-medium-dark)] rounded-lg">
                <div class="font-semibold text-white">${place.display_name}</div>
                <button class="mt-2 text-[var(--accent-color)] underline" onclick="window.map.flyTo([${place.lat}, ${place.lon}], 13)">Show on Map</button>
            </div>
        `;
    });
    sidebar.style.display = 'block';

    // Add close functionality
    document.getElementById('close-search-sidebar').onclick = () => {
        sidebar.style.display = 'none';
    };
}

export function setupSearch(searchInput, searchButton, mapInstance) {
    searchErrorContainer = document.getElementById('search-error-message');
    homeSearchListbox = document.getElementById('home-search-listbox'); // Initialize listbox reference
    const homeSearchContainer = document.querySelector('.home-search-container');

    if (searchInput && searchButton && mapInstance && homeSearchListbox && searchErrorContainer) {
        // Event listener for real-time suggestions as user types
        searchInput.addEventListener('input', () => {
            const query = searchInput.value.trim();
            fetchPhotonSuggestions(query, searchInput, mapInstance);
        });

        searchButton.addEventListener('click', async (event) => {
            event.preventDefault();

            // Get the computed width of the input
            const inputWidth = window.getComputedStyle(searchInput).width;
            // Set your threshold for "fully open" (e.g., 200px or more)
            if (parseFloat(inputWidth) < 150) { // Adjust 150 to your minimum "open" width
                // Optionally, focus the input or trigger the open animation here
                searchInput.focus();
                return;
            }

            clearSearchError();
            homeSearchListbox.classList.add('hidden');

            const query = searchInput.value;
            if (!query) {
                displaySearchError('Please enter a location to search.');
                return;
            }
            // Fetch multiple results for sidebar
            // Kazakhstan bounding box: minLon, minLat, maxLon, maxLat
            const bbox = [46.50, 40.95, 87.35, 55.95].join(',');
            const url = `https://photon.komoot.io/api/?q=${encodeURIComponent(query)}&lang=en&limit=20&bbox=${bbox}`;
            try {
                const response = await fetch(url);
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                const data = await response.json();
                // Photon returns features in data.features
                // Filter by country: Kazakhstan (country code 'KZ')
                const filtered = data.features.filter(f =>
                    f.properties.countrycode === 'KZ'
                );
                // Convert to Nominatim-like format for your displaySuggestions
                const suggestions = filtered.map(f => ({
                    display_name: f.properties.name + (f.properties.city ? ', ' + f.properties.city : '') + (f.properties.country ? ', ' + f.properties.country : ''),
                    lat: f.geometry.coordinates[1],
                    lon: f.geometry.coordinates[0],
                    type: f.properties.osm_value || '',
                    class: f.properties.osm_key || ''
                }));
                displaySuggestions(suggestions, inputElement, mapInstance);
            } catch (error) {
                console.error('Error fetching Photon suggestions:', error);
                displaySearchError('Error fetching search suggestions.');
                homeSearchListbox.classList.add('hidden');
            }
        });

        searchInput.addEventListener('keypress', async (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                clearSearchError();
                homeSearchListbox.classList.add('hidden'); // Hide suggestions on explicit search

                const query = searchInput.value;
                if (!query) {
                    displaySearchError('Please enter a location to search.');
                    return;
                }
                // Fetch multiple results for sidebar (same as search button)
                const bbox = [46.50, 40.95, 87.35, 55.95].join(',');
                const url = `https://photon.komoot.io/api/?q=${encodeURIComponent(query)}&lang=en&limit=20&bbox=${bbox}`;
                try {
                    const response = await fetch(url);
                    const data = await response.json();
                    if (data && data.length > 0) {
                        showSearchSidebar(data);
                    } else {
                        displaySearchError(`No results found for "${query}".`);
                    }
                } catch (e) {
                    displaySearchError('Error fetching search results.');
                }
            }
        });

        // Clear error message when user starts typing again
        searchInput.addEventListener('input', clearSearchError);

        // Hide suggestions when clicking outside the search container
        document.addEventListener('click', (event) => {
            if (homeSearchContainer && !homeSearchContainer.contains(event.target)) {
                homeSearchListbox.classList.add('hidden');
            }
        });

    } else {
        console.warn('Search input, button, or map instance not found. Nominatim search will not be fully initialized.');
    }
}
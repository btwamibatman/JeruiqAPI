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
        searchErrorContainer.style.display = 'block'; // Changed to block to make it visible
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
// This function will now pass the raw Photon features array
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
            const filteredFeatures = data.features.filter(f =>
                f.properties && f.properties.countrycode === 'KZ' // Added check for properties
            );
            // Pass the filtered features array directly to displaySuggestions
            displaySuggestions(filteredFeatures, inputElement, mapInstance);
        } catch (error) {
            console.error('Error fetching Photon suggestions:', error);
            displaySearchError('Error fetching search suggestions.');
            homeSearchListbox.classList.add('hidden');
        }
    }, 300);
}

// Function to display suggestions in the listbox
// This function now accepts an array of Photon Feature objects
function displaySuggestions(features, inputElement, mapInstance) {
    homeSearchListbox.innerHTML = '';

    if (!features || features.length === 0) {
        homeSearchListbox.classList.add('hidden');
        return;
    }

    // --- CATEGORY FILTER BUTTONS ---
    const categoryTypeMap = {
        city: ['city', 'municipality', 'town', 'locality', 'administrative'],
        nature: ['natural', 'peak', 'mountain', 'lake', 'river', 'forest', 'valley', 'park'],
        village: ['village', 'hamlet', 'suburb'],
        region: ['region', 'state', 'province', 'oblast', 'district', 'area'],
        // Add more categories if needed, mapping to osm_key or osm_value
        // e.g., 'poi': ['hotel', 'restaurant', 'cafe', 'shop']
    };
    const categories = [
        { key: 'all', label: 'All' },
        { key: 'city', label: 'City' },
        { key: 'nature', label: 'Nature' },
        { key: 'village', label: 'Village' },
        { key: 'region', label: 'Region' }
        // Add buttons for new categories here
    ];

    let activeCategory = 'all';

    // Create filter buttons container
    const filterContainer = document.createElement('div');
    filterContainer.className = 'flex gap-2 p-2 overflow-x-auto'; // Added overflow for many buttons

    categories.forEach(cat => {
        const btn = document.createElement('button');
        btn.textContent = cat.label;
        btn.className = 'category-filter px-3 py-1 rounded-full text-base whitespace-nowrap' + (cat.key === 'all' ? ' active-category' : ''); // Added whitespace-nowrap
        btn.onclick = () => {
            activeCategory = cat.key;
            filterContainer.querySelectorAll('button').forEach(b => b.classList.remove('active-category'));
            btn.classList.add('active-category');
            renderList(features); // Pass the original features to renderList
        };
        filterContainer.appendChild(btn);
    });

    homeSearchListbox.appendChild(filterContainer);

    // --- SUGGESTIONS LIST ---
    const listContainer = document.createElement('div');
    listContainer.className = 'suggestions-list-container'; // Add a class for potential styling
    homeSearchListbox.appendChild(listContainer);

    // renderList now takes the full features array and filters internally
    function renderList(allFeatures) {
        listContainer.innerHTML = '';
        let filtered = allFeatures;

        // Filter by category
        if (activeCategory !== 'all') {
            const types = categoryTypeMap[activeCategory] || [];
            filtered = allFeatures.filter(feature => {
                const properties = feature.properties || {}; // Ensure properties exist
                const type = (properties.osm_value || '').toLowerCase();
                const className = (properties.osm_key || '').toLowerCase();
                // Match if type or class matches any in the category's type list
                return types.some(t =>
                    type.includes(t) ||
                    className.includes(t)
                );
            });
        }

        // Filter by input value (partial match, case-insensitive)
        // This filter is applied AFTER category filter
        const query = inputElement.value.trim().toLowerCase();
        if (query.length > 0) {
             filtered = filtered.filter(feature => {
                 const properties = feature.properties || {};
                 // Construct a display name similar to the original logic for filtering
                 const displayName = (properties.name || '') + (properties.city ? ', ' + properties.city : '') + (properties.country ? ', ' + properties.country : '');
                 return displayName.toLowerCase().includes(query);
             });
        }


        // Render the filtered features
        filtered.forEach(feature => {
            const properties = feature.properties;
            const geometry = feature.geometry;

            if (!properties || !geometry || !geometry.coordinates) {
                 console.warn("Skipping invalid feature:", feature);
                 return; // Skip features without properties or coordinates
            }

            const lat = geometry.coordinates[1];
            const lon = geometry.coordinates[0];
            // Construct display name from properties
            const displayName = (properties.name || '') + (properties.city ? ', ' + properties.city : '') + (properties.country ? ', ' + properties.country : '');


            const item = document.createElement('div');
            item.classList.add('home-search-listbox-option', 'p-1', 'cursor-pointer', 'hover:bg-[var(--bg-medium-dark)]', 'text-white', 'text-sm', 'flex', 'flex-col');

            // Split the constructed display name for main/secondary lines
            const [main, ...secondaryParts] = displayName.split(',');
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

            // Store lat/lon/name on the item using data attributes
            item.dataset.lat = lat;
            item.dataset.lon = lon;
            item.dataset.name = displayName; // Store the full display name

            item.addEventListener('click', () => {
                // Use the stored data attributes
                const selectedLat = parseFloat(item.dataset.lat);
                const selectedLon = parseFloat(item.dataset.lon);
                const selectedName = item.dataset.name;

                inputElement.value = selectedName; // Set input value to the full name
                homeSearchListbox.classList.add('hidden');
                addLocationToMap(mapInstance, selectedLat, selectedLon, selectedName);
                clearSearchError();
            });
            listContainer.appendChild(item);
        });

        // If no results for the current filter
        if (filtered.length === 0) {
            listContainer.innerHTML = '<div class="text-gray-400 text-base p-2">No results for this filter.</div>';
        }
    }

    // Initial render with all features
    renderList(features);
    homeSearchListbox.classList.remove('hidden');
}

// Function to show sidebar of results
// This function now accepts an array of Photon Feature objects
function showSearchSidebar(features) {
    // Create or select a sidebar element inside main-content
    let sidebar = document.getElementById('search-sidebar');
    if (!sidebar) {
        sidebar = document.createElement('div');
        sidebar.id = 'search-sidebar';
        sidebar.className = 'absolute top-0 right-0 w-96 h-full bg-[var(--bg-dark)] z-50 p-6 overflow-y-auto shadow-lg';
        // Assuming 'main-content' is the container for your map and sidebar
        const mainContent = document.getElementById('main-content');
        if (mainContent) {
             mainContent.appendChild(sidebar);
        } else {
             console.error("Could not find 'main-content' element to attach sidebar.");
             return; // Exit if main-content is not found
        }
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

    if (!features || features.length === 0) {
         sidebar.innerHTML += '<div class="text-gray-400 text-base p-2">No results found.</div>';
    } else {
        features.forEach(feature => {
            const properties = feature.properties;
            const geometry = feature.geometry;

            if (!properties || !geometry || !geometry.coordinates) {
                 console.warn("Skipping invalid feature for sidebar:", feature);
                 return; // Skip invalid features
            }

            const lat = geometry.coordinates[1];
            const lon = geometry.coordinates[0];
            // Construct display name
            const displayName = (properties.name || '') + (properties.city ? ', ' + properties.city : '') + (properties.country ? ', ' + properties.country : '');

            sidebar.innerHTML += `
                <div class="mb-4 p-4 bg-[var(--bg-medium-dark)] rounded-lg">
                    <div class="font-semibold text-white">${displayName}</div>
                    <button class="mt-2 text-[var(--accent-color)] underline" onclick="window.map.flyTo([${lat}, ${lon}], 13)">Show on Map</button>
                </div>
            `;
        });
    }

    sidebar.style.display = 'block';

    // Add close functionality
    const closeButton = document.getElementById('close-search-sidebar');
    if (closeButton) {
        closeButton.onclick = () => {
            sidebar.style.display = 'none';
        };
    }
}


export function setupSearch(searchInput, searchButton, mapInstance) {
    searchErrorContainer = document.getElementById('search-error-message');
    homeSearchListbox = document.getElementById('home-search-listbox'); // Initialize listbox reference
    const homeSearchContainer = document.querySelector('.home-search-container');

    if (searchInput && searchButton && mapInstance && homeSearchListbox && searchErrorContainer) {
        // Event listener for real-time suggestions as user types
        searchInput.addEventListener('input', () => {
            const query = searchInput.value.trim();
            fetchPhotonSuggestions(query, searchInput, mapInstance); // fetchPhotonSuggestions now passes features
        });

        // Event listener for the search button click
        searchButton.addEventListener('click', async (event) => {
            event.preventDefault();

            // Get the computed width of the input
            const inputWidth = window.getComputedStyle(searchInput).width;
            // Set your threshold for "fully open" (e.g., 150px or more)
            if (parseFloat(inputWidth) < 150) { // Adjust 150 to your minimum "open" width
                // Optionally, focus the input or trigger the open animation here
                searchInput.focus();
                return;
            }

            clearSearchError();
            homeSearchListbox.classList.add('hidden'); // Hide suggestions

            const query = searchInput.value.trim(); // Use trim()
            if (!query) {
                displaySearchError('Please enter a location to search.');
                return;
            }

            // Fetch multiple results for sidebar (same logic as suggestions, but for sidebar)
            const bbox = [46.50, 40.95, 87.35, 55.95].join(',');
            const url = `https://photon.komoot.io/api/?q=${encodeURIComponent(query)}&lang=en&limit=20&bbox=${bbox}`;
            try {
                const response = await fetch(url);
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                const data = await response.json();
                // Photon returns features in data.features
                // Filter by country: Kazakhstan (country code 'KZ')
                const filteredFeatures = data.features.filter(f =>
                    f.properties && f.properties.countrycode === 'KZ' // Added check for properties
                );

                // Pass the filtered features array to showSearchSidebar
                showSearchSidebar(filteredFeatures);

            } catch (error) {
                console.error('Error fetching Photon search results:', error);
                displaySearchError('Error fetching search results.');
            }
        });

        // Event listener for Enter keypress in the search input
        searchInput.addEventListener('keypress', async (event) => {
            if (event.key === 'Enter') {
                event.preventDefault(); // Prevent default form submission

                clearSearchError();
                homeSearchListbox.classList.add('hidden'); // Hide suggestions on explicit search

                const query = searchInput.value.trim(); // Use trim()
                if (!query) {
                    displaySearchError('Please enter a location to search.');
                    return;
                }

                // Fetch multiple results for sidebar (same logic as search button)
                const bbox = [46.50, 40.95, 87.35, 55.95].join(',');
                const url = `https://photon.komoot.io/api/?q=${encodeURIComponent(query)}&lang=en&limit=20&bbox=${bbox}`;
                try {
                    const response = await fetch(url);
                    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                    const data = await response.json();
                     // Photon returns features in data.features
                    // Filter by country: Kazakhstan (country code 'KZ')
                    const filteredFeatures = data.features.filter(f =>
                        f.properties && f.properties.countrycode === 'KZ' // Added check for properties
                    );

                    // Pass the filtered features array to showSearchSidebar
                    if (filteredFeatures && filteredFeatures.length > 0) {
                        showSearchSidebar(filteredFeatures);
                    } else {
                        displaySearchError(`No results found for "${query}".`);
                    }

                } catch (error) { // Changed 'e' to 'error' for consistency
                    console.error('Error fetching Photon search results:', error);
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

        // Optional: Hide suggestions when input loses focus, unless clicking on listbox
        searchInput.addEventListener('blur', () => {
             // Add a small delay to allow click event on listbox items to register
             setTimeout(() => {
                 if (homeSearchListbox && !homeSearchListbox.contains(document.activeElement)) {
                      homeSearchListbox.classList.add('hidden');
                 }
             }, 100); // Adjust delay as needed
        });
        // Optional: Show suggestions again when input gains focus if there's text
        searchInput.addEventListener('focus', () => {
             if (searchInput.value.trim().length >= 3 && homeSearchListbox.innerHTML.trim() !== '') {
                  homeSearchListbox.classList.remove('hidden');
             }
        });


    } else {
        console.warn('Search input, button, map instance, listbox, or error container not found. Search will not be fully initialized.');
    }
}
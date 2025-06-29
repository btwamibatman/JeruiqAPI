// home.js - Main Orchestrator
import { setupSearch } from './search.js';
import { loadBookmarks } from './bookmarks.js';
import { setupExploreFilteringAndSearch, updateAllExploreCardBookmarkStates } from './explore.js';
import { clearMarkers } from './map.js';
import { processAiQuery } from './ai.js';

document.addEventListener('DOMContentLoaded', async () => {
    // --- Function to check login status and redirect if not logged in
    function checkLoginStatusAndRedirect() {
        const token = localStorage.getItem('jwt_token'); // Check for the JWT token

        if (!token) {
            // If no token is found, the user is not logged in
            console.log('No JWT token found. Redirecting to login page.');
            // Redirect to the login/registration page (assuming it's at the root '/')
            window.location.href = '/login';
        } else {
            console.log('JWT token found. User is logged in.');
            // User is logged in, allow them to stay on the page.
            // You might want to perform other actions here, like fetching user data
            // or initializing authenticated parts of the page.
        }
    }
    checkLoginStatusAndRedirect();

    // --- Global DOM Elements ---
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggle-btn');
    const mainContent = document.getElementById('main-content');
    const sidebarTexts = document.querySelectorAll('.sidebar-text');
    const mapContainer = document.getElementById('mapContainer');

    const openProfileBtn = document.getElementById('open-profile-btn');
    const profilePicture = document.getElementById('profile-picture');
    const accountSidePanel = document.getElementById('account-side-panel');
    const profileBtn = document.getElementById('profile-btn')
    const settingsBtn = document.getElementById('settings-btn')
    const logoutBtn = document.getElementById('logout-btn')

    const profileNameElement = document.getElementById('profile-name');
    const profileEmailElement = document.getElementById('profile-email');

    const homeSearchInput = document.getElementById('home-search-input');
    const homeSearchButton = document.getElementById('home-search-button');
    const homeSearchContainer = document.querySelector('.home-search-container')
    const homeAiContainer = document.querySelector('.home-ai-container');
    const homeAiInput = document.getElementById('home-ai-input');
    const homeAiButton = document.getElementById('home-ai-button');

    const exploreGrid = document.getElementById('explore-grid');
    const exploreSearchInput = document.getElementById('explore-search-input');
    const exploreSearchButton = document.getElementById('explore-search-button');
    const categoryFiltersContainer = document.getElementById('explore-categories');


    // --- Error Checking for Core Elements ---
    if (!sidebar || !toggleBtn || !mapContainer || !homeSearchInput || !homeSearchButton || !homeAiContainer || !homeAiInput || !homeAiButton) {
        console.error('Error: One or more core UI elements not found. Ensure all required IDs/classes exist in HTML.');
        return;
    }

    // --- Sidebar Toggle Script ---
    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('w-16');
        sidebar.classList.toggle('w-64');
        sidebarTexts.forEach(text => {
            text.classList.toggle('hidden');
            if (!sidebar.classList.contains('w-64')) {
                text.classList.add('hidden');
            } else {
                setTimeout(() => {
                    if (sidebar.classList.contains('w-64')) {
                        text.classList.remove('hidden');
                    }
                });
            }
        });
        mainContent.classList.toggle('ml-16');
        mainContent.classList.toggle('ml-64');

        if (window.map) {
             mainContent.addEventListener('transitionend', function handler(event) {
                if (event.propertyName === 'margin-left') {
                    window.map.invalidateSize();
                    mainContent.removeEventListener('transitionend', handler);
                }
            });
        }
    });

    // --- Unified Tab Switching Logic ---
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();

            // Remove active from all buttons and hide all contents
            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(tc => tc.style.display = 'none');

            // Activate clicked button and show corresponding content
            this.classList.add('active');

            // Show the corresponding section
            const tabId = this.getAttribute('data-tab');
            const tabContent = document.getElementById(tabId);
            if (tabContent) {
                tabContent.classList.add('active');
                tabContent.style.display = 'block';
            }

            // Optional: Call extra logic for certain tabs
            if (tabId === 'bookmarks') {
                loadBookmarks(window.map);
            } else if (tabId === 'explore') {
                updateAllExploreCardBookmarkStates(window.map);
            } else if (tabId === 'home') {
                setTimeout(() => {
                    if (window.map) window.map.invalidateSize();
                    clearMarkers(window.map);
                }, 50);
            }
        });
    });

    // Activate the first tab by default
    if (tabButtons.length > 0) tabButtons[0].click();

    // --- Function to fetch and display user profile data ---
    async function fetchAndDisplayUserProfile() {
        const token = localStorage.getItem('jwt_token');
        if (!token) {
            console.error('No JWT token found for profile fetch.');
            return;
        }

        try {
            const response = await fetch('/api/profile', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`, // Include the token in the Authorization header
                    'Content-Type': 'application/json'
                }
            });

            if (response.status === 401) {
                console.error('Profile fetch failed: Unauthorized. Token might be expired or invalid.');
                localStorage.removeItem('jwt_token'); // Remove invalid token
                window.location.href = '/login'; // Redirect to login
                return;
            }

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.message || response.statusText}`);
            }

            const userData = await response.json();
            console.log('User profile data fetched:', userData);

            // Update the profile info elements within the openProfileBtn
            // We already got references to these elements at the top
            if (profileNameElement) {
                profileNameElement.textContent = `${userData.name} ${userData.surname}`;
            }
            if (profileEmailElement) {
                profileEmailElement.textContent = userData.email;
            }
            if (profilePicture && userData.profile_picture) {
                profilePicture.src = `/static/${userData.profile_picture}?t=${Date.now()}`;
            }

        } catch (error) {
            console.error('Error fetching user profile:', error);
            // Optionally update the profile elements to show an error state
            if (profileNameElement) profileNameElement.textContent = 'Error';
            if (profileEmailElement) profileEmailElement.textContent = 'Failed to load';
        }
    }
    // Call the function here so the profile info is loaded when the page loads
    fetchAndDisplayUserProfile();

    // --- Account Side Panel Toggle Functionality ---
    // Initial state
    accountSidePanel.style.display = 'none';
    accountSidePanel.style.opacity = '0';

    openProfileBtn.addEventListener('click', (event) => {
        // Prevent the click from immediately propagating to the document listener
        event.stopPropagation();
        if (accountSidePanel.style.display === 'none' && accountSidePanel.style.opacity === '0') {
            accountSidePanel.style.display = 'flex';
            accountSidePanel.style.opacity = '1'
        } else {
            accountSidePanel.style.display = 'none';
            accountSidePanel.style.opacity = '0'
        }
    });

    // --- Close Account Side Panel on Outside Click ---
    document.addEventListener('click', (event) => {
        // Check if the account side panel is currently visible
        if (accountSidePanel.style.display !== 'none') {
            const isClickInsidePanel = accountSidePanel.contains(event.target);
            const isClickOnOpenButton = openProfileBtn.contains(event.target); // Check if click is on the button or its children

            // If the click is NOT inside the panel AND NOT on the open button
            if (!isClickInsidePanel && !isClickOnOpenButton) {
                console.log('Clicked outside account panel. Closing panel.');
                accountSidePanel.style.display = 'none';
                accountSidePanel.style.opacity = '0';
            }
        }
    });

    // Logout Button Functionality ---
    if (logoutBtn) { // Check if the logout button element was found
        logoutBtn.addEventListener('click', () => {
            console.log('Logout button clicked. Removing token and redirecting.');
            localStorage.removeItem('jwt_token'); // Remove the token from localStorage
            window.location.href = '/'; // Redirect to the starting page
        });
    }
    // Profile Button Functionality
    if (profileBtn) {
        profileBtn.addEventListener('click', () => {
            window.location.href = '/profile'
        });
    }

    // --- Leaflet Map Initialization ---
    // Define a global 'map' variable. This will be passed to other modules as needed.
    window.map = L.map('mapContainer', {
        zoomControl: false,
        attributionControl: false,
        maxBounds: [
            [40.95, 46.50], // South-West coordinates (Lat, Lng)
            [55.95, 87.35]  // North-East coordinates (Lat, Lng)
        ],
        minZoom: 5.3,
    }).setView([51.1294, 71.4491], 12);

    L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(window.map);

    // Initial map resize
    if (mapContainer) {
        setTimeout(() => {
            window.map.invalidateSize();
        }, 100);
    }

    // --- Function to load and style GeoJSON borders ---
    async function loadGeoJsonBorders(mapInstance) {
        try {
            // Fetch country border GeoJSON
            const countryResponse = await fetch('/static/geojson/kazakhstan_border.geojson');
            if (!countryResponse.ok) throw new Error(`HTTP error! status: ${countryResponse.status}`);
            const countryData = await countryResponse.json();

            // Add country border to map with styling
            L.geoJSON(countryData, {
                style: function(feature) {
                    return {
                        color: '#00FFFF', // Cyan color
                        weight: 3,        // Thicker line
                        opacity: 0,
                        fillOpacity: 0 // No fill
                    };
                }
            }).addTo(mapInstance);
            console.log('Kazakhstan country border loaded.');

            // Fetch regional borders GeoJSON
            const regionsResponse = await fetch('/static/geojson/kazakhstan_regions.geojson');
            if (!regionsResponse.ok) throw new Error(`HTTP error! status: ${regionsResponse.status}`);
            const regionsData = await regionsResponse.json();

            // Add regional borders to map with styling
            L.geoJSON(regionsData, {
                style: function(feature) {
                    return {
                        color: '#00FFFF', // Cyan color for regional borders
                        weight: 0.2,        // Thinner line
                        opacity: 0.6,
                        fillOpacity: 0 // No fill
                    };
                }
            }).addTo(mapInstance);
            console.log('Kazakhstan regional borders loaded.');

            // Fetch district borders GeoJSON
            const districtResponse = await fetch('/static/geojson/kazakhstan_districts.geojson');
            if (!districtResponse.ok) throw new Error(`HTTP error! status: ${districtResponse.status}`);
            const districtData = await districtResponse.json();

            // Add district borders to map with styling
            L.geoJSON(districtData, {
                style: function(feature) {
                    return {
                        color: '#00FFFF', // Cyan color 
                        weight: 0.2,        // Thinner line
                        opacity: 0.6,
                        fillOpacity: 0 // No fill
                    };
                }
            }).addTo(mapInstance);
            console.log('Kazakhstan district borders loaded.');

        } catch (error) {
            console.error('Error loading GeoJSON borders:', error);
            // Optionally display an error message to the user
        }
    }
    // Call the function to load borders after map initialization ---
    loadGeoJsonBorders(window.map);

    // --- Home Tab Search/AI Input Toggle ---
    homeSearchButton.addEventListener('click', () => {
        homeSearchContainer.style.width = "calc(100% - 3rem)";
        homeSearchInput.style.width = "100%";
        homeSearchInput.classList.remove('w-0')
        homeSearchInput.classList.add('pl-2', 'pr-5', 'w-full');

        homeAiContainer.style.width = "3rem";
        homeAiInput.style.width = "0";
        homeAiInput.classList.remove('pl-5', 'pr-5', 'w-full');
        homeAiInput.classList.add('w-0')
    });
    homeAiButton.addEventListener('click', () => {
        homeSearchContainer.style.width = "3rem";
        homeSearchInput.style.width = "0";
        homeSearchInput.classList.remove('pl-2', 'pr-5', 'w-full');
        homeSearchInput.classList.add('w-0')

        homeAiContainer.style.width = "calc(100% - 3rem)";
        homeAiInput.style.width = "100%";
        homeAiInput.classList.add('pl-5', 'pr-5', 'w-full');
        homeAiInput.classList.remove('w-0')

        // Only process AI query if input is fully extended
        const aiInputWidth = window.getComputedStyle(homeAiInput).width;
        if (parseFloat(aiInputWidth) > 150) {
            const query = homeAiInput.value.trim();
            if (query) {
                processAiQuery(query, window.map);
            }
        }
    });
    homeAiInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            // Only process AI query if input is fully extended
            const aiInputWidth = window.getComputedStyle(homeAiInput).width;
            if (parseFloat(aiInputWidth) > 150) {
                const query = homeAiInput.value.trim();
                if (query) {
                    processAiQuery(query, window.map);
                }
            }
        }
    });

    // --- Module Setups ---
    setupSearch(homeSearchInput, homeSearchButton, window.map);
    setupExploreFilteringAndSearch(exploreGrid, exploreSearchInput, exploreSearchButton, categoryFiltersContainer, window.map);

    console.log('Document loaded and global scripts executed successfully.');
});
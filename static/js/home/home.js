// home.js - Main Orchestrator
import { setupSearch } from './search.js';
import { loadBookmarks } from './bookmarks.js';
import { setupExploreFilteringAndSearch, updateAllExploreCardBookmarkStates } from './explore.js';
import { clearMarkers } from './map.js'; // To clear search marker when switching tabs

document.addEventListener('DOMContentLoaded', async () => {
    // Function to check login status and redirect if not logged in
    function checkLoginStatusAndRedirect() {
        const token = localStorage.getItem('jwt_token'); // Check for the JWT token

        if (!token) {
            // If no token is found, the user is not logged in
            console.log('No JWT token found. Redirecting to login page.');
            // Redirect to the login/registration page (assuming it's at the root '/')
            window.location.href = '/';
        } else {
            console.log('JWT token found. User is logged in.');
            // User is logged in, allow them to stay on the page.
            // You might want to perform other actions here, like fetching user data
            // or initializing authenticated parts of the page.
        }
    }

    // Run the check when the DOM is fully loaded
    checkLoginStatusAndRedirect();

    // --- Global DOM Elements ---
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggle-btn');
    const mainContent = document.getElementById('main-content');
    const sidebarTexts = document.querySelectorAll('.sidebar-text');
    const mapContainer = document.getElementById('mapContainer');

    const homeSearchInput = document.getElementById('home-search-input');
    const homeSearchButton = document.getElementById('home-search-button');
    const homeSearchContainer = document.querySelector('.home-search-container')
    const homeAiContainer = document.querySelector('.home-ai-container');
    const homeAiInput = document.getElementById('home-ai-input');
    const homeAiButton = document.getElementById('home-ai-button');

    const openProfileBtn = document.getElementById('open-profile-btn');
    const accountSidePanel = document.getElementById('account-side-panel');
    const logoutBtn = document.getElementById('logout-btn')

    const exploreGrid = document.getElementById('explore-grid');
    const exploreSearchInput = document.getElementById('explore-search-input');
    const exploreSearchButton = document.getElementById('explore-search-button');
    const categoryFiltersContainer = document.getElementById('explore-categories');


    // --- Error Checking for Core Elements ---
    if (!sidebar || !toggleBtn || !mapContainer || !homeSearchInput || !homeSearchButton || !homeAiContainer || !homeAiInput || !homeAiButton) {
        console.error('Error: One or more core UI elements not found. Ensure all required IDs/classes exist in HTML.');
        return;
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

    // --- Call the function to load borders after map initialization ---
    loadGeoJsonBorders(window.map);

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

    // --- Tab Switching Logic ---
    function openTab(evt, tabName) {
        document.querySelectorAll(".tabcontent").forEach(content => content.style.display = "none");
        document.querySelectorAll(".tablinks").forEach(link => link.classList.remove("active"));

        const activeTabContent = document.getElementById(tabName);
        if (activeTabContent) {
            activeTabContent.style.display = "flex";
        } else {
            console.error(`Tab content with id "${tabName}" not found.`);
        }

        if (evt) {
            evt.currentTarget.classList.add("active");
        }

        if (tabName === 'bookmarks') {
            loadBookmarks(window.map); // Pass map instance
        } else if (tabName === 'explore') {
            updateAllExploreCardBookmarkStates(window.map); // Pass map instance
        } else if (tabName === 'home') {
            setTimeout(() => {
                if (window.map) window.map.invalidateSize();
                clearMarkers(window.map); // Clear any search markers when going back to home
            }, 50);
        }
        console.log(`Tab switched to: ${tabName}`);
    }

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

    // --- Logout Button Functionality ---
    if (logoutBtn) { // Check if the logout button element was found
        logoutBtn.addEventListener('click', () => {
            console.log('Logout button clicked. Removing token and redirecting.');
            localStorage.removeItem('jwt_token'); // Remove the token from localStorage
            window.location.href = '/'; // Redirect to the starting page
        });
    } else {
        console.warn('Logout button element not found (#logout-btn). Logout functionality will not work.');
    }

    // Attach event listeners to tab buttons
    document.getElementById('tab-home').addEventListener('click', (e) => openTab(e, 'home'));
    document.getElementById('tab-explore').addEventListener('click', (e) => openTab(e, 'explore'));
    document.getElementById('tab-services').addEventListener('click', (e) => openTab(e, 'services'));
    document.getElementById('tab-chats').addEventListener('click', (e) => openTab(e, 'chats'));
    document.getElementById('tab-bookmarks').addEventListener('click', (e) => openTab(e, 'bookmarks'));

    // Set the default open tab on page load
    document.getElementById("tab-home").click();

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
    });

    // --- Module Setups ---
    setupSearch(homeSearchInput, homeSearchButton, window.map);
    setupExploreFilteringAndSearch(exploreGrid, exploreSearchInput, exploreSearchButton, categoryFiltersContainer, window.map);

    console.log('Document loaded and global scripts executed successfully.');
});
// home.js - Main Orchestrator
import { setupSearch } from './search.js';
import { loadBookmarks } from './bookmarks.js';
import { setupExploreFilteringAndSearch, updateAllExploreCardBookmarkStates } from './explore.js';
import { clearMarkers } from './map.js'; // To clear search marker when switching tabs

document.addEventListener('DOMContentLoaded', async () => {
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
        minZoom: 5.5,
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
    if (openProfileBtn && accountSidePanel) {
        accountSidePanel.style.display = 'none';
        accountSidePanel.style.opacity = '0';

        openProfileBtn.addEventListener('click', () => {
            if (accountSidePanel.style.display === 'none' && accountSidePanel.style.opacity === '0') {
                accountSidePanel.style.display = 'flex';
                accountSidePanel.style.opacity = '1'
            } else {
                accountSidePanel.style.display = 'none';
                accountSidePanel.style.opacity = '0'
            }
        });
    } else {
        console.warn('One or both account panel elements not found (open-profile-btn, account-side-panel).');
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
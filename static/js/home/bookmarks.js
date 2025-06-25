// bookmarks.js
import { showToast } from './utils.js';
import { addLocationToMap } from './map.js'; // For "View on Map" functionality

export function getBookmarks() {
    const bookmarks = localStorage.getItem('mapBookmarks');
    return bookmarks ? JSON.parse(bookmarks) : [];
}

function saveBookmarks(bookmarks) {
    localStorage.setItem('mapBookmarks', JSON.stringify(bookmarks));
}

export function isBookmarked(lat, lon) {
    const bookmarks = getBookmarks();
    // Compare lat/lon with a small tolerance for floating point inaccuracies
    return bookmarks.some(b => 
        Math.abs(b.lat - lat) < 0.000001 && Math.abs(b.lon - lon) < 0.000001
    );
}

export function toggleBookmark(lat, lon, name, mapInstance, type = 'explore-card') {
    let bookmarks = getBookmarks();
    const existingIndex = bookmarks.findIndex(b => 
        Math.abs(b.lat - lat) < 0.000001 && Math.abs(b.lon - lon) < 0.000001
    );

    if (existingIndex > -1) {
        // Already bookmarked, remove it
        bookmarks.splice(existingIndex, 1);
        if (type === 'explore-card') {
            showToast('Removed from bookmarks', 'error');
        } else {
            showToast(`"${name}" removed from bookmarks.`, 'error');
        }
    } else {
        // Not bookmarked, add it
        bookmarks.push({ lat, lon, name, timestamp: new Date().toISOString() });
        if (type === 'explore-card') {
            showToast('Added to bookmarks', 'success');
        } else {
            showToast(`"${name}" added to bookmarks!`, 'success');
        }
    }
    saveBookmarks(bookmarks);
    // Reload bookmarks grid if currently on the bookmarks tab
    if (document.getElementById('bookmarks').style.display === 'flex') {
        loadBookmarks(mapInstance); // Pass mapInstance to loadBookmarks
    }
    // This will be called by explore.js after this function
    // updateAllExploreCardBookmarkStates(); 
}

export function loadBookmarks(mapInstance) {
    const bookmarks = getBookmarks();
    const bookmarksGrid = document.getElementById('bookmarks-grid');
    const noBookmarksMessage = document.getElementById('no-bookmarks-message');

    if (!bookmarksGrid || !noBookmarksMessage) {
        console.error("Bookmarks grid or message element not found.");
        return;
    }

    bookmarksGrid.innerHTML = ''; // Clear existing bookmarks

    if (bookmarks.length === 0) {
        noBookmarksMessage.classList.remove('hidden');
    } else {
        noBookmarksMessage.classList.add('hidden');
        bookmarks.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)); // Sort by most recent
        bookmarks.forEach(bookmark => {
            const bookmarkCard = document.createElement('div');
            bookmarkCard.classList.add('explore-card', 'card-hover-effect'); // Use explore-card class for styling consistency
            bookmarkCard.innerHTML = `
                <div class="p-4">
                    <h4 class="text-xl font-bold text-white mb-2">${bookmark.name}</h4>
                    <p class="text-sm text-gray-300">Lat: ${bookmark.lat.toFixed(4)}, Lon: ${bookmark.lon.toFixed(4)}</p>
                </div>
                <button class="bookmark-btn bookmark-remove-btn" data-lat="${bookmark.lat}" data-lon="${bookmark.lon}" data-name="${bookmark.name}">
                    <span class="material-symbols-outlined bookmark-icon text-lg" style="font-variation-settings: 'FILL' 1;">bookmark</span>
                </button>
                <button class="view-on-map-btn absolute bottom-4 right-4 bg-[var(--accent-color)] text-white px-3 py-1 rounded-lg text-sm hover:bg-opacity-90 transition-colors">View on Map</button>
            `;
            bookmarksGrid.appendChild(bookmarkCard);

            // Add event listener to view on map button
            bookmarkCard.querySelector('.view-on-map-btn').addEventListener('click', () => {
                // Assuming addLocationToMap expects map instance as first arg
                addLocationToMap(mapInstance, bookmark.lat, bookmark.lon, bookmark.name, 'bookmark'); 
                document.getElementById("tab-home").click(); // Switch to home tab
            });

            // Add event listener to remove bookmark button
            bookmarkCard.querySelector('.bookmark-remove-btn').addEventListener('click', (event) => {
                event.stopPropagation(); // Prevent card click
                toggleBookmark(bookmark.lat, bookmark.lon, bookmark.name, mapInstance, 'bookmark');
            });
        });
    }
    console.log('Bookmarks loaded:', bookmarks);
}
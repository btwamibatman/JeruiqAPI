// explore.js
import { isBookmarked, toggleBookmark } from './bookmarks.js'; // Import bookmark functions

export function updateExploreCardBookmarkStates(cardElement, mapInstance) {
    const bookmarkBtn = cardElement.querySelector('.bookmark-btn');
    const bookmarkIcon = cardElement.querySelector('.bookmark-icon');
    if (!bookmarkBtn || !bookmarkIcon) return;

    // Get lat/lon/name from card data attributes
    const lat = parseFloat(cardElement.dataset.lat);
    const lon = parseFloat(cardElement.dataset.lon);
    const name = cardElement.dataset.name || cardElement.querySelector('h4')?.textContent;

    if (isNaN(lat) || isNaN(lon) || !name) {
        console.warn('Explore card missing lat, lon, or name data attributes:', cardElement);
        bookmarkBtn.style.display = 'none'; // Hide bookmark button if data is incomplete
        return;
    }

    const isCardBookmarked = isBookmarked(lat, lon);
    if (isCardBookmarked) {
        bookmarkIcon.style.fontVariationSettings = "'FILL' 1"; // Filled icon
        bookmarkIcon.style.color = 'var(--accent-color)'; // Filled icon color
    } else {
        bookmarkIcon.style.fontVariationSettings = "'FILL' 0"; // Outlined icon
        bookmarkIcon.style.color = '#fff'; // Default color
    }

    // Only add event listener if it's not already added to prevent duplicates
    if (!bookmarkBtn.dataset.listenerAdded) {
        bookmarkBtn.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent card click from propagating
            toggleBookmark(lat, lon, name, mapInstance, 'explore-card'); // Pass mapInstance
            // Update the specific card's bookmark state immediately after toggle
            updateExploreCardBookmarkStates(cardElement, mapInstance); // Pass mapInstance
        });
        bookmarkBtn.dataset.listenerAdded = 'true'; // Mark listener as added
    }
}

export function updateAllExploreCardBookmarkStates(mapInstance) {
    document.querySelectorAll('.explore-card').forEach(card => {
        updateExploreCardBookmarkStates(card, mapInstance);
    });
}

export function setupExploreFilteringAndSearch(exploreGrid, exploreSearchInput, exploreSearchButton, categoryFiltersContainer, mapInstance) {
    if (categoryFiltersContainer && exploreGrid) {
        categoryFiltersContainer.addEventListener('click', (event) => {
            const clickedButton = event.target.closest('.category-filter');
            if (clickedButton) {
                // Remove 'active-category' from all buttons
                document.querySelectorAll('.category-filter').forEach(btn => {
                    btn.classList.remove('active-category');
                });

                // Add 'active-category' to the clicked button
                clickedButton.classList.add('active-category');

                const category = clickedButton.dataset.category;
                filterExploreCards(exploreGrid, category);
            }
        });
    }

    if (exploreSearchInput && exploreSearchButton && exploreGrid) {
        const performExploreSearch = () => {
            const searchTerm = exploreSearchInput.value.toLowerCase().trim();
            const exploreCards = exploreGrid.querySelectorAll('.explore-card');

            exploreCards.forEach(card => {
                const title = card.querySelector('h4')?.textContent.toLowerCase();
                const description = card.querySelector('p')?.textContent.toLowerCase();
                const category = card.dataset.category?.toLowerCase();

                if (
                    !searchTerm ||
                    (title && title.includes(searchTerm)) ||
                    (description && description.includes(searchTerm)) ||
                    (category && category.includes(searchTerm))
                ) {
                    card.style.display = 'block'; // Or 'flex'
                } else {
                    card.style.display = 'none';
                }
            });
        };

        exploreSearchButton.addEventListener('click', performExploreSearch);
        exploreSearchInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                performExploreSearch();
            }
        });
    }
    // Initial load: ensure explore card bookmark states are correct
    updateAllExploreCardBookmarkStates(mapInstance);
}

function filterExploreCards(exploreGrid, selectedCategory) {
    const exploreCards = exploreGrid.querySelectorAll('.explore-card');
    exploreCards.forEach(card => {
        const cardCategory = card.dataset.category;
        if (selectedCategory === 'all' || cardCategory === selectedCategory) {
            card.style.display = 'block'; // Or 'flex' if that's your default display
        } else {
            card.style.display = 'none';
        }
    });
}
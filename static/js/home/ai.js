import { clearMarkers, addLocationToMap, fitMapToMarkers } from './map.js';

export async function processAiQuery(query, mapInstance) {
    const homeAiContainer = document.querySelector('.home-ai-container');
    const homeAiInput = document.getElementById('home-ai-input');
    if (!query) return;
    if (homeAiContainer) homeAiContainer.classList.add('gradient-border');
    if (homeAiInput) homeAiInput.disabled = true;

    try {
        const token = localStorage.getItem('jwt_token');
        const response = await fetch('/ai/query', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });
        if (!response.ok) throw new Error('AI query failed');
        const data = await response.json();

        // Clear previous markers
        clearMarkers(mapInstance);

        // Mark all returned locations
        if (Array.isArray(data.locations)) {
            data.locations.forEach(loc => {
                addLocationToMap(mapInstance, loc.lat, loc.lon, loc.name, 'search', false);
            });
            fitMapToMarkers(mapInstance);
        } else {
            alert('No locations found for your query.');
        }
    } catch (err) {
        alert('AI failed to process your request.');
        console.error(err);
    } finally {
        if (homeAiContainer) homeAiContainer.classList.remove('gradient-border');
        if (homeAiInput) homeAiInput.disabled = false;
    }
}
// map.js
// Assumes L (Leaflet) is globally available from the script tag in HTML

let searchMarkers = []; // Array to store search markers

// Custom Red Icon for Bookmarks (if map.js needs it for bookmark markers)
export const redIcon = L.ExtraMarkers.icon({
    icon: 'fa-circle',
    markerColor: 'red',
    shape: 'circle',
    prefix: 'fa'
});

// Custom Blue Icon for Search Results
export const blueIcon = L.ExtraMarkers.icon({
    icon: 'fa-circle',
    markerColor: 'blue',
    shape: 'circle',
    prefix: 'fa'
}); 

export function addLocationToMap(mapInstance, lat, lon, name, type = 'search', clear = true) {
    if (clear) clearMarkers(mapInstance); // Only clear is requested
    const markerIcon = type === 'bookmark' ? redIcon : blueIcon;
    const marker = L.marker([lat, lon], { icon: markerIcon }).addTo(mapInstance);
    if (name) marker.openPopup(); // Add a popup with the name
    searchMarkers.push(marker); // Keep track of this new marker
    mapInstance.setView([lat, lon], 13); // Center map on the new marker
}

export function addMarkerWithoutClearing(mapInstance, lat, lon, name, type = 'search') {
    const markerIcon = type === 'bookmark' ? redIcon : blueIcon;
    const marker = L.marker([lat, lon], { icon: markerIcon }).addTo(mapInstance);
    if (name) marker.openPopup(); // Add a popup with the name
    searchMarkers.push(marker); // Keep track of this new marker
}

export function clearMarkers(mapInstance) {
    searchMarkers.forEach(marker => mapInstance.removeLayer(marker));
    searchMarkers = []; // Clear the array after removing markers
}

export function fitMapToMarkers(mapInstance) {
    if (searchMarkers.length > 0) {
        const group = L.featureGroup(searchMarkers);
        mapInstance.fitBounds(group.getBounds().pad(0.2));
    }
}

export async function performPhotonSearch(mapInstance, queryText) {
    if (!mapInstance) {
        console.error('Map instance is not provided to performPhotonSearch.');
        return null;
    }

    // Kazakhstan bounding box: minLon, minLat, maxLon, maxLat
    const bbox = [46.50, 40.95, 87.35, 55.95].join(',');
    const url = `https://photon.komoot.io/api/?q=${encodeURIComponent(queryText)}&lang=en&limit=10&bbox=${bbox}`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        // Filter by country: Kazakhstan (country code 'KZ')
        const filtered = data.features.filter(f =>
            f.properties.countrycode === 'KZ'
        );

        if (filtered.length > 0) {
            const result = filtered[0];
            const lat = result.geometry.coordinates[1];
            const lon = result.geometry.coordinates[0];
            const displayName = result.properties.name +
                (result.properties.city ? ', ' + result.properties.city : '') +
                (result.properties.country ? ', ' + result.properties.country : '');

            mapInstance.flyTo([lat, lon], 13, {
                duration: 1.5,
                easeLinearity: 0.5
            });
            addLocationToMap(mapInstance, lat, lon, displayName, 'search');
            return { lat, lon, name: displayName };
        } else {
            console.warn('No results found for Photon query:', queryText);
            return null;
        }
    } catch (error) {
        console.error('Error in performPhotonSearch:', error);
        return null;
    }
}
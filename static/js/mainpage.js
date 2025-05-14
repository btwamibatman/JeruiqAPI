const marked = window.marked;
const DOMPurify = window.DOMPurify;

function initAIChat() {
    localStorage.clear();

    const chatContainer = document.getElementById('ai-chat-container');
    const chatLog = document.getElementById('ai-chat-log');
    const chatInput = document.getElementById('ai-chat-input');
    const sendButton = document.getElementById('send-message');
    let sessionId = null;

    function appendMessage(message, sender, isHTML = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        if (isHTML) {
            const renderedHTML = marked.parse(message);
            const sanitizedHTML = DOMPurify.sanitize(renderedHTML);
            messageDiv.innerHTML = sanitizedHTML;
        } else {
            messageDiv.textContent = message;
        }
        chatLog.appendChild(messageDiv);
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;
    
        try {
            console.log('Sending message:', message);
            console.log('Session ID:', sessionId);
    
            if (!sessionId) {
                console.log('No session ID found, initializing chat...');
                await initializeChat();
            }
    
            appendMessage(message, 'user');
            chatInput.value = '';
    
            const response = await fetch('/api/chat/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: sessionId
                })
            });
    
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
    
            const data = await response.json();
            console.log('Server response:', data);
            appendMessage(data.response, 'bot', true);
    
        } catch (error) {
            console.error('Error:', error);
            appendMessage('Error: Couldn’t connect—let’s try again! What do you love about nature?', 'bot');
            await initializeChat(); // Reinitialize chat on any error
        }
    }

    async function initializeChat() {
        try {
            console.log('Initializing chat session...');
            const response = await fetch('/api/chat/create_session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
    
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
    
            const data = await response.json();
            sessionId = data.session_id;
            console.log('Chat session initialized with ID:', sessionId);
    
            chatLog.innerHTML = '';
            appendMessage('Hello! How can I help you explore Kazakhstan today?', 'bot');
    
        } catch (error) {
            console.error('Error initializing chat session:', error);
            appendMessage('Error connecting to chat service. Please try again in a moment.', 'bot');
            // Add a retry mechanism
            setTimeout(initializeChat, 5000);
        }
    }

    initializeChat();

    if (sendButton && chatInput) {
        sendButton.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    } else {
        console.error("Chat input elements not found!");
    }

    function resetScroll() {
        if (chatLog) {
            chatLog.scrollTop = chatLog.scrollHeight;
        }
    }

    function debounce(func, wait) {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    const debouncedResetScroll = debounce(resetScroll, 100);

    function updateChatHeight() {
        const chatContainer = document.getElementById('ai-chat-container');
        if (chatContainer) {
            chatContainer.style.height = `calc(100vh - ${document.getElementById('header').offsetHeight}px - ${2 * parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--spacing-small'))}px - 4.5rem)`;
        }
        debouncedResetScroll();
    }

    const resizeObserver = new ResizeObserver(() => {
        debouncedResetScroll();
    });

    if (chatContainer) {
        resizeObserver.observe(chatContainer);
        resizeObserver.observe(chatLog);
    }

    const observer = new MutationObserver(() => {
        debouncedResetScroll();
    });
    if (chatLog) {
        observer.observe(chatLog, { childList: true, subtree: true });
    }

    window.addEventListener('resize', () => {
        updateChatHeight();
        debouncedResetScroll();
    });
    window.addEventListener('orientationchange', updateChatHeight);
}

document.addEventListener('DOMContentLoaded', () => {
    const logoButton = document.getElementById('logo-button');
    const sidenav = document.getElementById('mySidenav');
    const mainContent = document.getElementById('main');
    const body = document.body;
    const header = document.getElementById('header');
    let isNavOpen = false;

    if (!logoButton) console.error("Logo button not found!");
    if (!sidenav) console.error("Sidenav not found!");
    if (!mainContent) console.error("Main content not found!");
    if (!body) console.error("Body element not found!");

    // --- Cesium Initialization ---

    /* Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJmZjUwMjQ3Mi01NDlhLTQ3MmYtOWQ2YS1hNzBiZDQ5MDk4ZTYiLCJpZCI6Mjk0Mjk2LCJpYXQiOjE3NDQ3MjAyMzJ9.RhhaSbJergx7Uz8OL3ivIrY0yhL6bf58hkGg0QIRX_M';
    const viewer = new Cesium.Viewer('cesiumContainer', {
        baseLayer: Cesium.ImageryLayer.fromWorldImagery(),
        animation: false,
        baseLayerPicker: false,
        fullscreenButton: false,
        geocoder: false,
        homeButton: false,
        infoBox: false,
        sceneModePicker: false,
        selectionIndicator: false,
        timeline: false,
        navigationHelpButton: false,
        navigationInstructionsInitiallyVisible: false
    });

    viewer.creditDisplay.container.style.display = 'none'; // Hide the credits
    viewer.scene.screenSpaceCameraController.maximumZoomDistance = 80000000;
    viewer.scene.maximumscreenSpaceCameraFactor = 10.0;

    function flyToLocation(latitude, longitude) {
        viewer.camera.flyTo({
            destination: Cesium.Cartesian3.fromDegrees(longitude, latitude, 15000.0),
            orientation: {
                heading: Cesium.Math.toRadians(0.0),
                pitch: Cesium.Math.toRadians(-90.0),
                roll: 0.0
            },
            duration: 3.0,
            easingFunction: Cesium.EasingFunction.QUADRATIC_OUT
        });
    } */

    function openNav() {
        body.classList.add('sidenav-open');
        header.classList.add('sidenav-open');
        sidenav.style.width = '16rem';
        isNavOpen = true;
    }

    function closeNav() {
        body.classList.remove('sidenav-open');
        header.classList.remove('sidenav-open');
        sidenav.style.width = '5rem';
        isNavOpen = false;
    }

    logoButton.addEventListener('click', () => {
        isNavOpen ? closeNav() : openNav();
    });

    // --- Search Button and Script ---
    const searchButton = document.getElementById('location-search-button');
    const searchInput = document.querySelector('.searchbar .searchbox');
    
    // Create search error container if it doesn't exist
    let searchErrorContainer = document.getElementById('search-error');
    if (!searchErrorContainer) {
        searchErrorContainer = document.createElement('div');
        searchErrorContainer.id = 'search-error';
        searchErrorContainer.style.display = 'none';
        searchErrorContainer.style.color = 'red';
        searchErrorContainer.style.marginTop = '5px';
        document.querySelector('.searchbar').appendChild(searchErrorContainer);
    }

    if (searchButton && searchInput) {
        searchButton.addEventListener('click', async () => {
            const query = searchInput.value.trim();
            if (query) {
                clearSearchError();
                const nominatimUrl = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=jsonv2&limit=1`;

                try {
                    const response = await fetch(nominatimUrl, {
                        headers: { 'Accept': 'application/json' }
                    });
                    if (!response.ok) throw new Error(`Nominatim API error: ${response.statusText}`);
                    const data = await response.json();

                    if (data && data.length > 0) {
                        const latitude = parseFloat(data[0].lat);
                        const longitude = parseFloat(data[0].lon);
                        flyToLocation(latitude, longitude);
                        searchInput.value = '';
                    } else {
                        showSearchError(`Location "${query}" not found.`);
                    }
                } catch (error) {
                    console.error("Nominatim fetch error:", error);
                    showSearchError("Search failed. Please try again later.");
                }
            }
        });

        searchInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                searchButton.click();
            }
        });

        searchInput.addEventListener('input', clearSearchError);
    }

    function clearSearchError() {
        if (searchErrorContainer) {
            searchErrorContainer.style.display = 'none';
            searchErrorContainer.textContent = '';
        }
    }

    function showSearchError(message) {
        if (searchErrorContainer) {
            searchErrorContainer.textContent = message;
            searchErrorContainer.style.display = 'block';
            setTimeout(() => {
                if (searchErrorContainer.textContent === message) {
                    searchErrorContainer.style.display = 'none';
                    searchErrorContainer.textContent = '';
                }
            }, 5000);
        }
    }

    // --- Filter Button and Script ---
    const filterButton = document.getElementById('filter-btn');
    const filterOptionsPanel = document.getElementById('filter-options-panel');
    const filterModeCheckbox = document.getElementById('filter-mode-checkbox');
    const manualFilterTab = document.getElementById('manual-filter');
    const aiFilterTab = document.getElementById('ai-filter');

    if (filterButton && filterOptionsPanel) {
        filterButton.addEventListener('click', () => {
            filterOptionsPanel.classList.toggle('active');
            
            // When the panel opens, reset scroll in the chat log
            if (filterOptionsPanel.classList.contains('active')) {
                setTimeout(() => {
                    const chatLog = document.getElementById('ai-chat-log');
                    if (chatLog) {
                        chatLog.scrollTop = chatLog.scrollHeight;
                    }
                }, 300); // Small delay to allow panel animation to complete
            }
        });
    } else {
        console.error("Filter button or options panel not found in the DOM!");
    }

    if (filterModeCheckbox && manualFilterTab && aiFilterTab) {
        filterModeCheckbox.addEventListener('change', () => {
            if (filterModeCheckbox.checked) {
                manualFilterTab.classList.remove('active');
                aiFilterTab.classList.add('active');
                
                // Reset scroll when switching to AI chat tab
                setTimeout(() => {
                    const chatLog = document.getElementById('ai-chat-log');
                    if (chatLog) {
                        chatLog.scrollTop = chatLog.scrollHeight;
                    }
                }, 100);
            } else {
                manualFilterTab.classList.add('active');
                aiFilterTab.classList.remove('active');
            }
        });
    } else {
        console.error("One or more filter elements not found in the DOM!");
    }

    // Initialize the chat functionality
    initAIChat();
});
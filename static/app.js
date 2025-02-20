class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.send__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            chatInput: document.querySelector('.chat-input')
        }

        this.state = false;
        this.messages = [];
        this.transitionInProgress = false;
    }

    display() {
        const {openButton, chatBox, sendButton, chatInput} = this.args;

        // Check if we're on the start page or chat page
        if (window.location.pathname === '/' || window.location.pathname === '/index') {
            // Handle start page logic
            sendButton.addEventListener('click', () => this.handleStartPageSubmission(chatInput));
            chatInput.addEventListener('keyup', ({ key }) => {
                if (key === 'Enter') {
                    this.handleStartPageSubmission(chatInput);
                }
            });
        } else if (window.location.pathname === '/chat') {
            // Handle chat page logic
            this.initializeChatPage();
            sendButton.addEventListener('click', () => this.onSendButton(chatBox));
            if (chatInput) {
                chatInput.addEventListener('keyup', ({ key }) => {
                    if (key === 'Enter') {
                        this.onSendButton(chatBox);
                    }
                });
            }
            
            // Add animation class to show the page with fade-in
            document.body.classList.add('fade-in');
        }
    }

    handleStartPageSubmission(inputElement) {
        const query = inputElement.value.trim();
        if (query === '' || this.transitionInProgress) {
            return;
        }
        
        this.transitionInProgress = true;
        
        // Save the query to localStorage for retrieval on chat page
        localStorage.setItem('initialQuery', query);
        
        // Get the chat box container
        const chatBoxContainer = document.querySelector('.chat-box-container');
        const heroSection = document.querySelector('.hero');
        
        if (chatBoxContainer && heroSection) {
            // Animate the chat box to expand
            chatBoxContainer.classList.add('transition-active');
            heroSection.classList.add('fade-content');
            
            // Capture the position for smooth transition
            const rect = chatBoxContainer.getBoundingClientRect();
            localStorage.setItem('transitionData', JSON.stringify({
                top: rect.top,
                left: rect.left,
                width: rect.width,
                height: rect.height
            }));
            
            // Delay redirect to allow animation to complete
            setTimeout(() => {
                window.location.href = '/chat';
            }, 600);
        } else {
            // Fallback if elements not found
            window.location.href = `/chat?initial_query=${encodeURIComponent(query)}`;
        }
    }

    initializeChatPage() {
        // Check for transition data
        const transitionDataStr = localStorage.getItem('transitionData');
        const initialQuery = localStorage.getItem('initialQuery');
        
        if (initialQuery) {
            // Display initial query in chat box
            let msg1 = { name: 'You', message: initialQuery };
            this.messages.push(msg1);
            
            // Show loading indicator
            let loadingMsg = { name: 'Jeruyiq', message: 'Processing your request...' };
            this.messages.push(loadingMsg);
            this.updateChatDisplay();
            
            // Process the initial query
            this.processQuery(initialQuery);
            
            // Clear the localStorage
            localStorage.removeItem('initialQuery');
        } else {
            // Check URL parameters as fallback
            const urlParams = new URLSearchParams(window.location.search);
            const queryParam = urlParams.get('initial_query');
            
            if (queryParam) {
                let msg1 = { name: 'You', message: queryParam };
                this.messages.push(msg1);
                
                let loadingMsg = { name: 'Jeruyiq', message: 'Processing your request...' };
                this.messages.push(loadingMsg);
                this.updateChatDisplay();
                
                this.processQuery(queryParam);
                
                // Clean up URL
                window.history.replaceState({}, document.title, '/chat');
            }
        }
        
        // Apply transition effect if data available
        if (transitionDataStr) {
            try {
                const transitionData = JSON.parse(transitionDataStr);
                const chatContainer = document.querySelector('.chat-container');
                
                if (chatContainer) {
                    // Set initial position to match the starting point
                    chatContainer.style.opacity = '0';
                    chatContainer.style.transform = 'scale(0.8)';
                    
                    // Trigger animation after a tiny delay
                    setTimeout(() => {
                        chatContainer.style.transition = 'all 0.5s ease-out';
                        chatContainer.style.opacity = '1';
                        chatContainer.style.transform = 'scale(1)';
                    }, 50);
                }
            } catch (e) {
                console.error('Error applying transition:', e);
            }
            
            // Clear transition data
            localStorage.removeItem('transitionData');
        }
    }

    processQuery(query) {
        fetch($SCRIPT_ROOT + '/response', {
            method: 'POST',
            body: JSON.stringify({ message: query }),
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => {
            // Remove loading message
            this.messages.pop();
            
            // Add AI response
            let msg2 = { name: 'Jeruyiq', message: r.message };
            this.messages.push(msg2);
            this.updateChatDisplay();
        })
        .catch((error) => {
            console.error('Error:', error);
            // Remove loading message
            this.messages.pop();
            
            let errorMsg = { name: 'Jeruyiq', message: 'Sorry, I encountered an error. Please try again.' };
            this.messages.push(errorMsg);
            this.updateChatDisplay();
        });
    }

    toggleState(chatBox) {
        this.state = !this.state;
        
        if(this.state) {
            chatBox.classList.add('chatbox--active');
        } else {
            chatBox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatBox) {
        var textField = document.getElementById('user-input');
        if (!textField) return;
        
        let text1 = textField.value;
        if (text1 === '') {
            return;
        }

        let msg1 = { name: 'You', message: text1 };
        this.messages.push(msg1);
        this.updateChatDisplay();
        
        textField.value = '';
        
        // Process the query
        this.processQuery(text1);
    }

    updateChatDisplay() {
        const chatBox = document.getElementById('chat-box');
        if (!chatBox) return;
        
        // Clear existing messages
        chatBox.innerHTML = '';
        
        // Add each message
        this.messages.forEach(item => {
            const messageDiv = document.createElement('div');
            messageDiv.className = item.name === 'Jeruyiq' ? 'ai-message' : 'user-message';
            messageDiv.textContent = item.message;
            chatBox.appendChild(messageDiv);
        });
        
        // Scroll to bottom
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    const chatbox = new Chatbox();
    chatbox.display();
});
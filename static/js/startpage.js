document.addEventListener('DOMContentLoaded', () => {
    // Get the buttons by their IDs
    const signupButton = document.getElementById('signup-button');
    const loginButton = document.getElementById('login-button');

    // Add click event listeners
    signupButton.addEventListener('click', () => {
        window.location.href = '/signup';
    });

    loginButton.addEventListener('click', () => {
        window.location.href = '/login';
    });
});
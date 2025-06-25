// Existing toggle logic
const container = document.getElementById('container');
const loginBtn = document.getElementById('login');
const registerBtn = document.getElementById('register');

if (registerBtn && container) {
    registerBtn.addEventListener('click', () => {
        container.classList.add('active');
    });
}

if (loginBtn && container) {
    loginBtn.addEventListener('click', () => {
        container.classList.remove('active');
    });
}

// --- New Form Submission Logic ---
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form'); // The actual login form
    const registerForm = document.getElementById('register-form'); // The actual registration form
    const loginErrorMessage = document.getElementById('login-error-message');
    const registerErrorMessage = document.getElementById('register-error-message');

    // --- Login Form Submission ---
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent default form submission

            loginErrorMessage.textContent = ''; // Clear previous errors

            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;

            try {
                const response = await fetch('/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                });

                const data = await response.json();

                if (response.ok) { // Status code 200-299
                    console.log('Login successful:', data);
                    // Assuming the backend returns {"token": "..."}
                    localStorage.setItem('jwt_token', data.token); // Store the token in localStorage

                    // Redirect to a protected page (e.g., home or dashboard)
                    window.location.href = '/home'; // Adjust the redirect path as needed

                } else {
                    console.error('Login failed:', data);
                    // Display error message from backend
                    const errorMessage = data.message || 'An unknown error occurred during login.';
                    // If message is an object (from Marshmallow validation errors), format it
                    if (typeof errorMessage === 'object') {
                         // Format validation errors nicely
                         let errorString = 'Validation errors:';
                         for (const field in errorMessage) {
                             errorString += `\n${field}: ${errorMessage[field].join(', ')}`;
                         }
                         loginErrorMessage.textContent = errorString;
                    } else {
                         loginErrorMessage.textContent = errorMessage;
                    }
                }
            } catch (error) {
                console.error('Network error during login:', error);
                loginErrorMessage.textContent = 'A network error occurred. Please try again.';
            }
        });
    }

    // --- Registration Form Submission ---
    if (registerForm) {
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent default form submission

            registerErrorMessage.textContent = ''; // Clear previous errors

            const name = document.getElementById('register-name').value;
            const surname = document.getElementById('register-surname').value; // Get surname
            const email = document.getElementById('register-email').value;
            const password = document.getElementById('register-password').value;
            const confirmPassword = document.getElementById('register-confirm-password').value;

            // Basic client-side password confirmation check
            if (password !== confirmPassword) {
                registerErrorMessage.textContent = 'Passwords do not match.';
                return; // Stop submission
            }

            // Concatenate name and surname for the backend (assuming backend expects one 'name' field)
            // const fullName = `${name} ${surname}`.trim();
            // if (!fullName) {
            //     registerErrorMessage.textContent = 'Name and Surname are required.';
            //     return;
            // }

            // Basic check for name and surname presence
            if (!name.trim() || !surname.trim()) {
                registerErrorMessage.textContent = 'Name and Surname are required.';
                return;
            }

            try {
                const response = await fetch('/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    // Send concatenated name
                    body: JSON.stringify({ name: name.trim(), surname: surname.trim(), email, password }),
                });

                const data = await response.json();

                if (response.ok) { // Status code 200-299 (e.g., 201 Created)
                    console.log('Registration successful:', data);
                    // Display success message
                    alert('Registration successful! You can now log in.');
                    // Clear the form
                    registerForm.reset();
                    // Switch to login form
                    if (container) { // Check if container exists (from toggle logic)
                         container.classList.remove('active');
                         loginErrorMessage.textContent = ''; // Clear login errors just in case
                    }


                } else {
                    console.error('Registration failed:', data);
                     // Display error message from backend
                    const errorMessage = data.message || 'An unknown error occurred during registration.';
                     // If message is an object (from Marshmallow validation errors), format it
                    if (typeof errorMessage === 'object') {
                         let errorString = 'Validation errors:';
                         for (const field in errorMessage) {
                             errorString += `\n${field}: ${errorMessage[field].join(', ')}`;
                         }
                         registerErrorMessage.textContent = errorString;
                    } else {
                         registerErrorMessage.textContent = errorMessage;
                    }
                }
            } catch (error) {
                console.error('Network error during registration:', error);
                registerErrorMessage.textContent = 'A network error occurred. Please try again.';
            }
        });
    }
});
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signup-form');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    const passwordStrength = document.getElementById('password-strength');
    const passwordMatch = document.getElementById('password-match');

    if (form) {
        form.addEventListener('submit', function(e) {
            if (password.value !== confirmPassword.value) {
                e.preventDefault();
                showAlert('error', 'Passwords do not match!');
                return false;
            }

            if (!isPasswordStrong(password.value)) {
                e.preventDefault();
                showAlert('error', 'Password must be at least 8 characters long and contain uppercase, lowercase, number and special character');
                return false;
            }
        });
    }

    if (password) {
        password.addEventListener('input', function() {
            updatePasswordStrength(this.value);
        });
    }

    if (confirmPassword) {
        confirmPassword.addEventListener('input', function() {
            updatePasswordMatch(password.value, this.value);
        });
    }

    // Flash message auto-hide
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
});

// Add event listener for the login form if it exists
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault(); // Prevent default form submission

        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');

        const email = emailInput.value;
        const password = passwordInput.value;

        // Simple validation (can be expanded)
        if (!email || !password) {
            showAlert('error', 'Please enter both email and password.');
            return;
        }

        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email, password: password })
            });

            const result = await response.json();

            if (response.ok) {
                // Login successful
                // Store token and redirect or update UI
                console.log('Login successful:', result);
                showAlert('success', 'Login successful!');
                // Example: Redirect to home page
                window.location.href = '/home'; 
            } else {
                // Login failed
                console.error('Login failed:', result);
                showAlert('error', result.message || 'Login failed. Please check your credentials.');
            }
        } catch (error) {
            console.error('Error during login fetch:', error);
            showAlert('error', 'An error occurred during login.');
        }
    });
}

function isPasswordStrong(password) {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    return password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers && hasSpecialChar;
}

function updatePasswordStrength(password) {
    const strengthDiv = document.getElementById('password-strength');
    if (!strengthDiv) return;

    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;

    let strengthText = '';
    let strengthClass = '';

    switch(strength) {
        case 0:
        case 1:
            strengthText = 'Weak';
            strengthClass = 'strength-weak';
            break;
        case 2:
        case 3:
            strengthText = 'Medium';
            strengthClass = 'strength-medium';
            break;
        case 4:
        case 5:
            strengthText = 'Strong';
            strengthClass = 'strength-strong';
            break;
    }

    strengthDiv.textContent = `Password Strength: ${strengthText}`;
    strengthDiv.className = `password-strength ${strengthClass}`;
}

function updatePasswordMatch(password, confirmPassword) {
    const matchDiv = document.getElementById('password-match');
    if (!matchDiv) return;

    if (!confirmPassword) {
        matchDiv.textContent = '';
        return;
    }

    if (password === confirmPassword) {
        matchDiv.textContent = 'Passwords match';
        matchDiv.className = 'password-match strength-strong';
    } else {
        matchDiv.textContent = 'Passwords do not match';
        matchDiv.className = 'password-match strength-weak';
    }
}

function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const form = document.querySelector('form');
    form.insertBefore(alertDiv, form.firstChild);

    setTimeout(() => {
        alertDiv.style.opacity = '0';
        setTimeout(() => alertDiv.remove(), 300);
    }, 5000);
}

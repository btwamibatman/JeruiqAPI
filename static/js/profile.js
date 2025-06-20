document.addEventListener('DOMContentLoaded', function() {
    // Handle flash messages disappearing after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });

    // Password strength indicator for password change
    const newPasswordInput = document.getElementById('new_password');
    if (newPasswordInput) {
        newPasswordInput.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            
            // Length check
            if (password.length >= 8) strength++;
            
            // Uppercase check
            if (password.match(/[A-Z]/)) strength++;
            
            // Lowercase check
            if (password.match(/[a-z]/)) strength++;
            
            // Number check
            if (password.match(/[0-9]/)) strength++;
            
            // Special character check
            if (password.match(/[^A-Za-z0-9]/)) strength++;
            
            const strengthIndicator = document.getElementById('password-strength');
            if (strengthIndicator) {
                switch(strength) {
                    case 0:
                    case 1:
                        strengthIndicator.textContent = 'Weak';
                        strengthIndicator.className = 'strength-weak';
                        break;
                    case 2:
                    case 3:
                        strengthIndicator.textContent = 'Medium';
                        strengthIndicator.className = 'strength-medium';
                        break;
                    case 4:
                    case 5:
                        strengthIndicator.textContent = 'Strong';
                        strengthIndicator.className = 'strength-strong';
                        break;
                }
            }
        });
    }
});

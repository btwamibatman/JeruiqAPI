document.addEventListener('DOMContentLoaded', function () {
    // --- Element References ---
    const profileUsernameElement = document.getElementById("profile-username");
    const profileEmailElement = document.getElementById("profile-email");
    const profileBioElement = document.getElementById("profile-bio");
    const profilePicturePreview = document.getElementById('profile-picture-preview');
    // Edit form fields
    const editProfileForm = document.querySelector('.edit-profile-form');
    const nameInput = document.getElementById('name');
    const surnameInput = document.getElementById('surname');
    const emailInput = document.getElementById('email');
    const bioEditInput = document.getElementById('bio-edit');
    const profilePictureInput = document.getElementById('profile-picture');
    const instagramInput = document.getElementById('instagram');
    const telegramInput = document.getElementById('telegram');
    const xInput = document.getElementById('x');
    // Profile completion bar
    const completionBar = document.getElementById('profile-completion-bar');
    const completionLabel = document.getElementById('profile-completion-label');

    // --- Function to fetch and display user profile data ---
    async function fetchAndDisplayUserProfile() {
        const token = localStorage.getItem('jwt_token');
        if (!token) {
            console.error('No JWT token found for profile fetch.');
            // Use placeholder data if no token
            if (profileUsernameElement) profileUsernameElement.textContent = 'Guest User';
            if (profileEmailElement) profileEmailElement.textContent = 'Please log in';
            return;
        }

        try {
            const response = await fetch('/api/profile?t=' + Date.now(), {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.status === 401) {
                console.error('Profile fetch failed: Unauthorized.');
                localStorage.removeItem('jwt_token');
                window.location.href = '/login';
                return;
            }

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const userData = await response.json();
            
            // Populate profile header
            if (profileUsernameElement) profileUsernameElement.textContent = `${userData.name} ${userData.surname}`;
            if (profileEmailElement) profileEmailElement.textContent = userData.email;
            // Assuming bio comes from user data, add it if available
            if (profileBioElement) profileBioElement.textContent = userData.bio || 'No bio available';

            // Populate edit form
            if (nameInput) nameInput.value = userData.name || '';
            if (surnameInput) surnameInput.value = userData.surname || '';
            if (emailInput) emailInput.value = userData.email || '';
            if (bioEditInput) bioEditInput.value = userData.bio || '';
            if (instagramInput) instagramInput.value = userData.social_links?.instagram || '';
            if (telegramInput) telegramInput.value = userData.social_links?.telegram || '';
            if (xInput) xInput.value = userData.social_links?.x || '';

            // Optionally, show current profile picture preview
            if (profilePicturePreview && userData.profile_picture) {
                profilePicturePreview.src = `/static/${userData.profile_picture}?t=${Date.now()}`;
            }

            // Update profile completion bar
            if (completionBar && completionLabel && userData.profile_completion !== undefined) {
                completionBar.style.width = `${userData.profile_completion}%`;
                completionLabel.textContent = `${userData.profile_completion}%`;
            }

            const socialLinksList = document.getElementById('social-links-list');
            if (socialLinksList) {
                socialLinksList.innerHTML = '';
                if (userData.social_links?.instagram) {
                    socialLinksList.innerHTML += `<li><a href="${userData.social_links.instagram}" target="_blank" class="text-[var(--text-secondary)] hover:underline">Instagram</a></li>`;
                }
                if (userData.social_links?.telegram) {
                    socialLinksList.innerHTML += `<li><a href="${userData.social_links.telegram}" target="_blank" class="text-[var(--text-secondary)] hover:underline">Telegram</a></li>`;
                }
                // Add more as needed
            }
        } catch (error) {
            console.error('Error fetching user profile:', error);
            if (profileUsernameElement) profileUsernameElement.textContent = 'Error Loading Profile';
        }
    }
    // --- Edit Profile Functionality ---
    if (editProfileForm) {
        editProfileForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const token = localStorage.getItem('jwt_token');
            if (!token) {
                alert('You must be logged in to edit your profile.');
                return;
            }

            const formData = new FormData();
            formData.append('name', nameInput.value);
            formData.append('surname', surnameInput.value);
            formData.append('email', emailInput.value);
            formData.append('bio', bioEditInput ? bioEditInput.value : '');
            if (profilePictureInput && profilePictureInput.files.length > 0) {
                formData.append('profile_picture', profilePictureInput.files[0]);
            }
            const socialLinks = {
                instagram: instagramInput.value,
                telegram: telegramInput.value,
                x: xInput.value
            };
            formData.append('social_links', JSON.stringify(socialLinks));

            try {
                const response = await fetch('/api/profile?t=' + Date.now(), {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    body: formData
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    alert(errorData.message || 'Failed to update profile.');
                    return;
                }

                alert('Profile updated successfully!');
                fetchAndDisplayUserProfile();
                switchTab('#account');
            } catch (error) {
                alert('An error occurred while updating your profile.');
            }
        });
    }

    // File preview (run once, outside submit handler)
    if (profilePictureInput) {
        profilePictureInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    if (profilePicturePreview) profilePicturePreview.src = e.target.result;
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    }

    // --- Tab Switching Logic ---
    const tabLinks = document.querySelectorAll('.profile-tab-link');
    const tabLinkButtons = document.querySelectorAll('.profile-tab-link-button');
    const sections = document.querySelectorAll('.profile-section');

    function switchTab(targetId) {
        // Deactivate all links
        tabLinks.forEach(navLink => {
            if (navLink.getAttribute('href') === targetId) {
                navLink.classList.add('active');
            } else {
                navLink.classList.remove('active');
            }
        });

        // Hide all sections and show the target one
        sections.forEach(section => {
            if (`#${section.id}` === targetId) {
                section.style.display = 'block';
            } else {
                section.style.display = 'none';
            }
        });
    }
    tabLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            switchTab(targetId);
        });
    });
    
    // Also allow buttons to switch tabs
    tabLinkButtons.forEach(button => {
        button.addEventListener('click', function (e) {
             e.preventDefault();
            const targetId = this.getAttribute('href');
            switchTab(targetId);
        });
    });
    // Show the first section by default
    if (tabLinks.length > 0) {
        // To handle page reloads on a hash, check the URL hash first
        const currentHash = window.location.hash || tabLinks[0].getAttribute('href');
        switchTab(currentHash);
    }

    // Initial Setup ---
    fetchAndDisplayUserProfile();
});
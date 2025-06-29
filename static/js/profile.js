document.addEventListener('DOMContentLoaded', function () {
    // Banner elements
    const bannerUploadBtn = document.getElementById('banner-upload-btn');
    const bannerUploadInput = document.getElementById('banner-upload');
    const profileBanner = document.getElementById('profile-banner');
    // --- Element References ---
    const profileUsernameElement = document.getElementById("profile-username");
    const profileEmailElement = document.getElementById("profile-email");
    const profileLocationElement = document.getElementById("profile-location");
    const profileBioElement = document.getElementById("profile-bio");
    const profilePicturePreview = document.getElementById('profile-picture-preview');
    // Profile stats
    const statTrips = document.getElementById('stat-trips');
    const statPoints = document.getElementById('stat-points');
    const statRanking = document.getElementById('stat-ranking');
    // Edit form fields
    const editProfileForm = document.querySelector('.edit-profile-form');
    const nameInput = document.getElementById('name');
    const surnameInput = document.getElementById('surname');
    const emailInput = document.getElementById('email');
    const locationInput = document.getElementById('location');
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

            if (response.status === 401 || response.status === 403) {
                localStorage.removeItem('jwt_token');
                window.location.href = '/login';
                return;
            }

            if (!response.ok) {
                const error = await response.json();
                alert(error.message || `HTTP error! status: ${response.status}`);
                return;
            }

            const userData = await response.json();

            // Populate profile header
            if (profileUsernameElement) profileUsernameElement.textContent = `${userData.name ?? ''} ${userData.surname ?? ''}`;
            if (profileEmailElement) profileEmailElement.textContent = userData.email ?? '';
            if (profileLocationElement) profileLocationElement.textContent = userData.location || 'No location set';
            if (profileBioElement) profileBioElement.textContent = userData.bio || 'No bio yet';

            // Populate profile stats
            if (statTrips) statTrips.textContent = userData.trips_count ?? (userData.trips ? userData.trips.length : 0);
            if (statPoints) statPoints.textContent = userData.points ?? 0;
            if (statRanking) statRanking.textContent = userData.ranking ? `#${userData.ranking}` : '#0';

            // Populate edit form
            if (nameInput) nameInput.value = userData.name || '';
            if (surnameInput) surnameInput.value = userData.surname || '';
            if (emailInput) emailInput.value = userData.email || '';
            if (locationInput) locationInput.value = userData.location || '';
            if (bioEditInput) bioEditInput.value = userData.bio || '';
            if (instagramInput) instagramInput.value = userData.social_links?.instagram || '';
            if (telegramInput) telegramInput.value = userData.social_links?.telegram || '';
            if (xInput) xInput.value = userData.social_links?.x || '';

            // Profile picture preview
            if (profilePicturePreview && userData.profile_picture) {
                profilePicturePreview.src = `/static/${userData.profile_picture}?t=${Date.now()}`;
            }

            // Profile completion bar
            if (completionBar && completionLabel && userData.profile_completion !== undefined) {
                completionBar.style.width = `${userData.profile_completion}%`;
                completionLabel.textContent = `${userData.profile_completion}%`;
            }

            // --- Dashboard Widgets ---

            // Upcoming Trip Widget
            const upcomingTripContainer = document.getElementById('upcoming-trip-widget-content');
            if (upcomingTripContainer && Array.isArray(userData.trips)) {
                const now = new Date();
                const nextTrip = userData.trips
                    .map(trip => ({
                        ...trip,
                        startDateObj: new Date(trip.startDate)
                    }))
                    .filter(trip => trip.startDateObj > now)
                    .sort((a, b) => a.startDateObj - b.startDateObj)[0];

                if (nextTrip) {
                    upcomingTripContainer.innerHTML = `
                        <div class="trip-card flex items-center gap-4">
                            <img src="${nextTrip.imageUrl ?? '/static/img/default-trip.jpg'}" class="rounded-lg w-24 h-24 object-cover">
                            <div>
                                <h4 class="font-bold text-lg">${nextTrip.title ?? 'Untitled Trip'}</h4>
                                <p class="text-[var(--text-secondary)]">${nextTrip.dateRange ?? ''}</p>
                                <a href="/trips/${nextTrip.trip_id ?? nextTrip.id}" class="text-[var(--accent-color)] hover:underline">View Booking</a>
                            </div>
                        </div>`;
                } else {
                    upcomingTripContainer.innerHTML = `<p class="text-[var(--text-secondary)]">No upcoming trips. <a href="/tours" class="text-[var(--accent-color)] hover:underline">Time to explore!</a></p>`;
                }
            }

            renderSocialLinks(userData);
            setBannerImage(userData);

            // TODO: Populate full #my-trips and #my-wishlist sections on tab click if needed

        } catch (error) {
            console.error('Error fetching user profile:', error);
            if (profileUsernameElement) profileUsernameElement.textContent = 'Error Loading Profile';
        }
    }

    function renderSocialLinks(userData) {
        const socialLinksList = document.getElementById('social-links-list');
        if (!socialLinksList) return;
        socialLinksList.innerHTML = '';

        const platforms = [
            { key: 'instagram', icon: 'fab fa-instagram', label: 'Instagram' },
            { key: 'telegram', icon: 'fab fa-telegram', label: 'Telegram' },
            { key: 'x', icon: 'fab fa-x-twitter', label: 'X' }
        ];

        platforms.forEach(({ key, icon, label }) => {
            const value = userData.social_links?.[key] || '';
            socialLinksList.innerHTML += `
                <li class="overflow-hidden flex">
                    ${value ? `<a href="${value}" target="_blank" title="${label}" id="link-${key}">
                        <i class="${icon} social-icon"></i>
                    </a>` : `<i class="${icon} text-gray-400 social-icon"></i>`}
                    <div class="social-link-row flex justify-between items-center flex-1 ml-2">
                        <span class="social-link-name">${label}</span>
                        <button class="edit-social-link-btn" data-platform="${key}" title="Edit ${label}">
                            <i class="fas fa-pen"></i>
                        </button>
                    </div>
                </li>
            `;
        });

        // Add event listeners for edit buttons
        document.querySelectorAll('.edit-social-link-btn').forEach(btn => {
            btn.addEventListener('click', function () {
                const platform = this.dataset.platform;
                const currentValue = userData.social_links?.[platform] || '';
                const newValue = prompt(`Enter your ${platform} link:`, currentValue);
                if (newValue !== null) {
                    // Save to backend
                    updateSingleSocialLink(platform, newValue);
                }
            });
        });
    }
    async function updateSingleSocialLink(platform, value) {
        const token = localStorage.getItem('jwt_token');
        // Fetch current social_links
        const response = await fetch('/api/profile', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const userData = await response.json();
        const social_links = userData.social_links || {};
        social_links[platform] = value;

        // Send update to backend
        const formData = new FormData();
        formData.append('social_links', JSON.stringify(social_links));

        await fetch('/api/profile', {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData
        });
        // Refresh profile
        fetchAndDisplayUserProfile();
    }

    // --- Banner Upload Functionality ---
    if (bannerUploadBtn && bannerUploadInput) {
        bannerUploadBtn.addEventListener('click', function () {
            bannerUploadInput.click();
        });

        bannerUploadInput.addEventListener('change', async function () {
            if (this.files && this.files[0]) {
                const token = localStorage.getItem('jwt_token');
                const formData = new FormData();
                formData.append('banner_image', this.files[0]);
                const response = await fetch('/api/profile', {
                    method: 'PUT',
                    headers: { 'Authorization': `Bearer ${token}` },
                    body: formData
                });
                if (response.ok) {
                    fetchAndDisplayUserProfile();
                } else {
                    alert('Failed to update banner.');
                }
            }
        });
    }
    // When displaying the profile, set the banner image:
    function setBannerImage(userData) {
        if (profileBanner) {
            const url = userData.banner_image
                ? `/static/${userData.banner_image}`
                : '/static/default-banner.jpg';
            profileBanner.style.backgroundImage = `url('${url}')`;
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
            formData.append('location', locationInput.value);
            formData.append('bio', bioEditInput ? bioEditInput.value : '');
            if (profilePictureInput && profilePictureInput.files.length > 0) {
                formData.append('profile_picture', profilePictureInput.files[0]);
            }
            const socialLinks = {
                instagram: instagramInput.value,
                telegram: telegramInput.value,
                x: xInput.value,
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
                switchTab('#dashboard');
            } catch (error) {
                alert('An error occurred while updating your profile.');
            }
        });
    }
    // File preview (run once, outside submit handler)
    if (profilePictureInput) {
        profilePictureInput.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function (e) {
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
        tabLinks.forEach(navLink => {
            if (navLink.getAttribute('href') === targetId) {
                navLink.classList.add('active');
            } else {
                navLink.classList.remove('active');
            }
        });
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
    tabLinkButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            switchTab(targetId);
        });
    });
    if (tabLinks.length > 0) {
        const currentHash = window.location.hash || tabLinks[0].getAttribute('href');
        switchTab(currentHash);
    }

    // Initial Setup ---
    fetchAndDisplayUserProfile();
});
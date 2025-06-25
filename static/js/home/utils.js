// utils.js
export function showToast(message, type = 'info', duration = 3000) {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        console.error('Toast container not found!');
        return;
    }

    const toast = document.createElement('div');
    toast.classList.add('toast', 'p-3', 'rounded-lg', 'shadow-md', 'text-white', 'mb-3', 'flex', 'items-center', 'space-x-2');

    if (type === 'success') {
        toast.classList.add('bg-green-500');
        toast.innerHTML = `<span class="material-symbols-outlined">check_circle</span> <span>${message}</span>`;
    } else if (type === 'error') {
        toast.classList.add('bg-red-500');
        toast.innerHTML = `<span class="material-symbols-outlined">error</span> <span>${message}</span>`;
    } else {
        toast.classList.add('bg-gray-700');
        toast.innerHTML = `<span class="material-symbols-outlined">info</span> <span>${message}</span>`;
    }

    toastContainer.appendChild(toast);

    // Animate in
    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
    }, 10); // Small delay for CSS transition to apply

    // Animate out and remove
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-20px)';
        toast.addEventListener('transitionend', () => toast.remove());
    }, duration);
}
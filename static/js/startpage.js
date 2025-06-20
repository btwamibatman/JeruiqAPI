document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const closeMobileMenuButton = document.getElementById('close-mobile-menu');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuLinks = document.querySelectorAll('.mobile-menu-link');

    mobileMenuButton.addEventListener('click', () => {
        mobileMenu.classList.remove('hidden');
    });

    closeMobileMenuButton.addEventListener('click', () => {
        mobileMenu.classList.add('hidden');
    });

    mobileMenuLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // Scroll reveal animation
    const revealElements = document.querySelectorAll('.reveal');
    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;
        revealElements.forEach(el => {
            const elementTop = el.getBoundingClientRect().top;
            if (elementTop < windowHeight - 100) {
                el.classList.add('active');
            }
        });
    };
    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Initial check

    // Dombra sound using Tone.js
    const playDombraButton = document.getElementById('play-dombra');
    let isPlaying = false;
    let synth;

    playDombraButton.addEventListener('click', async () => {
        await Tone.start();
        
        if (!synth) {
                synth = new Tone.PluckSynth().toDestination();
        }

        if (!isPlaying) {
            isPlaying = true;
            playDombraButton.innerHTML = '<i class="fas fa-pause text-2xl"></i>';
            
            // A simple, pleasant melody to represent the Dombra
            const now = Tone.now();
            synth.triggerAttackRelease("G3", "8n", now);
            synth.triggerAttackRelease("D4", "8n", now + 0.25);
            synth.triggerAttackRelease("E4", "4n", now + 0.5);
            synth.triggerAttackRelease("D4", "8n", now + 1.0);
            synth.triggerAttackRelease("G3", "8n", now + 1.25);
            synth.triggerAttackRelease("A3", "4n", now + 1.5);
            
            setTimeout(() => {
                    isPlaying = false;
                    playDombraButton.innerHTML = '<i class="fas fa-play text-2xl"></i>';
            }, 2000);

        } else {
            // This example doesn't support stopping, but this structure allows for it.
            // For a real implementation, Tone.Transport would be used to manage sequences.
        }
    });
});
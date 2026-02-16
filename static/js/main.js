/**
 * Main JavaScript for Company Website
 * Handles theme switching and mobile navigation
 */

(function() {
    'use strict';

    // Theme Management
    const ThemeManager = {
        STORAGE_KEY: 'theme',
        LIGHT: 'light',
        DARK: 'dark',

        init() {
            this.themeToggle = document.querySelector('.theme-toggle');
            this.html = document.documentElement;

            // Load saved theme or detect system preference
            const savedTheme = localStorage.getItem(this.STORAGE_KEY);
            if (savedTheme) {
                this.setTheme(savedTheme);
            } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                this.setTheme(this.DARK);
            }

            // Listen for theme toggle clicks
            if (this.themeToggle) {
                this.themeToggle.addEventListener('click', () => this.toggle());
            }

            // Listen for system theme changes
            if (window.matchMedia) {
                window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                    if (!localStorage.getItem(this.STORAGE_KEY)) {
                        this.setTheme(e.matches ? this.DARK : this.LIGHT);
                    }
                });
            }
        },

        setTheme(theme) {
            this.html.setAttribute('data-theme', theme);
            localStorage.setItem(this.STORAGE_KEY, theme);
        },

        toggle() {
            const currentTheme = this.html.getAttribute('data-theme');
            const newTheme = currentTheme === this.DARK ? this.LIGHT : this.DARK;
            this.setTheme(newTheme);
        }
    };

    // Mobile Navigation
    const MobileNav = {
        init() {
            this.menuBtn = document.querySelector('.mobile-menu-btn');
            this.navLinks = document.querySelector('.nav-links');

            if (this.menuBtn && this.navLinks) {
                this.menuBtn.addEventListener('click', () => this.toggle());

                // Close menu when clicking on a link
                this.navLinks.querySelectorAll('.nav-link').forEach(link => {
                    link.addEventListener('click', () => this.close());
                });

                // Close menu when clicking outside
                document.addEventListener('click', (e) => {
                    if (!this.menuBtn.contains(e.target) && !this.navLinks.contains(e.target)) {
                        this.close();
                    }
                });
            }
        },

        toggle() {
            this.navLinks.classList.toggle('active');
            this.menuBtn.classList.toggle('active');
        },

        close() {
            this.navLinks.classList.remove('active');
            this.menuBtn.classList.remove('active');
        }
    };

    // Smooth Scroll for anchor links
    const SmoothScroll = {
        init() {
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', (e) => {
                    const targetId = anchor.getAttribute('href');
                    if (targetId === '#') return;

                    const target = document.querySelector(targetId);
                    if (target) {
                        e.preventDefault();
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });
        }
    };

    // Navbar scroll effect
    const NavbarScroll = {
        init() {
            this.navbar = document.querySelector('.navbar');
            if (!this.navbar) return;

            let lastScroll = 0;

            window.addEventListener('scroll', () => {
                const currentScroll = window.pageYOffset;

                if (currentScroll > 100) {
                    this.navbar.classList.add('scrolled');
                } else {
                    this.navbar.classList.remove('scrolled');
                }

                lastScroll = currentScroll;
            });
        }
    };

    // Form validation enhancement
    const FormEnhancer = {
        init() {
            const forms = document.querySelectorAll('.contact-form');
            forms.forEach(form => {
                form.addEventListener('submit', (e) => {
                    const inputs = form.querySelectorAll('.form-input');
                    const submitBtn = form.querySelector('button[type="submit"]');
                    let isValid = true;

                    inputs.forEach(input => {
                        if (input.hasAttribute('required') && !input.value.trim()) {
                            isValid = false;
                            input.classList.add('error');
                        } else {
                            input.classList.remove('error');
                        }
                    });

                    if (!isValid) {
                        e.preventDefault();
                    } else if (submitBtn) {
                        submitBtn.classList.add('loading');
                        submitBtn.disabled = true;
                    }
                });
            });
        }
    };

    // Scroll Animations
    const ScrollAnimations = {
        init() {
            this.elements = document.querySelectorAll('.animate-on-scroll');
            this.observer = new IntersectionObserver(
                (entries) => this.handleIntersection(entries),
                {
                    threshold: 0.1,
                    rootMargin: '0px 0px -50px 0px'
                }
            );

            this.elements.forEach(el => this.observer.observe(el));
        },

        handleIntersection(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                    // Optionally unobserve after animation
                    // this.observer.unobserve(entry.target);
                }
            });
        }
    };

    // Parallax Effect
    const ParallaxEffect = {
        init() {
            this.layers = document.querySelectorAll('.parallax-layer');
            if (this.layers.length === 0) return;

            window.addEventListener('scroll', () => this.update());
        },

        update() {
            const scrolled = window.pageYOffset;
            this.layers.forEach((layer, index) => {
                const speed = (index + 1) * 0.1;
                const yPos = -(scrolled * speed);
                layer.style.transform = `translateY(${yPos}px)`;
            });
        }
    };

    // Cursor Trail Effect (optional, cool effect)
    const CursorTrail = {
        init() {
            if (window.innerWidth < 768) return; // Skip on mobile

            this.coords = { x: 0, y: 0 };
            this.circles = [];

            const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe'];

            for (let i = 0; i < 12; i++) {
                const circle = document.createElement('div');
                circle.className = 'cursor-circle';
                circle.style.cssText = `
                    position: fixed;
                    width: 10px;
                    height: 10px;
                    border-radius: 50%;
                    background: ${colors[i % colors.length]};
                    pointer-events: none;
                    z-index: 9999;
                    opacity: ${1 - i / 12};
                    transition: transform 0.1s ease;
                `;
                document.body.appendChild(circle);
                this.circles.push(circle);
            }

            document.addEventListener('mousemove', (e) => {
                this.coords.x = e.clientX;
                this.coords.y = e.clientY;
            });

            this.animateCircles();
        },

        animateCircles() {
            let x = this.coords.x;
            let y = this.coords.y;

            this.circles.forEach((circle, index) => {
                circle.style.left = x - 5 + 'px';
                circle.style.top = y - 5 + 'px';
                circle.style.transform = `scale(${(this.circles.length - index) / this.circles.length})`;

                const nextCircle = this.circles[index + 1] || this.circles[0];
                x += (parseInt(nextCircle.style.left) || 0) * 0.3;
                y += (parseInt(nextCircle.style.top) || 0) * 0.3;
            });

            requestAnimationFrame(() => this.animateCircles());
        }
    };

    // Image Lazy Loading with Blur Effect
    const LazyImages = {
        init() {
            const images = document.querySelectorAll('img[data-src]');

            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                });
            });

            images.forEach(img => imageObserver.observe(img));
        }
    };

    // Card 3D Tilt Effect
    const Card3DTilt = {
        init() {
            const cards = document.querySelectorAll('.card-3d');

            cards.forEach(card => {
                card.addEventListener('mousemove', (e) => {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;

                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;

                    const rotateX = (y - centerY) / 10;
                    const rotateY = (centerX - x) / 10;

                    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
                });

                card.addEventListener('mouseleave', () => {
                    card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
                });
            });
        }
    };

    // Counter Animation
    const CounterAnimation = {
        init() {
            const counters = document.querySelectorAll('.counter');

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const counter = entry.target;
                        const target = parseInt(counter.dataset.target);
                        this.animateCounter(counter, target);
                        observer.unobserve(counter);
                    }
                });
            });

            counters.forEach(counter => observer.observe(counter));
        },

        animateCounter(element, target) {
            let current = 0;
            const increment = target / 100;
            const duration = 2000;
            const stepTime = duration / 100;

            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    element.textContent = target;
                    clearInterval(timer);
                } else {
                    element.textContent = Math.floor(current);
                }
            }, stepTime);
        }
    };

    // Typing Effect
    const TypingEffect = {
        init() {
            const typingElements = document.querySelectorAll('.typing-text');

            typingElements.forEach(element => {
                const text = element.dataset.text || element.textContent;
                element.textContent = '';
                element.style.visibility = 'visible';
                this.typeText(element, text);
            });
        },

        typeText(element, text, index = 0) {
            if (index < text.length) {
                element.textContent += text.charAt(index);
                setTimeout(() => this.typeText(element, text, index + 1), 50);
            } else {
                // Add blinking cursor after typing is complete
                element.classList.add('typing-complete');
            }
        }
    };

    // Initialize all modules when DOM is ready
    document.addEventListener('DOMContentLoaded', () => {
        ThemeManager.init();
        MobileNav.init();
        SmoothScroll.init();
        NavbarScroll.init();
        FormEnhancer.init();
        ScrollAnimations.init();
        ParallaxEffect.init();
        // CursorTrail.init(); // Uncomment for cursor trail effect
        LazyImages.init();
        // Card3DTilt.init(); // Disabled - simple animations only
        CounterAnimation.init();
        TypingEffect.init();
    });
})();

/**
 * Internationalization helpers for language switching
 */

(function() {
    'use strict';

    const I18nManager = {
        COOKIE_NAME: 'django_language',

        init() {
            this.langSelector = document.querySelector('.language-selector');
            this.langBtn = document.querySelector('.lang-btn');
            this.langDropdown = document.querySelector('.lang-dropdown');

            if (!this.langSelector) return;

            // Keyboard navigation for language dropdown
            if (this.langBtn) {
                this.langBtn.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        this.langDropdown.classList.toggle('show');
                    }
                });
            }

            // Close dropdown on escape
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && this.langDropdown) {
                    this.langDropdown.classList.remove('show');
                }
            });

            // Handle language link clicks (save preference)
            const langLinks = document.querySelectorAll('.lang-dropdown a');
            langLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    const href = link.getAttribute('href');
                    const langCode = href.split('/')[1];
                    this.setLanguageCookie(langCode);
                });
            });
        },

        setLanguageCookie(langCode) {
            document.cookie = `${this.COOKIE_NAME}=${langCode};path=/;max-age=31536000`;
        },

        getCurrentLanguage() {
            const path = window.location.pathname;
            const match = path.match(/^\/([a-z]{2})\//);
            return match ? match[1] : 'ru';
        }
    };

    document.addEventListener('DOMContentLoaded', () => {
        I18nManager.init();
    });
})();

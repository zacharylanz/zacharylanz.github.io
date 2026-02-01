// ===========================
// Matrix Background Effect
// ===========================
function initMatrixEffect() {
    const canvas = document.getElementById('matrix-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const matrix = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()";
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = Array(Math.floor(columns)).fill(1);

    function drawMatrix() {
        ctx.fillStyle = 'rgba(10, 14, 23, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#00ff41';
        ctx.font = fontSize + 'px monospace';

        for (let i = 0; i < drops.length; i++) {
            const text = matrix[Math.floor(Math.random() * matrix.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);

            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }

    setInterval(drawMatrix, 35);

    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
}

// ===========================
// Typing Effect
// ===========================
function initTypingEffect() {
    const typingText = document.querySelector('.typing-text');
    if (!typingText) return;
    const phrases = [
        "Senior Cyber Threat Intelligence Consultant",
        "Threat Hunter & Adversary Analyst",
        "OSINT Investigator",
        "Adjunct Professor @ UAlbany",
        "Published Security Researcher"
    ];

    let phraseIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typingSpeed = 100;

    function type() {
        const currentPhrase = phrases[phraseIndex];

        if (isDeleting) {
            typingText.textContent = currentPhrase.substring(0, charIndex - 1);
            charIndex--;
            typingSpeed = 50;
        } else {
            typingText.textContent = currentPhrase.substring(0, charIndex + 1);
            charIndex++;
            typingSpeed = 100;
        }

        if (!isDeleting && charIndex === currentPhrase.length) {
            typingSpeed = 2000;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            phraseIndex = (phraseIndex + 1) % phrases.length;
            typingSpeed = 500;
        }

        setTimeout(type, typingSpeed);
    }

    type();
}

// ===========================
// Navigation Toggle
// ===========================
function initNavToggle() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    if (!navToggle || !navMenu) return;
    const navLinks = document.querySelectorAll('.nav-link');

    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
            navMenu.classList.remove('active');
        }
    });
}

// ===========================
// Smooth Scrolling
// ===========================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offsetTop = target.offsetTop - 70;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===========================
// Active Nav Link on Scroll
// ===========================
function initScrollSpy() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (window.pageYOffset >= sectionTop - 100) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// ===========================
// Hero Stats Animation
// ===========================
function initStatsAnimation() {
    const threatLevel = document.getElementById('threat-level');
    const status = document.getElementById('status');
    const clearance = document.getElementById('clearance');
    if (!threatLevel || !status || !clearance) return;

    const levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];
    const statuses = ['STANDBY', 'MONITORING', 'ANALYZING', 'ACTIVE'];
    const clearances = ['PENDING', 'VERIFIED', 'AUTHORIZED'];

    let levelIndex = 0;
    let statusIndex = 0;
    let clearanceIndex = 0;

    // Animate to final values
    const levelInterval = setInterval(() => {
        threatLevel.textContent = levels[levelIndex];
        levelIndex++;
        if (levelIndex >= levels.length) {
            clearInterval(levelInterval);
        }
    }, 300);

    setTimeout(() => {
        const statusInterval = setInterval(() => {
            status.textContent = statuses[statusIndex];
            statusIndex++;
            if (statusIndex >= statuses.length) {
                clearInterval(statusInterval);
            }
        }, 300);
    }, 500);

    setTimeout(() => {
        const clearanceInterval = setInterval(() => {
            clearance.textContent = clearances[clearanceIndex];
            clearanceIndex++;
            if (clearanceIndex >= clearances.length) {
                clearInterval(clearanceInterval);
            }
        }, 300);
    }, 1000);
}

// ===========================
// GitHub API Integration
// ===========================
async function fetchGitHubRepos(username) {
    const reposContainer = document.getElementById('github-repos');

    try {
        reposContainer.innerHTML = '<div class="loading-message"><p>Fetching repositories...</p></div>';

        const response = await fetch(`https://api.github.com/users/${username}/repos?sort=updated&per_page=6`);

        if (!response.ok) {
            throw new Error('User not found or API limit reached');
        }

        const repos = await response.json();

        if (repos.length === 0) {
            reposContainer.innerHTML = '<div class="loading-message"><p>No repositories found</p></div>';
            return;
        }

        reposContainer.innerHTML = '';

        repos.forEach(repo => {
            const repoCard = document.createElement('div');
            repoCard.className = 'repo-card';

            repoCard.innerHTML = `
                <div class="repo-header">
                    <h4 class="repo-name">
                        <a href="${repo.html_url}" target="_blank" rel="noopener" class="repo-link">
                            ${repo.name}
                        </a>
                    </h4>
                </div>
                <p class="repo-description">
                    ${repo.description || 'No description available'}
                </p>
                <div class="repo-meta">
                    ${repo.language ? `<span class="repo-language">▪ ${repo.language}</span>` : ''}
                    <span class="repo-stat">★ ${repo.stargazers_count}</span>
                    <span class="repo-stat">⑂ ${repo.forks_count}</span>
                </div>
            `;

            reposContainer.appendChild(repoCard);
        });

    } catch (error) {
        reposContainer.innerHTML = `
            <div class="loading-message">
                <p style="color: var(--accent-danger);">Error: ${error.message}</p>
                <p>Please check the username and try again</p>
            </div>
        `;
    }
}

function initGitHubFetch() {
    const fetchButton = document.getElementById('fetch-repos');
    const usernameInput = document.getElementById('github-username');
    if (!fetchButton || !usernameInput) return;

    fetchButton.addEventListener('click', () => {
        const username = usernameInput.value.trim();
        if (username) {
            fetchGitHubRepos(username);
        }
    });

    // Allow Enter key to trigger fetch
    usernameInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const username = usernameInput.value.trim();
            if (username) {
                fetchGitHubRepos(username);
            }
        }
    });
}

// ===========================
// Intersection Observer for Animations
// ===========================
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe timeline items
    document.querySelectorAll('.timeline-item').forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(30px)';
        item.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(item);
    });

    // Observe cards
    document.querySelectorAll('.cert-card, .education-card, .teaching-card, .publication-card, .affiliation-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// ===========================
// Navbar Scroll Effect
// ===========================
function initNavbarScroll() {
    const navbar = document.querySelector('.nav-bar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        const style = getComputedStyle(document.documentElement);

        if (currentScroll > 100) {
            navbar.style.background = style.getPropertyValue('--nav-bg-scrolled').trim();
            navbar.style.boxShadow = '0 2px 20px ' + style.getPropertyValue('--glow-primary').trim();
        } else {
            navbar.style.background = style.getPropertyValue('--nav-bg').trim();
            navbar.style.boxShadow = 'none';
        }
    });
}

// ===========================
// Terminal Cursor Blink
// ===========================
function initTerminalEffects() {
    // Add random terminal flicker effect
    const terminals = document.querySelectorAll('.terminal-body');

    terminals.forEach(terminal => {
        setInterval(() => {
            if (Math.random() > 0.95) {
                terminal.style.opacity = '0.95';
                setTimeout(() => {
                    terminal.style.opacity = '1';
                }, 50);
            }
        }, 3000);
    });
}

// ===========================
// Glitch Effect on Hover
// ===========================
function initGlitchHover() {
    const glitchElements = document.querySelectorAll('.glitch');

    glitchElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            element.style.animation = 'none';
            setTimeout(() => {
                element.style.animation = '';
            }, 10);
        });
    });
}

// ===========================
// Console Easter Egg
// ===========================
function initConsoleMessage() {
    const styles = [
        'color: #00ff41',
        'background: #0a0e17',
        'font-size: 16px',
        'font-family: monospace',
        'padding: 10px',
        'border: 1px solid #00ff41'
    ].join(';');

    console.log('%c┌──(visitor㉿portfolio)-[~]', styles);
    console.log('%c└─$ whoami', styles);
    console.log('%cLooking for CTI talent? Check out the site above!', 'color: #00d9ff; font-family: monospace;');
    console.log('%c└─$ cat contact.txt', styles);
    console.log('%cemail: zacharylanz@live.com', 'color: #a0a0a0; font-family: monospace;');
    console.log('%clinkedin: linkedin.com/in/zacharylanz', 'color: #a0a0a0; font-family: monospace;');
}

// ===========================
// Keyboard Navigation
// ===========================
function initKeyboardNav() {
    const sections = ['home', 'about', 'experience', 'portfolio', 'contact'];
    let currentSection = 0;

    document.addEventListener('keydown', (e) => {
        // Alt + Arrow keys for section navigation
        if (e.altKey && (e.key === 'ArrowDown' || e.key === 'ArrowUp')) {
            e.preventDefault();

            if (e.key === 'ArrowDown') {
                currentSection = (currentSection + 1) % sections.length;
            } else {
                currentSection = (currentSection - 1 + sections.length) % sections.length;
            }

            const target = document.getElementById(sections[currentSection]) || document.querySelector('.hero');
            const offsetTop = target.offsetTop - 70;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
}

// ===========================
// Performance Monitoring
// ===========================
function logPerformance() {
    window.addEventListener('load', () => {
        const entries = performance.getEntriesByType('navigation');
        if (entries.length > 0) {
            const pageLoadTime = Math.round(entries[0].loadEventEnd);
            console.log(`%c[PERFORMANCE] Page loaded in ${pageLoadTime}ms`, 'color: #6366f1; font-family: monospace;');
        }
    });
}

// ===========================
// Theme Toggle (Light/Dark)
// ===========================
function initThemeToggle() {
    const toggleBtn = document.getElementById('theme-toggle');
    if (!toggleBtn) return;

    // Load saved theme or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateToggleIcon(toggleBtn, savedTheme);

    toggleBtn.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme') || 'dark';
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        updateToggleIcon(toggleBtn, next);

        // Reset navbar inline styles so CSS variables take effect
        const navbar = document.querySelector('.nav-bar');
        if (navbar) {
            navbar.style.background = '';
            navbar.style.boxShadow = '';
        }
    });
}

function updateToggleIcon(btn, theme) {
    btn.textContent = theme === 'dark' ? '☀' : '☾';
    btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
}

// Apply saved theme immediately (before DOMContentLoaded) to avoid flash
(function() {
    const saved = localStorage.getItem('theme');
    if (saved) {
        document.documentElement.setAttribute('data-theme', saved);
    }
})();

// ===========================
// Back to Top Button
// ===========================
function initBackToTop() {
    const btn = document.querySelector('.back-to-top');
    if (!btn) return;

    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 400) {
            btn.classList.add('visible');
        } else {
            btn.classList.remove('visible');
        }
    });

    btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ===========================
// Initialize All Functions
// ===========================
document.addEventListener('DOMContentLoaded', () => {
    // Wrap each init in try/catch so one failure doesn't break everything
    const inits = [
        initMatrixEffect,
        initTypingEffect,
        initNavToggle,
        initSmoothScroll,
        initScrollSpy,
        initStatsAnimation,
        initGitHubFetch,
        initScrollAnimations,
        initNavbarScroll,
        initTerminalEffects,
        initGlitchHover,
        initKeyboardNav,
        initBackToTop,
        initThemeToggle,
        initConsoleMessage,
        logPerformance
    ];

    inits.forEach(fn => {
        try { fn(); } catch (e) { console.warn(`[init] ${fn.name} failed:`, e); }
    });

    // Set initial active nav link
    const firstNavLink = document.querySelector('.nav-link');
    if (firstNavLink) {
        firstNavLink.classList.add('active');
    }
});

// ===========================
// Service Worker Registration (Optional for PWA)
// ===========================
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment when you want to add PWA functionality
        // navigator.serviceWorker.register('/sw.js')
        //     .then(reg => console.log('Service Worker registered'))
        //     .catch(err => console.log('Service Worker registration failed'));
    });
}

// ===========================
// Prevent Right Click on Images (Optional)
// ===========================
// Uncomment if you want to protect your content
// document.addEventListener('contextmenu', (e) => {
//     if (e.target.tagName === 'IMG') {
//         e.preventDefault();
//     }
// });

// ===========================
// Copy Email to Clipboard
// ===========================
function initEmailCopy() {
    const emailLinks = document.querySelectorAll('a[href^="mailto:"]');

    emailLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const email = link.href.replace('mailto:', '');
            navigator.clipboard.writeText(email).then(() => {
                // Could add a toast notification here
                console.log('Email copied to clipboard!');
            }).catch(err => {
                console.error('Failed to copy email:', err);
            });
        });
    });
}

// Initialize email copy on load
document.addEventListener('DOMContentLoaded', () => {
    initEmailCopy();
});

// ===========================
// Add Active Class to Nav
// ===========================
const style = document.createElement('style');
style.textContent = `
    .nav-link.active {
        color: var(--accent-primary);
        border-color: var(--accent-primary);
    }
`;
document.head.appendChild(style);

// Base JavaScript functionality for all pages
document.addEventListener('DOMContentLoaded', function() {
    console.log('Deal Radar - Base JS loaded');
    
    // Message close functionality for alert messages
    const messageCloseButtons = document.querySelectorAll('.message-close');
    messageCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const message = this.parentElement;
            message.style.animation = 'slideOutUp 0.3s ease';
            setTimeout(() => {
                message.remove();
            }, 300);
        });
    });

    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            if (message.parentElement) {
                message.style.animation = 'slideOutUp 0.3s ease';
                setTimeout(() => {
                    if (message.parentElement) {
                        message.remove();
                    }
                }, 300);
            }
        }, 5000);
    });

    // Enhanced button hover interactions
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Smooth scroll for skip links (accessibility)
    const skipLink = document.querySelector('.sr-only-focusable');
    if (skipLink) {
        skipLink.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.focus();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    // Sticky navbar scroll effects
    const navbar = document.querySelector('.nav-bar');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add scrolled class for enhanced styling
        if (scrollTop > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // Optional: Hide navbar when scrolling down, show when scrolling up
        // Uncomment these lines if you want auto-hide behavior:
        /*
        if (scrollTop > lastScrollTop && scrollTop > 200) {
            // Scrolling down - hide navbar
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up - show navbar
            navbar.style.transform = 'translateY(0)';
        }
        */
        
        lastScrollTop = scrollTop;
    });
    
    // Smooth scroll for navigation links (anchors)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Enhanced Categories Dropdown with JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const categoriesDropdown = document.querySelector('.categories-dropdown');
    const dropdownBtn = document.querySelector('.dropdown-btn');
    const dropdownContent = document.querySelector('.dropdown-content');
    const dropdownArrow = document.querySelector('.dropdown-arrow');
    
    if (categoriesDropdown && dropdownBtn && dropdownContent) {
        let isOpen = false;
        let hoverTimeout;
        
        // Show dropdown on hover
        categoriesDropdown.addEventListener('mouseenter', function() {
            clearTimeout(hoverTimeout);
            showDropdown();
        });
        
        // Hide dropdown when leaving the entire dropdown area
        categoriesDropdown.addEventListener('mouseleave', function() {
            hoverTimeout = setTimeout(hideDropdown, 200); // Small delay
        });
        
        // Toggle on click (for mobile)
        dropdownBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (isOpen) {
                hideDropdown();
            } else {
                showDropdown();
            }
        });
        
        // Close when clicking outside
        document.addEventListener('click', function(e) {
            if (!categoriesDropdown.contains(e.target)) {
                hideDropdown();
            }
        });
        
        // Close on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && isOpen) {
                hideDropdown();
            }
        });
        
        function showDropdown() {
            dropdownContent.style.display = 'block';
            dropdownArrow.style.transform = 'rotate(180deg)';
            isOpen = true;
        }
        
        function hideDropdown() {
            dropdownContent.style.display = 'none';
            dropdownArrow.style.transform = 'rotate(0deg)';
            isOpen = false;
        }
    }
    
    // Keep existing message close functionality for messages in dropdown
    const messageCloseButtons = document.querySelectorAll('.message-close');
    messageCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });
});

// Add slide out animation for message dismissals
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutUp {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-20px);
        }
    }
`;
document.head.appendChild(style);
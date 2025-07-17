// Forms functionality for product add/edit and user profile forms
document.addEventListener('DOMContentLoaded', function() {
    console.log('Forms page loaded');
    
    // Form validation and enhancements for product forms
    const form = document.querySelector('.product-form');
    const inputs = document.querySelectorAll('.product-form input');
    
    // Enhanced input interactions (focus/blur/validation)
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentNode.style.transform = 'translateY(-2px)';
        });
        
        input.addEventListener('blur', function() {
            this.parentNode.style.transform = 'translateY(0)';
            
            // Basic validation feedback
            if (this.value.trim() === '' && this.required) {
                this.style.borderColor = '#dc3545';
            } else if (this.checkValidity()) {
                this.style.borderColor = '#28a745';
            }
        });
        
        input.addEventListener('input', function() {
            if (this.checkValidity()) {
                this.style.borderColor = '#28a745';
            } else {
                this.style.borderColor = '#667eea';
            }
        });
    });

    // Form submission animation (loading state)
    if (form) {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.style.opacity = '0.7';
            submitBtn.innerHTML = '⏳ Processing...';
        });
    }

    // URL validation for product URL input
    const urlInput = document.querySelector('input[name="url"]');
    if (urlInput) {
        urlInput.addEventListener('blur', function() {
            const url = this.value.trim();
            if (url && !isValidProductURL(url)) {
                this.style.borderColor = '#fd7e14';
                showURLHelp();
            }
        });
    }
});

// Validate if the product URL is from a supported domain
function isValidProductURL(url) {
    const validDomains = [
        'amazon.co.uk', 'amazon.com',
        'ebay.co.uk', 'ebay.com',
        'johnlewis.com',
        'argos.co.uk',
        'currys.co.uk'
    ];
    
    try {
        const urlObj = new URL(url);
        return validDomains.some(domain => urlObj.hostname.includes(domain));
    } catch {
        return false;
    }
}

// Show help message for invalid URLs (can be expanded)
function showURLHelp() {
    // Could add a dynamic help message here
}
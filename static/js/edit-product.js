// Edit product page functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Edit product page loaded');
    
    // Animation on load
    const container = document.querySelector('.edit-container');
    if (container) {
        container.style.opacity = '0';
        container.style.transform = 'translateY(30px)';
        setTimeout(() => {
            container.style.transition = 'all 0.6s ease';
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        }, 100);
    }

    // Price input enhancements
    const priceInput = document.querySelector('#desired_price');
    const currentPriceElement = document.querySelector('.current-price .price');
    
    if (priceInput && currentPriceElement) {
        const currentPrice = parseFloat(currentPriceElement.textContent.replace('£', ''));
        
        // Real-time validation and feedback
        priceInput.addEventListener('input', function() {
            const desiredPrice = parseFloat(this.value);
            
            if (desiredPrice && currentPrice) {
                if (desiredPrice >= currentPrice) {
                    this.style.borderColor = '#fd7e14';
                    showPriceWarning(desiredPrice, currentPrice);
                } else {
                    this.style.borderColor = '#28a745';
                    hidePriceWarning();
                }
            } else {
                this.style.borderColor = '#667eea';
                hidePriceWarning();
            }
        });
        
        // Format price on blur
        priceInput.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (value) {
                this.value = value.toFixed(2);
            }
        });
    }

    // Form submission enhancement
    const editForm = document.querySelector('.edit-form');
    const submitButton = document.querySelector('button[type="submit"]');
    
    if (editForm && submitButton) {
        editForm.addEventListener('submit', function() {
            submitButton.style.opacity = '0.7';
            submitButton.innerHTML = '⏳ Updating...';
            submitButton.disabled = true;
        });
    }

    // Enhanced button interactions
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            if (!this.disabled) {
                this.style.transform = 'translateY(-2px)';
            }
        });
        
        btn.addEventListener('mouseleave', function() {
            if (!this.disabled) {
                this.style.transform = 'translateY(0)';
            }
        });
    });
});

function showPriceWarning(desired, current) {
    let warning = document.querySelector('.price-warning');
    if (!warning) {
        warning = document.createElement('div');
        warning.className = 'price-warning';
        document.querySelector('.form-group').appendChild(warning);
    }
    
    warning.innerHTML = `⚠️ Your target price (£${desired.toFixed(2)}) is higher than the current price (£${current.toFixed(2)}). You'll be alerted immediately!`;
}

function hidePriceWarning() {
    const warning = document.querySelector('.price-warning');
    if (warning) {
        warning.remove();
    }
}
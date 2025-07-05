// Dashboard page functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard loaded successfully');
    
    // Initialize dashboard
    initializeDashboard();
    
    // Force stat card dimensions after page load
    setTimeout(forceStatCardDimensions, 100);
    
    // Animate stat cards on load
    animateStatCards();
});

function initializeDashboard() {
    // Handle stat card hover effects
    handleStatCardHovers();
    
    // Handle product card animations
    handleProductCardAnimations();
    
    // Handle alert form submissions
    handleAlertForms();
    
    // Handle confirmation dialogs
    handleConfirmationDialogs();
}

// Force stat card dimensions to be compact WIDTH
function forceStatCardDimensions() {
    // Force stat cards to be compact WIDTH
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(card => {
        card.style.width = '200px';
        card.style.maxWidth = '200px';
        card.style.height = '100px';
        card.style.minHeight = '100px';
        card.style.maxHeight = '100px';
        card.style.margin = '0';
        
        const cardBody = card.querySelector('.card-body');
        if (cardBody) {
            cardBody.style.padding = '0.5rem';
            cardBody.style.height = '100%';
            cardBody.style.display = 'flex';
            cardBody.style.flexDirection = 'column';
            cardBody.style.justifyContent = 'center';
            cardBody.style.alignItems = 'center';
            cardBody.style.textAlign = 'center';
        }
    });
    
    // Force stat card columns to be compact
    const statCardCols = document.querySelectorAll('.stat-card-col');
    statCardCols.forEach(col => {
        col.style.width = '200px';
        col.style.maxWidth = '200px';
        col.style.flex = '0 0 auto';
        col.style.padding = '0';
    });
    
    // Force stat cards row to use flexbox
    const statCardsRow = document.querySelector('.stat-cards-row');
    if (statCardsRow) {
        statCardsRow.style.display = 'flex';
        statCardsRow.style.flexWrap = 'wrap';
        statCardsRow.style.gap = '1rem';
    }
}

// Animate stat cards on load
function animateStatCards() {
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.5s ease';
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100);
        }, index * 200);
    });
}

// Handle stat card hover effects
function handleStatCardHovers() {
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
            this.style.boxShadow = '0 8px 20px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        });
    });
}

// Handle product card animations
function handleProductCardAnimations() {
    const productCards = document.querySelectorAll('.tracked-product-item');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 6px 20px rgba(0,0,0,0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 15px rgba(0,0,0,0.06)';
        });
    });

    // Enhanced product card interactions
    const productCards2 = document.querySelectorAll('.product');
    productCards2.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 12px 30px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 4px 15px rgba(0,0,0,0.1)';
        });
    });
}

// Handle price alert form submissions
function handleAlertForms() {
    const alertForms = document.querySelectorAll('form[action*="create_price_alert"]');
    alertForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const input = this.querySelector('input[name="target_price"]');
            if (!input.value || parseFloat(input.value) <= 0) {
                e.preventDefault();
                alert('Please enter a valid price');
                return false;
            }
        });
    });
}

// Handle confirmation dialogs
function handleConfirmationDialogs() {
    // Delete alert confirmations
    const deleteButtons = document.querySelectorAll('a[href*="delete_price_alert"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this price alert?')) {
                e.preventDefault();
                return false;
            }
        });
    });
    
    // Untrack product confirmations
    const untrackButtons = document.querySelectorAll('a[href*="remove_from_tracking"]');
    untrackButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to stop tracking this product?')) {
                e.preventDefault();
                return false;
            }
        });
    });
}

// Auto-hide success/error messages
function autoHideMessages() {
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
}

// Call auto-hide messages
autoHideMessages();
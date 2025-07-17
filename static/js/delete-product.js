// Delete product page functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Delete product page loaded');
    
    // Animation on load for delete container
    const container = document.querySelector('.delete-container');
    if (container) {
        container.style.opacity = '0';
        container.style.transform = 'translateY(30px)';
        setTimeout(() => {
            container.style.transition = 'all 0.6s ease';
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        }, 100);
    }

    // Confirmation handling for delete action
    const deleteForm = document.querySelector('.delete-form');
    const deleteButton = document.querySelector('.btn-danger');
    
    if (deleteForm && deleteButton) {
        deleteForm.addEventListener('submit', function(e) {
            // Double confirmation for safety
            const confirmed = confirm('Are you absolutely sure you want to remove this product from tracking? This action cannot be undone.');
            
            if (!confirmed) {
                e.preventDefault();
                return false;
            }
            
            // Visual feedback for loading state
            deleteButton.style.opacity = '0.7';
            deleteButton.innerHTML = '⏳ Removing...';
            deleteButton.disabled = true;
        });
    }

    // Enhanced button hover interactions
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
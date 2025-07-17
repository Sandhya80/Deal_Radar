// Product detail page functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Product detail page loaded');
    
    // Smooth scroll animations for product detail card
    const productDetail = document.querySelector('.product-detail');
    if (productDetail) {
        productDetail.style.opacity = '0';
        productDetail.style.transform = 'translateY(30px)';
        setTimeout(() => {
            productDetail.style.transition = 'all 0.6s ease';
            productDetail.style.opacity = '1';
            productDetail.style.transform = 'translateY(0)';
        }, 100);
    }

    // Tracking button interactions (visual feedback on click)
    const trackingButtons = document.querySelectorAll('.tracking-section .btn');
    trackingButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Add loading state
            this.style.opacity = '0.7';
            this.style.transform = 'scale(0.95)';
            
            // If it's a tracking action, show confirmation
            if (this.textContent.includes('Track')) {
                setTimeout(() => {
                    this.style.opacity = '1';
                    this.style.transform = 'scale(1)';
                }, 200);
            }
        });
    });

    // Price highlight animation on hover
    const price = document.querySelector('.product-price');
    if (price) {
        price.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.textShadow = '3px 3px 6px rgba(0,0,0,0.2)';
        });
        
        price.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.textShadow = '2px 2px 4px rgba(0,0,0,0.1)';
        });
    }
});
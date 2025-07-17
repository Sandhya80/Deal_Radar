// Authentication forms functionality (login/signup)
document.addEventListener('DOMContentLoaded', function() {
    console.log('Auth page loaded');
    
    // Form validation feedback for auth forms
    const inputs = document.querySelectorAll('.form-group input');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                this.style.borderColor = '#dc3545';
            } else {
                this.style.borderColor = '#28a745';
            }
        });
        
        input.addEventListener('focus', function() {
            this.style.borderColor = '#667eea';
        });
    });

    // Password strength indicator for signup form
    const passwordField = document.querySelector('input[name="password1"]');
    if (passwordField) {
        passwordField.addEventListener('input', function() {
            const password = this.value;
            const strength = getPasswordStrength(password);
            
            // Remove existing strength indicator
            const existing = document.querySelector('.password-strength');
            if (existing) existing.remove();
            
            // Add strength indicator below password field
            const indicator = document.createElement('div');
            indicator.className = 'password-strength';
            indicator.style.marginTop = '5px';
            indicator.style.fontSize = '12px';
            indicator.style.fontWeight = 'bold';
            
            if (password.length > 0) {
                indicator.textContent = `Password strength: ${strength.text}`;
                indicator.style.color = strength.color;
                this.parentNode.appendChild(indicator);
            }
        });
    }

    // Form submission animation (loading state)
    const authForm = document.querySelector('.auth-form form');
    if (authForm) {
        authForm.addEventListener('submit', function() {
            const button = this.querySelector('.auth-btn');
            button.style.opacity = '0.7';
            button.textContent = 'Processing...';
        });
    }
});

// Password strength checker for signup
function getPasswordStrength(password) {
    let score = 0;
    if (password.length >= 8) score++;
    if (/[a-z]/.test(password)) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;
    
    switch (score) {
        case 0:
        case 1: 
            return { text: 'Very Weak', color: '#dc3545' };
        case 2: 
            return { text: 'Weak', color: '#fd7e14' };
        case 3: 
            return { text: 'Fair', color: '#ffc107' };
        case 4: 
            return { text: 'Good', color: '#20c997' };
        case 5: 
            return { text: 'Strong', color: '#28a745' };
        default: 
            return { text: 'Weak', color: '#dc3545' };
    }
}
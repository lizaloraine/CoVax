document.addEventListener('DOMContentLoaded', function() {
    // Password visibility toggle
    document.querySelectorAll('.toggle-password').forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            const input = this.previousElementSibling;
            if (input.type === 'password') {
                input.type = 'text';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            }
        });
    });

    // Form validation
    const form = document.getElementById('registrationForm');
    form.addEventListener('submit', function(e) {
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
        const license = document.getElementById('license').value;

        // Only validate password match and license format
        if (password !== confirmPassword) {
            e.preventDefault();
            showError('Passwords do not match');
            return;
        }

        // License format validation
        if (!/^\d{4}-\d{4}$/.test(license)) {
            e.preventDefault();
            showError('Please enter a valid license number (Format: XXXX-XXXX)');
            return;
        }
    });

    function showError(message) {
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        const error = document.createElement('div');
        error.className = 'error-message';
        error.textContent = message;
        form.insertBefore(error, form.firstChild);
    }
});

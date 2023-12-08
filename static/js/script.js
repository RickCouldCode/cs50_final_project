document.addEventListener('DOMContentLoaded', function() {
    var registrationForm = document.getElementById('registration-form');
    if (registrationForm) {
        registrationForm.addEventListener('submit', function(event) {
            var username = document.getElementById('username').value;
            var email = document.getElementById('email').value;
            var password = document.getElementById('password').value;
            var confirmPassword = document.getElementById('confirm-password').value;

            if (username.length < 3) {
                alert('Username must be at least 3 characters long.');
                event.preventDefault();
            }

            if (!email.includes('@')) {
                alert('Please enter a valid email address.');
                event.preventDefault();
            }

            if (password !== confirmPassword) {
                alert('Passwords do not match.');
                event.preventDefault();
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            var email = document.getElementById('email').value;

            if (!email.includes('@')) {
                alert('Please enter a valid email address.');
                event.preventDefault();
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var navLinks = document.querySelectorAll('nav ul li a');
    var currentLocation = window.location.pathname;

    navLinks.forEach(function(link) {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active-link');
        }
    });
});
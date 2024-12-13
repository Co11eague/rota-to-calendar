// Wait for the DOM to be loaded

document.addEventListener('DOMContentLoaded', function () {

    if (typeof bootstrap !== 'undefined' && bootstrap.Toast) {
        console.log('Bootstrap is loaded. Initializing Toasts.');

        var toasts = document.querySelectorAll('.toast');
        toasts.forEach(function (toast) {
            // Initialize and show the toast
            var toastInstance = new bootstrap.Toast(toast);
            toastInstance.show();
        });
    } else {
        console.log('Bootstrap JS not found. Dynamically loading it.');
        var script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js';
        document.body.appendChild(script);

        script.onload = function () {
            console.log('Bootstrap dynamically loaded. Initializing Toasts.');

            var toasts = document.querySelectorAll('.toast');
            toasts.forEach(function (toast) {
                var toastInstance = new bootstrap.Toast(toast);
                toastInstance.show();
            });
        };

        script.onerror = function () {
            console.error('Failed to load Bootstrap JS.');
        };
    }
});


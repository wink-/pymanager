// Get CSRF token from meta tag
function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Add CSRF token to all AJAX requests
document.addEventListener('DOMContentLoaded', function() {
    // Add CSRF token to all fetch requests
    const originalFetch = window.fetch;
    window.fetch = function(url, options = {}) {
        options.headers = options.headers || {};
        options.headers['X-CSRF-TOKEN'] = getCsrfToken();
        return originalFetch(url, options);
    };

    // Add CSRF token to all axios requests
    if (window.axios) {
        axios.interceptors.request.use(function(config) {
            config.headers['X-CSRF-TOKEN'] = getCsrfToken();
            return config;
        });
    }

    // Add CSRF token to all jQuery AJAX requests
    if (window.jQuery) {
        $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': getCsrfToken()
            }
        });
    }
});

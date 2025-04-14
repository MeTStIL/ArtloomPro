(function() {
    const token = localStorage.getItem('access_token');
    const expiresAt = localStorage.getItem('expires_at');

    if (!token) {
        window.location.href = '/login';
    }
    else if (expiresAt && Date.now() > Number(expiresAt)) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('expires_at');
        window.location.href = '/login';
    }
})();

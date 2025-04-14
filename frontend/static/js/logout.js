function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('expires_at');
    window.location.href = '/login';
}

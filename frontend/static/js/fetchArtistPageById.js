import { apiBaseUrl } from './apiConfig.js';

export async function fetchArtistPageById(artistPageId) {
    try {
        const token = localStorage.getItem('access_token');

        const response = await fetch(`${apiBaseUrl}/artist-pages/${artistPageId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Ошибка при выполнении запроса:", error);
        return null;
    }
}

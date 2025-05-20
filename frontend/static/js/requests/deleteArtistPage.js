import { apiBaseUrl } from '../utils/apiBaseUrl.js';

export async function deleteArtistPage () {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${apiBaseUrl}/artist_pages/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

    } catch (error) {
        console.log(`Ошибка при удалении страницы: ${error}`);
        throw error;
    }
}
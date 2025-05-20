import {apiBaseUrl} from '../utils/apiBaseUrl.js';

export async function fetchArtistPageByLogin(login) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${apiBaseUrl}/artist-pages/by_login/${login}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        return await response.json();

    } catch (error) {
        console.log(`Ошибка ${error}`);
        throw error;
    }
}
import { apiBaseUrl } from './apiConfig.js';

export async function subscribe(login, artistId)
{
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${apiBaseUrl}/subscribe/${artistId}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })

    } catch (error) {
        console.log(`Ошибка при попытке подписаться: ${error}`)
    }
}
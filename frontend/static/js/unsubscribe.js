import { apiBaseUrl } from './apiConfig.js';

export async function unsubscribe(login, artistId)
{
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${apiBaseUrl}/unsubscribe/${artistId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })

    } catch (error) {
        console.log(`Ошибка при попытке подписаться: ${error}`)
    }
}
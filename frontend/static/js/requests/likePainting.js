import { apiBaseUrl } from '../utils/apiBaseUrl.js';

export async function likePainting(login, paintingId)
{
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${apiBaseUrl}/set_like/${paintingId}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
    } catch (error) {
        console.log(`Ошибка при попытке подписаться: ${error}`)
    }
}
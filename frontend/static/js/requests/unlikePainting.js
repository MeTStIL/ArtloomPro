import { apiBaseUrl } from '../utils/apiBaseUrl.js';

export async function unlikePainting(login, paintingId)
{
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${apiBaseUrl}/delete_like/${paintingId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
    } catch (error) {
        console.log(`Ошибка при попытке подписаться: ${error}`)
    }
}
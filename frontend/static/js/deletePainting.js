import { apiBaseUrl } from './apiConfig.js';

export async function deletePainting(paintingId){
    try {
        const token = localStorage.getItem('access_token');

        const response = await fetch(`${apiBaseUrl}/paintings/${paintingId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        const data = await response.json();
    } catch (error) {
        console.error("Ошибка при выполнении запроса:", error);
        throw error;
    }
}
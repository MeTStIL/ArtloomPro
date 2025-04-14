import { apiBaseUrl } from './apiConfig.js';

export async function patchPainting(paintingId, newDescription, imgPath){
    try {
        const token = localStorage.getItem('access_token');

        const body = {
            'description': newDescription,
            'img_path': imgPath,
        };

        const response = await fetch(`${apiBaseUrl}/paintings/${paintingId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(body)
        });
        const data = await response.json();
    } catch (error) {
        console.error("Ошибка при выполнении запроса:", error);
        throw error;
    }
}
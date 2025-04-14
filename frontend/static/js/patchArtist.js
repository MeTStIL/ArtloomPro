import { apiBaseUrl } from './apiConfig.js';

export async function patchArtist(name, imgPath, description) {
    try {
        const token = localStorage.getItem('access_token');

        const body = {
            'name': name,
            'img_path': imgPath,
            'description': description,
        }

        console.log(JSON.stringify(body))

        const response = await fetch(`${apiBaseUrl}/artists`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(body)
        });
        const data = await response.json();

    } catch (error) {
        console.log(`Ошибка при обновлении данных: ${error}`);
        throw error;
    }
}
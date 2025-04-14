import { apiBaseUrl } from './apiConfig.js';

export async function createArtistPage(name, description, img_path='https://avatars.mds.yandex.net/get-mpic/11408907/2a0000018b43910fcb397141d550aaf4bb2a/orig') {
    try {
        const token = localStorage.getItem('access_token');

        const response = await fetch(`${apiBaseUrl}/artists`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                name: name,
                img_path: img_path,
                description: description
            })
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

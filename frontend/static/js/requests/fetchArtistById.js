import { apiBaseUrl } from '../utils/apiBaseUrl.js';

export async function fetchArtistById(artistId) {
    try {
        const response = await fetch(`${apiBaseUrl}/artists/${artistId}`);
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

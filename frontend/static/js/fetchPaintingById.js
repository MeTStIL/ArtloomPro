import { apiBaseUrl } from './apiConfig.js';

export async function fetchPaintingById(paintingId) {
    try {
        const response = await fetch(`${apiBaseUrl}/paintings/${paintingId}`);
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

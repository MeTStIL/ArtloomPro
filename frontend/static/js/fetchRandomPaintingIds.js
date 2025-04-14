import {apiBaseUrl} from "./apiConfig.js";

/**
 * Получает случайные ID картин с сервера
 * @param {number} limit - количество случайных картин
 * @returns {Promise<number[]>} - массив id картин
 */
export async function fetchRandomPaintingIds(limit) {
    try {
        const response = await fetch(`${apiBaseUrl}/random-paintings/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ limit: limit })
        });

        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status} ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Ошибка при получении id случайных картин:', error);
        return [];
    }
}

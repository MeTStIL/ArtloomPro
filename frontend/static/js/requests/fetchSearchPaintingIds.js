import { apiBaseUrl } from "../utils/apiBaseUrl.js";

export async function fetchSearchPaintingIds(text, limit) {
    try {
        const response = await fetch(`${apiBaseUrl}/search-paintings/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text, limit: limit })
        });

        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Ошибка при поиске картин:', error);
        return [];
    }
}

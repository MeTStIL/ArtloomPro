export async function fetchPaintingById(paintingId) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/paintings/${paintingId}`);
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

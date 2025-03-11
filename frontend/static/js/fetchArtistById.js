export async function fetchArtistById(artistId) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/artists/${artistId}`);
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

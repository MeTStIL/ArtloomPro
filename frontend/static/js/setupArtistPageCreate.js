import { apiBaseUrl } from './apiConfig.js';
import { createArtistPage } from './createArtistPage.js';


export async function setupArtistPageCreate(login) {
    const popup = document.getElementById('add-page-popup');
    const form = document.getElementById('popup-form');

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

            const name = document.getElementById('popup-title').value;
            const description = document.getElementById('popup-desc').value;

        try {
            popup.style.display = 'none';
            await createArtistPage(name, description);
            window.location.href = `/${login}`;

        } catch (error) {
            popup.style.display = 'none';
            console.error("Ошибка в процессе создания артиста:", error);
        }
    })
}


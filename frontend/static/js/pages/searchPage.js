import { fetchCurrentAccount } from "../requests/fetchCurrentAccount.js";
import { fetchRandomPaintingIds } from "../requests/fetchRandomPaintingIds.js";
import { fetchSearchPaintingIds } from "../requests/fetchSearchPaintingIds.js";
import { setupArtistGallery } from "../setup/setupArtistGallery.js";
import { setupNavMenuButton } from "../utils/navMenuUtils.js";

const RANDOM_PAINTINGS_LIMIT = 9;
const SEARCH_PAINTINGS_LIMIT = RANDOM_PAINTINGS_LIMIT;


async function loadRandomPaintings() {
    const paintingIds = await fetchRandomPaintingIds(RANDOM_PAINTINGS_LIMIT);
    const gallery = document.getElementById('gallery');
    const me = await fetchCurrentAccount();

    await setupNavMenuButton(me);
    await setupArtistGallery(gallery, paintingIds, true, me);
}

async function performSearch(queryText) {
    const paintingIds = await fetchSearchPaintingIds(queryText, SEARCH_PAINTINGS_LIMIT);
    const gallery = document.getElementById('gallery');
    const me = await fetchCurrentAccount();

    gallery.innerHTML = '';

    if (!queryText.trim()) {
        await loadRandomPaintings();
        return;
    }

    await setupArtistGallery(gallery, paintingIds, true, me);
}


async function setupSearch() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');

    searchButton.addEventListener('click', async () => {
        const queryText = searchInput.value;
        await performSearch(queryText);
    });

    searchInput.addEventListener('keydown', async (event) => {
        if (event.key === 'Enter') {
            const queryText = searchInput.value;
            await performSearch(queryText);
        }
    });
}

document.addEventListener("DOMContentLoaded", async () => {
    await setupSearch();
    await loadRandomPaintings();
});
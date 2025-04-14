import { fetchPaintingById } from "./fetchPaintingById.js";
import { getScrollbarWidth } from "./getScrollbarWidth.js";
import { fetchCurrentAccount } from "./fetchCurrentAccount.js";
import { fetchRandomPaintingIds } from "./fetchRandomPaintingIds.js";
import { fetchSearchPaintingIds } from "./fetchSearchPaintingIds.js";

const RANDOM_PAINTINGS_LIMIT = 6;
const SEARCH_PAINTINGS_LIMIT = RANDOM_PAINTINGS_LIMIT;

async function loadRandomPaintings() {
    const gallery = document.getElementById('gallery');
    // Очищаем галерею
    gallery.innerHTML = '';

    const me = await fetchCurrentAccount();
    if (me) {
        document.getElementById('pc-username').innerHTML =
            `<a href="/accounts/${me.login}">${me.login}</a>`;
        document.getElementById('mobile-username').innerHTML =
            `<a href="/accounts/${me.login}">${me.login}</a>`;
    }

    const paintingIds = await fetchRandomPaintingIds(RANDOM_PAINTINGS_LIMIT);

    for (const paintingId of paintingIds) {
        try {
            const paintingInfo = await fetchPaintingById(paintingId);
            gallery.innerHTML += `
                <div class="photo no-select">
                    <img src="${paintingInfo.img_path}" data-description="${paintingInfo.description}">
                </div>`;
        } catch (error) {
            console.error(`Ошибка при загрузке картины с id ${paintingId}:`, error);
        }
    }

    setupGalleryInteraction();
}

async function performSearch(queryText) {
    const gallery = document.getElementById('gallery');
    // Очищаем галерею для вывода результатов поиска
    gallery.innerHTML = '';

    // Если строка пустая – показываем случайные картины
    if (!queryText.trim()) {
        loadRandomPaintings();
        return;
    }

    const paintingIds = await fetchSearchPaintingIds(queryText, SEARCH_PAINTINGS_LIMIT);

    for (const paintingId of paintingIds) {
        try {
            const paintingInfo = await fetchPaintingById(paintingId);
            gallery.innerHTML += `
                <div class="photo no-select">
                    <img src="${paintingInfo.img_path}" data-description="${paintingInfo.description}">
                </div>`;
        } catch (error) {
            console.error(`Ошибка при загрузке картины с id ${paintingId}:`, error);
        }
    }
    setupGalleryInteraction();
}

function setupGalleryInteraction() {
    const photos = document.querySelectorAll('.photo img');
    const overlay = document.getElementById('overlay');
    const fullImage = document.getElementById('fullImage');
    const imageDescription = document.getElementById('imageDescription');

    photos.forEach(photo => {
        photo.addEventListener('click', function () {
            const scrollbarWidth = getScrollbarWidth();
            const description = this.getAttribute('data-description');

            fullImage.src = this.src;
            imageDescription.textContent = description;
            overlay.classList.add('active');
            document.body.classList.add('no-scroll');
            document.body.style.paddingRight = `${scrollbarWidth}px`;
        });
    });

    overlay.addEventListener('click', function () {
        overlay.classList.remove('active');
        document.body.classList.remove('no-scroll');
        document.body.style.paddingRight = '';
        setTimeout(() => fullImage.src = '', 150);
    });
}

// Добавляем обработчики события для строки поиска
function setupSearch() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');

    searchButton.addEventListener('click', () => {
        const queryText = searchInput.value;
        performSearch(queryText);
    });

    // Можно сделать поиск при нажатии Enter
    searchInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            const queryText = searchInput.value;
            performSearch(queryText);
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    setupSearch();
    loadRandomPaintings();
});

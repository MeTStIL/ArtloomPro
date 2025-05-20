import { fetchArtistById } from "../requests/fetchArtistById.js";
import { fetchCurrentAccount } from "../requests/fetchCurrentAccount.js";
import { fetchArtistPageByLogin } from "../requests/fetchArtistPageByLogin.js";
import { setupArtistGallery } from "../setup/setupArtistGallery.js";
import { setupNavMenuButton } from "../utils/navMenuUtils.js";
import { setupArtistMenuButtons } from "../setup/setupArtistMenuButtons.js";
import { setupArtisDescription } from "../setup/setupArtistDescription.js";

async function fetchDataArtistPage(login) {

    const artistPage = await fetchArtistPageByLogin(login);
    const artist = await fetchArtistById(artistPage.artist_id);
    const me = await fetchCurrentAccount();

    const gallery = document.getElementById('gallery');
    const mainPicture = document.getElementById('main-picture');

    if (artistPage.is_owner) {
        document.getElementById('editor').style = 'display:block';
        document.getElementById('editor').href = `/editor/${login}`;

        const editorOpenBtn = document.getElementById('editor-open');
        document.getElementById('editor-open').style = 'display:flex';
        editorOpenBtn.addEventListener('click', () => {
            location.href = `/editor/${login}`;
        });
    }

    if (artist) {
        document.getElementById('author-name').textContent = artist.name;
        mainPicture.style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.5)), url(${artist.img_path})`;

        await setupNavMenuButton(me);
        await setupArtistMenuButtons(me, artistPage.artist_id, artist.subscribers_count)
        await setupArtisDescription(artist.description);
        await setupArtistGallery(gallery, artistPage.painting_ids, false, me);
    }
}


document.addEventListener("DOMContentLoaded", async () => {
    const path = window.location.pathname;
    const login = path.split("/").pop()

    await fetchDataArtistPage(login);
});

import {fetchArtistById} from "../requests/fetchArtistById.js";
import {setupPostPainting} from "../setup/setupPostPainting.js";
import {fetchCurrentAccount} from "../requests/fetchCurrentAccount.js";
import {fetchArtistPageByLogin} from "../requests/fetchArtistPageByLogin.js";
import {deleteArtistPage} from "../requests/deleteArtistPage.js";
import {setupPopup} from "../setup/setupPopup.js";
import {setupNavMenuButton} from "../utils/navMenuUtils.js";
import {setupPostBackground} from "../setup/setupPostBackground.js";
import {setupPostDescriprion} from "../setup/setupPostDescriprion.js";
import {setupPostArtistName} from "../setup/setupPostArtistName.js";
import {setupArtistEditorGallery} from "../setup/setupArtistEditorGallery.js";
import {setupArtisDescription} from "../setup/setupArtistDescription.js";
import {setupArtistMenuButtons} from "../setup/setupArtistMenuButtons.js";
import {setupAlert} from "../setup/setupAlert.js";

async function fetchDataArtistPage(login) {
    try {
        const artistPage = await fetchArtistPageByLogin(login);
        const artist = await fetchArtistById(artistPage.artist_id);
        const me = await fetchCurrentAccount();

        const gallery = document.getElementById('gallery');
        const mainPicture = document.getElementById('main-picture');

        if (artistPage.is_owner) {
            document.getElementById('editor').style = 'display:block';
            document.getElementById('editor').href = `../${login}`;

            const exitEditorBtn = document.getElementById('editor-exit');
            exitEditorBtn.addEventListener('click', () => {
                location.href = `/${login}`;
            });
        }

        if (artist) {
            document.getElementById('author-name').textContent = artist.name;
            mainPicture.style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.5)), url(${artist.img_path})`;

            await setupNavMenuButton(me);
            await setupArtistMenuButtons(me, artistPage.artist_id, artist.subscribers_count)
            await setupArtisDescription(artist.description);
            await setupArtistEditorGallery(gallery, artistPage.painting_ids, false);
        }


        const addPhotoButton = document.getElementById('addPhotoButton');
        const addPhotoPopup = document.getElementById('add-photo-popup');
        await setupPopup(addPhotoButton, addPhotoPopup);
        await setupPostPainting(artistPage.artist_id);


        const deleteArtistPageButton = document.getElementById('delete-artist-page-btn');
        if (deleteArtistPageButton) {
            deleteArtistPageButton.addEventListener('click', async () => {
                if (confirm('Вы точно хотите удалить свою страницу?')) {
                    await deleteArtistPage();
                    window.location.href = `/accounts/${login}`;
                }
            })
        }

        const descriptionArea = document.getElementById('new-description');
        descriptionArea.innerHTML = artist.description;

        const changeDescriptionButton = document.getElementById('change-description-btn');
        const changeDescriptionPopup = document.getElementById('change-description-popup');
        await setupPopup(changeDescriptionButton, changeDescriptionPopup);
        await setupPostDescriprion(artist);


        const changeBackgroundButton = document.getElementById('change-background-btn');
        const changeBackgroundPopup = document.getElementById('change-background-popup');
        await setupPopup(changeBackgroundButton, changeBackgroundPopup);
        await setupPostBackground(artist);


        const changeAuthorNameButton = document.getElementById('change-author-name-btn');
        const changeAuthorNamePopup = document.getElementById('change-author-name-popup');
        await setupPopup(changeAuthorNameButton, changeAuthorNamePopup);
        await setupPostArtistName(artist);

    } catch (error) {
        console.error("Ошибка при выполнении запроса:", error);
        window.handleScriptError(error);
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    const path = window.location.pathname;
    const login = path.split("/").pop();

    await fetchDataArtistPage(login);
});

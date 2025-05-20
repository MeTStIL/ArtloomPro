import { fetchArtistById } from "../requests/fetchArtistById.js";
import { setupArtistPageCreate } from "../setup/setupArtistPageCreate.js";
import { fetchCurrentAccount } from "../requests/fetchCurrentAccount.js";
import { fetchAccountPageByLogin } from "../requests/fetchAccountPageByLogin.js";
import { setupArtistGallery } from "../setup/setupArtistGallery.js";
import { setupNavMenuButton } from "../utils/navMenuUtils.js";
import { setupPopup } from "../setup/setupPopup.js";

async function fetchDataAccountPage(login) {
    const data = await fetchAccountPageByLogin(login);
    const me = await fetchCurrentAccount();

    const gallery = document.getElementById('gallery');

    const avatar = document.getElementById('avatar');
    const image = document.createElement('img');
    image.src = data.avatar_img_path;
    avatar.appendChild(image);

    if (me && me.login === data.login) {
        if (me.artist_id) {
            await showBlockAndRedirect('my-page', me.login);
        } else {
            const artistButton = document.getElementById('artist-page-button');
            if (artistButton) {
                artistButton.style.display = 'flex';
            }
        }
    } else {
        if (data.artist_id) {
            await showBlockAndRedirect('not-my-page', data.login);
        }
    }

    const createPageButton = document.querySelector('.add-button');
    const createPagePopup = document.getElementById('add-page-popup');
    await setupPopup(createPageButton, createPagePopup);

    await setupNavMenuButton(me);
    await setupSubscribtions(data.subscribed_artist_ids);
    await setupArtistPageCreate(login);
    await setupArtistGallery(gallery, data.liked_paintings_ids, true, me);

    const toMain = document.getElementById('to-main');
    toMain.addEventListener('click', () => {
        window.location.href = '/';
    });
}

async function setupSubscribtions(subscribed_artist_ids) {
    const artists = document.getElementById('authors');

    for (const artistId of subscribed_artist_ids) {
        const artistInfo = await fetchArtistById(artistId);

        const tooltip = document.createElement('div');
        tooltip.classList.add('tooltip');

        const artist = document.createElement('a');
        artist.classList.add('author-photo');
        artist.classList.add('no-select');
        artist.href = artistInfo.artist_page_url;

        const tooltiptext = document.createElement('span');
        tooltiptext.classList.add('tooltiptext');
        tooltiptext.textContent = artistInfo.name;

        const image = document.createElement('img');
        image.src = artistInfo.img_path;

        tooltip.appendChild(image);
        tooltip.appendChild(tooltiptext);

        artist.appendChild(tooltip);
        artists.appendChild(artist);
    }
}

async function showBlockAndRedirect(elementId, login) {
    const element = document.getElementById(elementId);
    if (!element) return;

    element.style.display = 'flex';
    element.addEventListener('click', () => {
        window.location.href = `/${login}`;
    });
}

document.addEventListener("DOMContentLoaded", async () => {
    const path = window.location.pathname;
    const login = path.split("/").pop();

    await fetchDataAccountPage(login);
});

import { patchArtist } from "../requests/patchArtist.js";

export async function setupPostArtistName(artistInfo) {
    const newName = document.getElementById('new-author-name');
    const name = document.getElementById('author-name');
    newName.placeholder = artistInfo.name;
    newName.value = artistInfo.name;

    const form = document.getElementById('change-author-name-form');
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        // overlay_l.style.display = 'block';
        // loader.style.display = 'block';

        name.innerText = newName.value;
        await patchArtist(newName.value, artistInfo.img_path, artistInfo.description)

        // loader.style.display = 'none';
        // overlay_l.style.display = 'none';
        // content.style.display = 'block';
    });
}
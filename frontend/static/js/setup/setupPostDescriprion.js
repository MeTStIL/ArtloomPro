import { patchArtist } from "../requests/patchArtist.js";

export async function setupPostDescriprion(artist) {
    const form = document.getElementById('change-description-form');
    const description = document.getElementById('artist-description');
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        // overlay_l.style.display = 'block';
        // loader.style.display = 'block';

        const newDescription = document.getElementById('new-description');
        description.textContent = newDescription.value;
        await patchArtist(artist.name, artist.img_path, newDescription.value)


        // loader.style.display = 'none';
        // overlay_l.style.display = 'none';
        // content.style.display = 'block';
    });
}
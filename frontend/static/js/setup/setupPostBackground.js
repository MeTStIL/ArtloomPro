import {paintingUploadToYC} from "./setupPostPainting.js";
import {patchArtist} from "../requests/patchArtist.js";
import {setupAlert} from "../setup/setupAlert.js";

export async function setupPostBackground(artistInfo) {
    const form = document.getElementById('change-background-form');
    const background = document.getElementById('main-picture');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const files = document.getElementById('new-background').files;

        if (files.length === 0) {
            await setupAlert("Выберите файл для заднего фона");
            return;
        }

        const newBackground = {
            photo: files[0]
        };

        // overlay_l.style.display = 'block';
        // loader.style.display = 'block';

        const newImgPath = await paintingUploadToYC(newBackground);
        background.style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.5)), url(${newImgPath.img_url})`;
        await patchArtist(artistInfo.name, newImgPath.img_url, artistInfo.description);
        // loader.style.display = 'none';
        // overlay_l.style.display = 'none';
        // content.style.display = 'block';
    });

}
import {fetchPaintingById} from "../requests/fetchPaintingById.js";
import {removeOverlay, setOverlay} from "../utils/overlayUtils.js";
import {deletePainting} from "../requests/deletePainting.js";
import {setupPopup} from "./setupPopup.js";
import {patchPainting} from "../requests/patchPainting.js";

let currentPainting = null;
let currentImageElement = null;

export async function setupArtistEditorGallery(gallery, paintingIds) {
    const overlay = document.getElementById('overlay');
    const nav = document.querySelector('.nav');
    const fullImage = document.getElementById('fullImage');

    overlay.addEventListener('click', () => clickOnOverlay(overlay, fullImage, nav));

    const form = document.getElementById('change-painting-describe-form');
    const newDescriptionInput = document.getElementById('new-painting-describe');


    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!currentPainting || !currentImageElement) return;

        const newDescription = newDescriptionInput.value;
        await patchPainting(currentPainting.id, newDescription, currentPainting.img_path);

        currentImageElement.setAttribute('data-description', newDescription);
        currentPainting.description = newDescription;
    });

    for (const paintingId of paintingIds) {

        const node = await createNode(paintingId);

        gallery.appendChild(node);

        await new Promise(resolve => {
            setTimeout(() => {
                node.classList.add('showItem');
                resolve();
            }, 50);
        });
    }
}

export async function createNode(paintingId) {
    const overlay = document.getElementById('overlay');
    const nav = document.querySelector('.nav');
    const fullImage = document.getElementById('fullImage');
    const imageDescription = document.getElementById('imageDescription');
    const changePaintingDescriptionPopup = document.getElementById('change-painting-describe-popup');
    const newDescriptionInput = document.getElementById('new-painting-describe');

    const paintingInfo = await fetchPaintingById(paintingId);

    const node = document.createElement('div');
    node.classList.add('photo', 'no-select');

    const image = document.createElement('img');
    image.classList.add('photo-item');
    image.src = paintingInfo.img_path;
    image.setAttribute('data-description', paintingInfo.description);

    image.addEventListener('click', () => clickOnImage(image, fullImage, imageDescription, overlay, nav));

    const deleteButton = document.createElement('button');
    deleteButton.classList.add('delete-photo-btn');

    const deleteButtonImg = document.createElement('img');
    deleteButtonImg.src = '../static/root/trash.svg';

    deleteButton.appendChild(deleteButtonImg);
    deleteButton.addEventListener('click', async () => {
        node.remove();
        await deletePainting(paintingInfo.id);
    });

    const changeButton = document.createElement('button');
    changeButton.classList.add('change-painting-describe-btn');

    const changeButtonImg = document.createElement('img');
    changeButtonImg.src = '../static/root/blackchange2.svg';

    changeButton.appendChild(changeButtonImg);
    await setupPopup(changeButton, changePaintingDescriptionPopup);

    changeButton.addEventListener('click', () => {
        currentPainting = paintingInfo;
        currentImageElement = image;
        newDescriptionInput.value = paintingInfo.description;
    });

    node.appendChild(image);
    node.appendChild(deleteButton);
    node.appendChild(changeButton);

    return node;
}

export function clickOnImage(image, fullImage, imageDescription, overlay, nav) {
    const description = image.getAttribute('data-description');
    fullImage.src = image.src;
    imageDescription.textContent = description;
    setOverlay(overlay, document.body, nav, fullImage);
}

function clickOnOverlay(overlay, fullImage, nav) {
    removeOverlay(overlay, document.body, nav, fullImage);
    setTimeout(() => fullImage.src = '', 150);
}
import { fetchPaintingById } from "../requests/fetchPaintingById.js";
import { unlikePainting } from "../requests/unlikePainting.js";
import { likePainting } from "../requests/likePainting.js";
import { removeOverlay, setOverlay } from "../utils/overlayUtils.js";
import {fetchArtistById} from "../requests/fetchArtistById.js";
import {fetchArtistPageById} from "../requests/fetchArtistPageById.js";

export async function setupArtistGallery(gallery, paintingIds, toAuthor = false, me = null) {

    const overlay = document.getElementById('overlay');
    const nav = document.querySelector('.nav');
    const fullImage = document.getElementById('fullImage');
    const imageDescription = document.getElementById('imageDescription');

    overlay.addEventListener('click', () => clickOnOverlay(overlay, fullImage, nav))

    for (const paintingId of paintingIds) {
        const paintingInfo = await fetchPaintingById(paintingId);

        const node = document.createElement('div');
        node.classList.add('photo');
        node.classList.add('no-select');

        const image = document.createElement('img');
        image.classList.add('photo-item');
        image.src = paintingInfo.img_path;
        image.setAttribute('data-description', paintingInfo.description);

        image.addEventListener('click', () => clickOnImage(image, fullImage, imageDescription, overlay, nav));

        const button = document.createElement('button');
        const isLiked = me?.liked_paintings_ids?.includes(paintingInfo.id);
        button.id = paintingInfo.id;
        button.classList.add('like-painting-btn');
        if (isLiked) {
            button.classList.add('liked');
        }

        button.addEventListener('click', async () => await clickOnLike(button, me));

        const likesCount = document.createElement('p');
        likesCount.textContent = paintingInfo.likes_count;

        const like = document.createElement('img');
        like.src = '../static/root/nolike.svg';

        button.appendChild(likesCount);
        button.appendChild(like);

        node.appendChild(image);
        node.appendChild(button);

        if (toAuthor) {
            const authorButton = document.createElement('button');
            authorButton.classList.add('author-link');

            const authorButtonA = document.createElement('a');
            authorButtonA.href =  paintingInfo.artist_page_url;
            authorButtonA.textContent = 'К автору'

            authorButton.appendChild(authorButtonA);
            node.appendChild(authorButton);
        }

        gallery.appendChild(node);

        await new Promise(resolve => {
            setTimeout(() => {
                node.classList.add('showItem');
                resolve();
            }, 50);
        });
    }
}

async function clickOnLike(button, me) {
    if (!me) {
        return;
    }

    if (button.classList.contains('liked')) {
        button.classList.remove('liked');
        button.firstChild.innerText = Number(button.firstChild.innerText) - 1;
        await unlikePainting(me.login, button.id);
    } else {
        button.classList.add('liked');
        button.firstChild.innerText = Number(button.firstChild.innerText) + 1;
        await likePainting(me.login, button.id);
    }
}

function clickOnImage(image, fullImage, imageDescription, overlay, nav) {
    const description = image.getAttribute('data-description');
    fullImage.src = image.src;
    imageDescription.textContent = description;
    setOverlay(overlay, document.body, nav, fullImage);
}

function clickOnOverlay(overlay, fullImage, nav) {
    removeOverlay(overlay, document.body, nav, fullImage);
    setTimeout(() => fullImage.src = '', 150);
}

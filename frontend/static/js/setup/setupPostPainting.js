import {fetchPaintingById} from "../requests/fetchPaintingById.js";
import {apiBaseUrl} from '../utils/apiBaseUrl.js';
import {deletePainting} from "../requests/deletePainting.js";
import {setupPopup} from "./setupPopup.js";
import {patchPainting} from "../requests/patchPainting.js";
import {clickOnImage, createNode} from "./setupArtistEditorGallery.js";
import {setupAlert} from "./setupAlert.js";

export async function setupPostPainting(accountPageId) {
    const popup = document.getElementById('add-photo-popup');
    const form = document.getElementById('popup-form');
    const gallery = document.getElementById('gallery');

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const files = document.getElementById('input-photo').files;
        if (files.length === 0) {
            await  setupAlert("Пожалуйста, выберите файл для загрузки");
            return;
        }
        const paintingPhoto = {
            photo: files[0]
        };

        let paintingImgPath;


        try {
            paintingImgPath = await paintingUploadToYC(paintingPhoto);
        } catch (error) {
            console.error("Ошибка в процессе добавления картины на диск:", error);
        }


        const paintingInfo = {
            artist_account_id: accountPageId,
            img_path: paintingImgPath.img_url,
            description: document.getElementById('photo-desc').value,
        }

        try {
            const popupImageDescription = document.getElementById('photo-desc');
            console.log(popupImageDescription.value);
            popupImageDescription.value = "";
            const paintingId = await paintingPost(paintingInfo);
            const node = await createNode(paintingId);
            if (gallery.children.length > 1) {
                gallery.insertBefore(node, gallery.children[1]);
            } else {
                gallery.appendChild(node);
            }

            await new Promise(resolve => {
                setTimeout(() => {
                    node.classList.add('showItem');
                    resolve();
                }, 20);
            });

        } catch (error) {
            await setupAlert(`Ошибка в процессе добавления картины: ${error}`);
            console.error("Ошибка в процессе добавления картины:", error);
        }
    })
}

export async function paintingUploadToYC(paintingPhoto) {
    try {
        const formData = new FormData();
        formData.append('file', paintingPhoto.photo);

        const response = await fetch(`${apiBaseUrl}/upload-photo/`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Ошибка при загрузке файла на Yandex Cloud:", error);
        throw error;
    }
}

async function paintingPost(paintingInfo) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${apiBaseUrl}/paintings/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(paintingInfo)
        });
        const data = await response.json();
        return data.id;

    } catch (error) {
        console.error("Ошибка при добавлении картины:", error);
        await setupAlert("Ошибка при добавлении картины");
    }
}


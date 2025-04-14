import {fetchPaintingById} from "./fetchPaintingById.js";
import { apiBaseUrl } from './apiConfig.js';

export async function setupPostPainting(accountPageId) {
    const popup = document.getElementById('add-photo-popup');
    const form = document.getElementById('popup-form');

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const files = document.getElementById('input-photo').files;
        if (files.length === 0) {
            alert("Пожалуйста, выберите хотя бы один файл");
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

        console.log(paintingPhoto)

        const paintingInfo = {
            artist_account_id: accountPageId,
            img_path: paintingImgPath.img_url,
            description: document.getElementById('photo-desc').value,
        }

        console.log(paintingInfo)

        try {
            popup.style.display = 'none';
            await paintingPost(paintingInfo);
            window.location.reload();

        } catch (error) {
            console.error("Ошибка в процессе добавления картины:", error);
            popup.style.display = 'none';
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
        await fetch(`${apiBaseUrl}/paintings/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(paintingInfo)
        });

    } catch (error) {
        console.error("Ошибка при добавлении картины:", error);
        alert("Ошибка при добавлении картины");
    }
}

import { apiBaseUrl } from './apiConfig.js';

async function register() {
    try {

        const form = document.querySelector('form');
        form.addEventListener('submit', async (event) => {
            event.preventDefault();

            const name = document.getElementById('name').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;

            const files = document.getElementById('avatar').files;
            if (files.length === 0) {
                alert("Пожалуйста, выберите хотя бы один файл");
                return;
            }
            const paintingPhoto = {
                photo: files[0]
            };

            let avatarImgPath;
            try {
                avatarImgPath = await avatarUploadToYC(paintingPhoto);
            } catch (error) {
                console.error("Ошибка в процессе добавления картины на диск:", error);
            }

            if (password !== confirmPassword) {
                alert('Ваши пароли не совпадают!!!');
            }

            const registerPayload = {
                login: name,
                password: password,
                avatar_img_path: avatarImgPath.img_url,
            };

            console.log(registerPayload)


            const response = await fetch(`${apiBaseUrl}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(registerPayload)
            })

            if (response.ok) {
                const data = response.json();
                window.location.href = `/login`;
            } else {
                throw new Error('Ошибка в регистрации');
            }

        })

    } catch (error) {
        console.error("Ошибка при регистрации", error);
        window.handleScriptError(error);
    }
}

async function avatarUploadToYC(paintingPhoto) {
    try {
        const formData = new FormData();
        formData.append('file', paintingPhoto.photo);

        console.log(12132)

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


document.addEventListener("DOMContentLoaded", () => {
    register();
})
import {setupAlert} from "../setup/setupAlert.js";
import {register} from "../requests/register.js";
import {paintingUploadToYC} from "../setup/setupPostPainting.js";
import {setupNavMenuButton} from "../utils/navMenuUtils.js";
import {fetchCurrentAccount} from "../requests/fetchCurrentAccount.js";

async function setupRegisterPage() {
    try {
        const me = await fetchCurrentAccount();
        await setupNavMenuButton(me);

        const createAccountBtn = document.getElementById('create-account-btn');
        createAccountBtn.addEventListener('click', () => {
            location.href = '/login';
        })

        const avatarInput = document.getElementById('avatar');
        const avatarFileName = document.getElementById('avatar-filename');
        const labelAvatar = document.querySelector('.input-file-button')

        avatarInput.addEventListener('change', () => {
            if (avatarInput.files.length > 0) {
                const names = Array.from(avatarInput.files).map(f => f.name);
                avatarFileName.textContent = names.join(', ');
                labelAvatar.textContent = 'Файл выбран!';
                labelAvatar.classList.remove('default');
                labelAvatar.classList.add('selected');
            } else {
                labelAvatar.textContent = 'Выберите аватар';
                avatarFileName.textContent = 'Файл не выбран';
                labelAvatar.classList.remove('selected');
                labelAvatar.classList.add('default');
            }
        });


        const form = document.querySelector('form');
        form.addEventListener('submit', async (event) => {

            event.preventDefault();


            const username = document.getElementById('name').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;

            if (password !== confirmPassword) {
                await setupAlert('Ваши пароли не совпадают');
                return;
            }

            const files = document.getElementById('avatar').files;
            if (files.length === 0) {
                await setupAlert("Выберите файл для аватарки");
                return;
            }

            const paintingPhoto = {
                photo: files[0]
            };

            let avatarImgPath;
            try {
                avatarImgPath = await paintingUploadToYC(paintingPhoto);
            } catch (error) {
                console.error("Ошибка в процессе добавления картины на диск:", error);
            }

            const registerPayload = {
                login: username,
                password: password,
                avatar_img_path: avatarImgPath.img_url,
            };


            try {
                await register(registerPayload);
            } catch (error) {
                await setupAlert(error.message);
            }
        })

    } catch (error) {
        window.handleScriptError(error);
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    await setupRegisterPage();
})
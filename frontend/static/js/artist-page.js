import {apiBaseUrl} from './apiConfig.js';

import {fetchArtistById} from "./fetchArtistById.js";
import {fetchPaintingById} from "./fetchPaintingById.js";
import {getScrollbarWidth} from "./getScrollbarWidth.js";
import {setupPostPainting} from "./setupPostPainting.js";
import {fetchCurrentAccount} from "./fetchCurrentAccount.js";
import {subscribe} from "./subscribe.js";
import {extensionFetchByLogin} from "./extensionFetchByLogin.js";
import {unsubscribe} from "./unsubscribe.js";
import {likePainting} from "./likePainting.js";
import {unlikePainting} from "./unlikePainting.js";

async function fetchDataArtistPage(login) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${apiBaseUrl}/artist-pages/by_login/${login}`,
            {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();

        setupPostPainting(data.artist_id)

        console.log(data)

        const id = data.artist_id;
        const paintingsIds = data.painting_ids;

        const artistInfo = await fetchArtistById(id);
        const me = await fetchCurrentAccount();

        console.log(me);

        if (me) {
            document.getElementById('pc-username').innerHTML =
                `<a href="/accounts/${me.login}">${me.login}</a>`;
            document.getElementById('mobile-username').innerHTML =
                `<a href="/accounts/${me.login}">${me.login}</a>`;
            if (data.is_owner) {
                document.getElementById('editor').style = 'display:block';
                document.getElementById('editor').href = `/editor/${login}`;

            }
        }

        if (artistInfo) {
            document.getElementById('author-name').innerHTML = artistInfo.name;
            document.getElementById('likes').innerHTML = artistInfo.subscribers_count;
            document.getElementById('main-picture').style =
                `background-image: linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.5)), url(${artistInfo.img_path});`
            const gallery = document.getElementById('gallery');

            // По каждой картине загружаем данные и формируем DOM
            for (const paintingId of paintingsIds) {
                const paintingInfo = await fetchPaintingById(paintingId);
                gallery.innerHTML += `
          <div class="photo no-select">
            <img class="photo-item" src="${paintingInfo.img_path}" data-description="${paintingInfo.description}">
            <button class="like-painting-btn" id="${paintingId}"><img src="../static/root/nolike.svg" alt=""></button>
          </div>`
            }
        }

        // Выбор DOM-элементов
        const photos = document.querySelectorAll('.photo .photo-item');
        const overlay = document.getElementById('overlay');
        const fullImage = document.getElementById('fullImage');
        const navMenuLoader = document.querySelector('.nav-menu-loader');
        const body = document.querySelector('body');
        const menuIcon = document.getElementById('menu-icon');
        const menu = document.getElementById('more');
        const nav = document.querySelector('.nav');

        // Слушатели на иконку меню
        navMenuLoader.addEventListener('click', function () {
            if (menuIcon.src.endsWith('menu.svg')) {
                menu.classList.add('show');
                setTimeout(() => {
                    menuIcon.src = "../static/root/x.svg";
                }, 100);
            } else {
                menu.classList.remove('show');
                setTimeout(() => {
                    menuIcon.src = "../static/root/menu.svg";
                }, 0);
            }
        });

        // Закрытие меню по клику вне его
        body.addEventListener('click', function () {
            if (menuIcon.src.endsWith('x.svg')) {
                menu.classList.remove('show');
                setTimeout(() => {
                    menuIcon.src = "../static/root/menu.svg";
                }, 0);
            }
        });

        // Слушатели на каждое изображение
        photos.forEach(photo => {
            photo.addEventListener('click', function () {
                const scrollbarWidth = getScrollbarWidth();
                const description = this.getAttribute('data-description');
                const imageDescription = document.getElementById('imageDescription');

                fullImage.src = this.src;
                imageDescription.textContent = description;
                overlay.classList.add('active');
                document.body.classList.add('no-scroll');
                document.body.style.overflow = 'hidden';
                nav.style.paddingRight = `${scrollbarWidth}px`;
                document.body.style.paddingRight = `${scrollbarWidth}px`;
            });
        });

        // Закрытие оверлея
        overlay.addEventListener('click', function () {
            overlay.classList.remove('active');
            document.body.classList.remove('no-scroll');
            document.querySelector('.nav').style.paddingRight = '';
            document.body.style.overflow = '';
            document.body.style.paddingRight = '';
            setTimeout(() => fullImage.src = '', 150);
        });

        // Работа с формами (добавление фото, альбома)
        const path = window.location.pathname;
        const segments = path.split('/');
        const sec_id = segments[segments.length - 1];
        const addPhotoButtons = document.querySelectorAll('.first');
        const addPhotoPopup = document.getElementById('add-photo-popup');
        const albumInput = document.querySelector('input[name="album_id"]');
        const addPhotoSectionInput = document.querySelector('input[name="section_id1"]');

        // Кнопки “Добавить фото”
        addPhotoButtons.forEach((firstItem) => {
            firstItem.addEventListener('click', () => {
                const scrollbarWidth = getScrollbarWidth();
                albumInput.value = firstItem.getAttribute('data-album-id');
                addPhotoSectionInput.value = sec_id;
                addPhotoPopup.classList.add('open');
                document.body.classList.add('no-scroll');
                document.body.style.paddingRight = `${scrollbarWidth}px`;
                nav.style.paddingRight = `${scrollbarWidth}px`;
            });
        });


        // Закрытие всплывающих окон по клику вне их содержимого
        addPhotoPopup.addEventListener('click', (event) => {
            if (!event.target.closest('.popup-content')) {
                addPhotoPopup.classList.remove('open');
                document.body.classList.remove('no-scroll');
                document.body.style.paddingRight = "";
                nav.style.paddingRight = "";
            }
        });

        const subscribeButton = document.querySelector('.link.like');
        subscribeButton.addEventListener('click', async (event) => {
            event.preventDefault();
            const myLogin = me.login;
            console.log(myLogin)

            const path = window.location.pathname;
            const loginToSubscribe = path.split("/").pop();

            const artistData = await extensionFetchByLogin(loginToSubscribe);
            const id = artistData.artist_id;

            console.log(me.subscribed_artist_ids)

            if (!me.subscribed_artist_ids.includes(id)) {
                await subscribe(myLogin, id);
            } else {
                await unsubscribe(myLogin, id);
            }

            window.location.reload();
        });

        const likeButtons = document.querySelectorAll('.like-painting-btn');
        likeButtons.forEach((likeBtn) => {
            likeBtn.addEventListener('click', async (event) => {
                event.preventDefault();
                const myLogin = me.login;

                const paintingId = +event.currentTarget.id;

                if (!me.liked_paintings_ids.includes(paintingId)) {
                    await likePainting(myLogin, paintingId);
                } else {
                    await unlikePainting(myLogin, paintingId);
                }

            });
        })


    } catch (error) {
        console.error("Ошибка при выполнении запроса:", error);
        window.handleScriptError(error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const path = window.location.pathname;
    const login = path.split("/").pop();
    fetchDataArtistPage(login);
});
import {apiBaseUrl} from './apiConfig.js';
import {fetchArtistById} from "./fetchArtistById.js";
import {fetchPaintingById} from "./fetchPaintingById.js";
import {getScrollbarWidth} from "./getScrollbarWidth.js";
import {setupPostPainting} from "./setupPostPainting.js";
import {fetchCurrentAccount} from "./fetchCurrentAccount.js";
import {patchPainting} from "./patchPainting.js";
import {patchArtist} from "./patchArtist.js";
import {extensionFetchByLogin} from "./extensionFetchByLogin.js";
import {paintingUploadToYC} from "./setupPostPainting.js";
import {deletePainting} from "./deletePainting.js";

async function fetchDataArtistPage(login) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${apiBaseUrl}/artist-pages/by_login/${login}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();

        // Настраиваем функционал добавления новых картин (у вас это уже есть)
        setupPostPainting(data.artist_id);

        console.log(data);

        const id = data.artist_id;
        const paintingsIds = data.painting_ids;

        const artistInfo = await fetchArtistById(id);
        const me = await fetchCurrentAccount();

        console.log(me);
        console.log(artistInfo)

        // Если пользователь авторизован, проставляем в шапку его логин
        if (me) {
            document.getElementById('pc-username').innerHTML =
                `<a href="/accounts/${me.login}">${me.login}</a>`;
            document.getElementById('mobile-username').innerHTML =
                `<a href="/accounts/${me.login}">${me.login}</a>`;

            // Если это страница артиста, и мы - владелец
            if (data.is_owner) {
                // Показываем ссылку «Перейти в режим редактирования»
                document.getElementById('editor').style = 'display:block';
                document.getElementById('editor').href = `../${login}`;
            }
        }

        // Заполнение данных об авторе: имя, количество лайков/подписчиков, фон
        if (artistInfo) {
            document.getElementById('author-name').innerHTML = artistInfo.name;
            document.getElementById('likes').innerHTML = artistInfo.subscribers_count;
            document.getElementById('main-picture').style =
                `background-image: linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.5)), url(${artistInfo.img_path});`

            // Блок «Галерея»
            const gallery = document.getElementById('gallery');

            // Для каждой картины создаём DOM-элементы с фото и кнопками
            for (const paintingId of paintingsIds) {
                const paintingInfo = await fetchPaintingById(paintingId);
                gallery.innerHTML += `
                    <div class="photo photo-m no-select">
                        <img src="${paintingInfo.img_path}" data-description="${paintingInfo.description}">
                        <button class="delete-photo-btn" id="${paintingId}"><img src="../static/root/xwhite.svg" alt=""></button>
                        <button class="change-painting-describe-btn" id="${paintingId}"><img src="../static/root/change.svg" alt=""></button>
                    </div>
                `
                    // <button class="delete-photo-btn" id="${paintingId}"><img src="../static/root/change.svg" alt=""></button>
                    // <button class="change-painting-describe-btn" id="${paintingId}"><img src="../static/root/change.svg" alt="">
            }
        }

        // -------------------------
        // Здесь начинаем навешивать слушатели событий на то, что уже отрендерилось
        // -------------------------

        // Обработчик на иконку «гамбургера» в шапке
        const navMenuLoader = document.querySelector('.nav-menu-loader');
        const body = document.querySelector('body');
        const menuIcon = document.getElementById('menu-icon');
        const menu = document.getElementById('more');
        const nav = document.querySelector('.nav');

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

        // Навешиваем клики на все фото в галерее для открытия в оверлее
        // const photos = document.querySelectorAll('.photo img');
        // const overlay = document.getElementById('overlay');
        // const fullImage = document.getElementById('fullImage');
        //
        // photos.forEach(photo => {
        //     photo.addEventListener('click', function () {
        //         const scrollbarWidth = getScrollbarWidth();
        //         const description = this.getAttribute('data-description');
        //         const imageDescription = document.getElementById('imageDescription');
        //
        //         fullImage.src = this.src;
        //         imageDescription.textContent = description;
        //         overlay.classList.add('active');
        //         document.body.classList.add('no-scroll');
        //         document.body.style.overflow = 'hidden';
        //         nav.style.paddingRight = `${scrollbarWidth}px`;
        //         document.body.style.paddingRight = `${scrollbarWidth}px`;
        //     });
        // });
        //
        // // Закрытие оверлея по клику
        // overlay.addEventListener('click', function () {
        //     overlay.classList.remove('active');
        //     document.body.classList.remove('no-scroll');
        //     document.body.style.overflow = '';
        //     document.body.style.paddingRight = '';
        //     nav.style.paddingRight = '';
        //     setTimeout(() => fullImage.src = '', 150);
        // });

        // Попап «Добавить фото»
        const path = window.location.pathname;
        const segments = path.split('/');
        const sec_id = segments[segments.length - 1];
        const addPhotoButtons = document.querySelectorAll('.first');
        const addPhotoPopup = document.getElementById('add-photo-popup');
        const albumInput = document.querySelector('input[name="album_id"]');
        const addPhotoSectionInput = document.querySelector('input[name="section_id1"]');

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

        addPhotoPopup.addEventListener('click', (event) => {
            if (!event.target.closest('.popup-content')) {
                addPhotoPopup.classList.remove('open');
                document.body.classList.remove('no-scroll');
                document.body.style.paddingRight = "";
                nav.style.paddingRight = "";
            }
        });

        // -------------------------
        // Теперь добавляем конкретные обработчики для кнопок
        // -------------------------

        // 1) Кнопка «Изменить фон»
        const changeBackgroundBtn = document.getElementById('change-background-btn');
        const changeBackgroundPopup = document.getElementById('change-background-popup');
        if (changeBackgroundBtn) {
            changeBackgroundBtn.addEventListener('click', async (event) => {
                console.log('Нажали кнопку "Изменить фон"');
                changeBackgroundPopup.classList.add('open');

                const path = window.location.pathname;
                const login = path.split("/").pop();

                const dataByLogin = await extensionFetchByLogin(login)

                const artistInfo = await fetchArtistById(dataByLogin.artist_id);

                const form = document.getElementById('change-background-popup');
                form.addEventListener('submit', async function (event) {
                    event.preventDefault();

                    const newBackground = {
                        photo: document.getElementById('new-background').files[0]
                    };

                    const name = artistInfo.name;
                    const newImgPath = await paintingUploadToYC(newBackground);
                    const description = artistInfo.description;

                    console.log(newImgPath);

                    await patchArtist(name, newImgPath.img_url, description);

                    changeBackgroundPopup.classList.remove('open');

                    window.location.reload();

                });

            });
        }

        changeBackgroundPopup.addEventListener('click', (event) => {
            if (!event.target.closest('.popup-content')) {
                changeBackgroundPopup.classList.remove('open');
                document.body.classList.remove('no-scroll');
                document.body.style.paddingRight = "";
                nav.style.paddingRight = "";
            }
        });

        // 2) Кнопка «Сменить имя автора»
        const changeAuthorNameBtn = document.getElementById('change-author-name-btn');
        const changeAuthorNamePopup = document.getElementById('change-author-name-popup');
        if (changeAuthorNameBtn) {
            changeAuthorNameBtn.addEventListener('click', async (event) => {
                console.log(`Нажали кнопку "Сменить имя автора" ${event.target.id}`);
                changeAuthorNamePopup.classList.add('open');

                const path = window.location.pathname;
                const login = path.split("/").pop();

                const dataByLogin = await extensionFetchByLogin(login)

                const artistInfo = await fetchArtistById(dataByLogin.artist_id);

                document.getElementById('new-author-name').placeholder = artistInfo.name;

                const form = document.getElementById('change-author-name-form');
                form.addEventListener('submit', async function (event) {
                    event.preventDefault();

                    const newName = document.getElementById('new-author-name').value;
                    const img_path = artistInfo.img_path;
                    const description = artistInfo.description;


                    await patchArtist(newName, img_path, description)
                    changeAuthorNamePopup.classList.remove('open');

                    window.location.reload();


                });



            });
        }

        changeAuthorNamePopup.addEventListener('click', (event) => {
            if (!event.target.closest('.popup-content')) {
                changeAuthorNamePopup.classList.remove('open');
                document.body.classList.remove('no-scroll');
                document.body.style.paddingRight = "";
                nav.style.paddingRight = "";
            }
        });


        // 4) Клики по «Лайк», «Поделиться», «Смотреть»
        const likeEl = document.querySelector('.link.like');
        if (likeEl) {
            likeEl.addEventListener('click', () => {
                console.log("Нажали «Лайк»");
                // TODO: Релаизовать логику отправки лайка (например, POST на /api/likes)
            });
        }

        const repostEl = document.querySelector('.link.repost');
        if (repostEl) {
            repostEl.addEventListener('click', () => {
                console.log("Нажали «Поделиться»");
                // TODO: Функционал репоста/поделиться (например, открытие соц. сетей или копирование ссылки)
            });
        }

        const playEl = document.querySelector('.link.play');
        if (playEl) {
            playEl.addEventListener('click', () => {
                console.log("Нажали «Смотреть»");
                // TODO: Открыть страницу/попап с видео, если это предусмотрено
            });
        }

        // 5) Динамически добавленные кнопки «Удалить фото» и «Изменить описание»
        //    (появились в галерее после цикла for)
        const gallery = document.getElementById('gallery');

        // Находим все кнопки «Удалить фото»
        const deletePhotoButtons = gallery.querySelectorAll('.delete-photo-btn');
        deletePhotoButtons.forEach(button => {
            button.addEventListener('click', async (e) => {
                const paintingId = e.currentTarget.id;
                console.log('Нажата кнопка «Удалить фото»:', paintingId);
                await deletePainting(paintingId)
                window.location.reload();
            });
        });

        // Находим все кнопки «Изменить описание»
        const changePaintingDescribeButtons = gallery.querySelectorAll('.change-painting-describe-btn');

        const changePaintingDescribePopup = document.getElementById('change-painting-describe-popup');

        changePaintingDescribeButtons.forEach(button => {
            button.addEventListener('click', async (e) => {
                const paintingId = e.currentTarget.id;
                console.log('Нажата кнопка «Изменить описание» для фото:', paintingId);
                changePaintingDescribePopup.classList.add('open');

                const oldDescribe = document.getElementById('new-painting-describe');
                const paintingInfo = await fetchPaintingById(paintingId)
                oldDescribe.innerHTML = paintingInfo.description;

                const form = document.getElementById('change-painting-describe-form');
                form.addEventListener('submit', async function (event) {
                    event.preventDefault();

                    const newDescription = document.getElementById('new-painting-describe').value;
                    const imgPath = paintingInfo.img_path;

                    await patchPainting(paintingId, newDescription, imgPath);

                    window.location.reload();

                    changePaintingDescribePopup.classList.remove('open');

                });

            });


        });

        changePaintingDescribePopup.addEventListener('click', (event) => {
            if (!event.target.closest('.popup-content')) {
                changePaintingDescribePopup.classList.remove('open');
                document.body.classList.remove('no-scroll');
                document.body.style.paddingRight = "";
                nav.style.paddingRight = "";
            }
        });

    } catch (error) {
        console.error("Ошибка при выполнении запроса:", error);
        // Вызов вашей функции handleScriptError в случае ошибки
        window.handleScriptError(error);
    }
}

// Запускаем после загрузки DOM, чтобы корректно найти элементы
document.addEventListener("DOMContentLoaded", () => {
    const path = window.location.pathname;
    const login = path.split("/").pop();
    fetchDataArtistPage(login);
});

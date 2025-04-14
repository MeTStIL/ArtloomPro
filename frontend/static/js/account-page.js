import { apiBaseUrl } from './apiConfig.js';

import { fetchArtistById } from "./fetchArtistById.js"
import { fetchPaintingById } from "./fetchPaintingById.js";
import { setupArtistPageCreate } from "./setupArtistPageCreate.js";
import { getScrollbarWidth } from "./getScrollbarWidth.js";
import { fetchCurrentAccount } from "./fetchCurrentAccount.js";
import {fetchArtistPageById } from "./fetchArtistPageById.js";

async function fetchDataAccountPage(login) {
  try {
    const token = localStorage.getItem('access_token');
    const response = await fetch(`${apiBaseUrl}/accounts/${login}`,
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

    await setupArtistPageCreate(login);

    const gallery = document.getElementById('gallery');
    const authors = document.getElementById('authors');

    const me = await fetchCurrentAccount();

    console.log(me);

    if (me) {
      document.getElementById('pc-username').innerHTML =
          `<a href="/accounts/${me.login}">${me.login}</a>`;
      document.getElementById('mobile-username').innerHTML =
          `<a href="/accounts/${me.login}">${me.login}</a>`;
      if (me.artist_id) {
        document.getElementById('artist-page-button').style = 'display:none';
        document.getElementById('my-page').href = `/${login}`
        document.getElementById('my-page').style = 'display:flex';
      }
    }

    // По каждой картине загружаем данные и формируем DOM
    for (const paintingId of data.liked_paintings_ids) {
      const paintingInfo = await fetchPaintingById(paintingId);
      gallery.innerHTML += `
      <div class="photo no-select">
        <img src="${paintingInfo.img_path}" data-description="${paintingInfo.description}">
      </div>`;
    }

    for (const authorId of data.subscribed_artist_ids) {

      const authorInfo = await fetchArtistById(authorId);
      const authorPageInfo = await fetchArtistPageById(authorInfo.artist_page_id);
      authors.innerHTML += `
      <a class="no-select author-photo" href="${authorPageInfo.url}">
        <img src="${authorInfo.img_path}">
      </a>`;
    }

    // Выбор DOM-элементов
    const photos = document.querySelectorAll('.photo img');
    const overlay = document.getElementById('overlay');
    const fullImage = document.getElementById('fullImage');
    const navMenuLoader = document.querySelector('.nav-menu-loader');
    const body = document.querySelector('body');
    const menuIcon = document.getElementById('menu-icon');
    const menu = document.getElementById('more');
    const nav = document.querySelector('.nav');

    // Слушатели на иконку меню
    navMenuLoader.addEventListener('click', function() {
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
    body.addEventListener('click', function() {
      if (menuIcon.src.endsWith('x.svg')) {
        menu.classList.remove('show');
        setTimeout(() => {
          menuIcon.src = "../static/root/menu.svg";
        }, 0);
      }
    });

    // Слушатели на каждое изображение
    photos.forEach(photo => {
      photo.addEventListener('click', function() {
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
    overlay.addEventListener('click', function() {
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
    const addAlbumButton = document.querySelector('.add-button');
    const addAlbumSectionInput = document.querySelector('input[name="section_id2"]');
    const addAlbumPopup = document.getElementById('add-page-popup');

    // Кнопка “Добавить альбом”
    addAlbumButton.addEventListener('click', () => {
      const scrollbarWidth = getScrollbarWidth();
      addAlbumSectionInput.value = sec_id;
      addAlbumPopup.classList.add('open');
      document.body.classList.add('no-scroll');
      document.body.style.paddingRight = `${scrollbarWidth}px`;
      nav.style.paddingRight = `${scrollbarWidth}px`;
    });

    // Закрытие всплывающих окон по клику вне их содержимого
    addAlbumPopup.addEventListener('click', (event) => {
      if (!event.target.closest('.popup-content')) {
        addAlbumPopup.classList.remove('open');
        document.body.classList.remove('no-scroll');
        document.body.style.paddingRight = "";
        nav.style.paddingRight = "";
      }
    });

  } catch (error) {
    console.error("Ошибка при выполнении запроса:", error);
    window.handleScriptError(error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;
  const login = path.split("/").pop();
  fetchDataAccountPage(login);
});
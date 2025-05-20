import { subscribe } from "../requests/subscribe.js";
import { unsubscribe } from "../requests/unsubscribe.js";


export async function setupArtistMenuButtons(me, artistId, count) {
    setupSubscriberButton(me, artistId, count);
    setupShareButton();
    setupWatchButton();
}

function setupSubscriberButton(me, artistId, count) {
    const subscribeButton = document.querySelector('.link.like');
    const subscribersCount = document.getElementById('likes');
    subscribersCount.textContent = count;
    if (!me) {
        return;
    }

    if (me.subscribed_artist_ids.includes(artistId)) {
        subscribeButton.classList.add('subscribed');
    }
    subscribeButton.addEventListener('click', async () => {
        if (!subscribeButton.classList.contains('subscribed')) {
            subscribeButton.classList.add('subscribed');
            subscribersCount.innerText = Number(subscribersCount.innerText) + 1;
            await subscribe(me.login, artistId);
        } else {
            subscribeButton.classList.remove('subscribed');
            subscribersCount.innerText = Number(subscribersCount.innerText) - 1;
            await unsubscribe(me.login, artistId);
        }
    });
}

function setupShareButton() {
    const shareButton = document.getElementById('repost-btn');
    shareButton.addEventListener('click', async (event) => {
        let link = window.location.href;
        if (link.includes("editor")) {
            link = link.replace("editor/", "");
        }

        await navigator.clipboard.writeText(link);
        const shareImg = document.getElementById('share-img');
        shareImg.src = '../static/root/repostgreen.svg';

        const shareBtn = document.getElementById('share-btn');
        shareBtn.textContent = 'Скопировано!';

        setTimeout(() => {
            shareImg.src = '../static/root/repost.svg';
            shareBtn.textContent = 'Поделиться';
        }, 2000);
    });
}

function setupWatchButton() {
    const watchButton = document.getElementById('watch-btn');
    watchButton.addEventListener('click', () => {
        document.getElementById('gallery').scrollIntoView({
            behavior: "smooth"
        });
    })
}
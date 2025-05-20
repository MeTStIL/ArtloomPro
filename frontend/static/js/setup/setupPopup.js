import { setOverlay, removeOverlay } from "../utils/overlayUtils.js";

export async function setupPopup(button, popup) {

    const overlay = document.getElementById('overlay');
    const nav = document.querySelector('.nav');
    const loadButtons = document.querySelectorAll('.loadButton');

    button.addEventListener('click', async () => {
        popup.classList.add('open');
        setOverlay(overlay, document.body, nav, popup);
    });

    popup.addEventListener('click', async (event) => {
        if (!event.target.closest('.popup-content')) {
            popup.classList.remove('open');
            removeOverlay(overlay, document.body, nav, popup);
        }
    });

    for (const button of loadButtons) {
        button.addEventListener('click', async (event) => {
            popup.classList.remove('open');
            removeOverlay(overlay, document.body, nav, popup);
        })
    }
}
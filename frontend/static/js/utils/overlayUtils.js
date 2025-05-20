import { getScrollbarWidth } from "./getScrollbarWidth.js";


export function setOverlay(overlay, ...elements) {
    const scrollbarWidth = getScrollbarWidth();
    overlay.classList.add('active');
    document.body.classList.add('no-scroll');
    document.body.style.overflow = 'hidden';

    for (const e of elements) {
        e.style.paddingRight = `${scrollbarWidth}px`;
    }
}

export function removeOverlay(overlay, ...elements) {
    overlay.classList.remove('active');
    document.body.classList.remove('no-scroll');
    document.body.style.overflow = '';

    for (const e of elements) {
        e.style.paddingRight = '';
    }
}
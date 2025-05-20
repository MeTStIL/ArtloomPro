import { setOverlay, removeOverlay} from "../utils/overlayUtils.js";

export async function setupAlert(error){
    const hiddenAlert = document.querySelector(".hidden-alert");
    const alertContent = document.querySelector(".alert-content");
    alertContent.textContent = error;
    hiddenAlert.classList.remove("hidden-alert");
    setTimeout(() => {
        hiddenAlert.classList.add("hidden-alert");
    }, 4000);

}
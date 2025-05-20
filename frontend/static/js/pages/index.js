import { fetchCurrentAccount } from "../requests/fetchCurrentAccount.js";
import { setupNavMenuButton } from "../utils/navMenuUtils.js";


document.addEventListener("DOMContentLoaded", async () => {
    const me = await fetchCurrentAccount();
    await setupNavMenuButton(me);
    document.getElementById("index-register").addEventListener("click", async () => {
        window.location.href = "/register";
    })
    document.getElementById("index-search").addEventListener("click", async () => {
        window.location.href = "/search";
    })
});
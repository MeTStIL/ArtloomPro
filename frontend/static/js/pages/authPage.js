import {auth} from "../requests/auth.js";
import {setupNavMenuButton} from "../utils/navMenuUtils.js";
import {fetchCurrentAccount} from "../requests/fetchCurrentAccount.js";
import {setupAlert} from "../setup/setupAlert.js";

async function setupAuthPage() {
    const me = await fetchCurrentAccount();
    await setupNavMenuButton(me);

    try {
        const loader = document.getElementById('loader');
        const overlay_l = document.getElementById('overlay-l');
        const content = document.getElementById('content');

        const authForm = document.querySelector('form');

        const createAccountBtn = document.getElementById('create-account-btn');
        createAccountBtn.addEventListener('click', () => {
            location.href = '/register';
        })

        authForm.addEventListener('submit', async (event) => {
            overlay_l.style.display = 'block';
            loader.style.display = 'block';
            event.preventDefault();

            const username = document.getElementById('name').value;
            const password = document.getElementById('password').value;

            const userData = new URLSearchParams();
            userData.append('username', username);
            userData.append('password', password);
            try {
                await auth(userData);
                window.location.href = `/accounts/${username}`;
            } catch (error) {
                await setupAlert(error.message);
            }
            loader.style.display = 'none';
            overlay_l.style.display = 'none';  
            content.style.display = 'block';
        });
    } catch (error) {
        window.handleScriptError(error);
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    await setupAuthPage();
});
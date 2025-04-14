import { apiBaseUrl } from './apiConfig.js';

async function auth() {
    try {
        const loginForm = document.querySelector('form');

        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const username = document.getElementById('name').value;
            const password = document.getElementById('password').value;

            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const response = await fetch(`${apiBaseUrl}/auth`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData.toString()
            })

            if (response.ok) {
                const data = await response.json();

                const accessToken = data.access_token;
                localStorage.setItem('access_token', accessToken);


                window.location.href = `/accounts/${username}`;
            } else {
                throw new Error('Ошибка auth');
            }
        })
    } catch (error) {
        console.error("Ошибка auth", error);
        window.handleScriptError(error);
    }



}

document.addEventListener("DOMContentLoaded", () => {
    auth();
})
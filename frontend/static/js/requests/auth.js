import {apiBaseUrl} from "../utils/apiBaseUrl.js";

export async function auth(userData) {
    const response = await fetch(`${apiBaseUrl}/auth/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: userData
    })

    if (response.ok) {
        const data = await response.json();
        const accessToken = data.access_token;

        localStorage.setItem('access_token', accessToken);
    } else {
        if (response.status > 500) {
            throw new Error('Ошибка авторизации');
        } else {
            throw new Error('Неправильный логин или пароль');
        }

    }
}
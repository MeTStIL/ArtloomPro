import {apiBaseUrl} from "../utils/apiBaseUrl.js";

export async function register(registerPayload) {
    const response = await fetch(`${apiBaseUrl}/register/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(registerPayload)
    })

    if (response.ok) {
        const data = await response.json();

        const accessToken = data.access_token;
        localStorage.setItem('access_token', accessToken);

        window.location.href = `/accounts/${registerPayload.login}`;
    } else {
        throw new Error('Такой логин уже существует');
    }
}
import {apiBaseUrl} from '../utils/apiBaseUrl.js';

export async function fetchAccountPageByLogin(login) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${apiBaseUrl}/accounts/${login}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        return await response.json();

    } catch (error) {
        console.log(`Ошибка ${error}`);
        throw error;
    }
}
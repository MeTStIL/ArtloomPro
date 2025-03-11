async function fetchData() {
    try {
        // Выполняем GET-запрос к FastAPI
        const response = await fetch('http://localhost:8000');

        // Проверяем, успешен ли запрос
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }

        const data = await response.json();

        const result = document.getElementById('message');

        if (result) {
            result.innerHTML = `<p>${data.message}</p>`;
        }
    } catch (error) {
        console.error("Ошибка при выполнении запроса:", error);

        // Если произошла ошибка, выводим сообщение об ошибке
        const result = document.getElementById('message');
        if (result) {
            result.innerHTML = "<p>Ошибка при загрузке данных.</p>";
        }
    }
}

// Вызываем функцию при загрузке страницы
document.addEventListener("DOMContentLoaded", fetchData);
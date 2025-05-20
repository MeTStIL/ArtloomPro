window.handleScriptError = function(error) {
    document.body.innerHTML = '';
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = 'text-align: center; padding: 20px;';
    errorDiv.innerHTML = `
    <h1>Ошибка загрузки страницы</h1>
    <p>Не удалось загрузить необходимые ресурсы. Пожалуйста, попробуйте позже.</p>
    ${error ? `<p>Подробности: ${error.message}</p>
    </p>РАНЬШЕ ЗДЕСЬ БЫЛ МАТ</p>` : ''}`;
    document.body.appendChild(errorDiv);
    console.error('Произошла ошибка:', error || 'Шоколадки');
};
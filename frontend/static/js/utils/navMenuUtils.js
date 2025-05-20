export async function setupNavMenuButton(me = null) {
    const navMenuButton = document.querySelector('.nav-menu-button');
    const menuIcon = document.getElementById('menu-icon');
    const menu = document.getElementById('more');
    const artloomButton = document.querySelector('.title');

    if (me) {
        const pcUsername = document.createElement('a');
        pcUsername.href = `/accounts/${me.login}`;
        pcUsername.textContent = me.login;

        const mobileUsername = document.createElement('a');
        mobileUsername.href = `/accounts/${me.login}`;
        mobileUsername.textContent = me.login;

        const pcUsernameWrapper = document.getElementById('pc-username');
        pcUsernameWrapper.firstChild.remove();
        pcUsernameWrapper.appendChild(pcUsername);
        pcUsernameWrapper.appendChild(getLogoutButton());

        const mobileUsernameWrapper = document.getElementById('mobile-username');
        mobileUsernameWrapper.firstChild.remove();
        mobileUsernameWrapper.appendChild(mobileUsername);
        mobileUsernameWrapper.appendChild(getLogoutButton());
    }

    navMenuButton.addEventListener('click', async function () {

        if (menuIcon.src.endsWith('menu.svg')) {
            menu.classList.add('show');
            setTimeout(() => {
                menuIcon.src = "../static/root/x.svg";
            }, 100);
        } else {
            menu.classList.remove('show');
            setTimeout(() => {
                menuIcon.src = "../static/root/menu.svg";
            }, 0);
        }
    });

    artloomButton.addEventListener('click', () => {
        window.location.href = '/';
    });


    document.body.addEventListener('click', async function () {
        if (menuIcon.src.endsWith('x.svg')) {
            menu.classList.remove('show');
            setTimeout(() => {
                menuIcon.src = "../static/root/menu.svg";
            }, 0);
        }
    });
}

function getLogoutButton() {
    const logoutImage = document.createElement('img');
    logoutImage.src = "../static/root/logout.svg";

    const logout = document.createElement('span');
    logout.addEventListener('click', () => {
        localStorage.removeItem('access_token');
        location.href = '/login';
    })

    logout.appendChild(logoutImage);
    logout.classList.add('logout');

    return logout;
}

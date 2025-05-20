import os
import requests
import time

# Инструкция как накидать картин в бд, читай комментарии сверху вниз

# В папку накидать изображений картин и тут указать путь папки, это делать один
# раз, в папке может быть хоть сколько картин. После того как картина добавляется
# в бд, она удаляется из папки.

PAINTINGS_DIR = r"C:\Users\admin\Desktop\fiit\Artloom\backend\domain\logic\test_paintings\images"

# Далее при каждом запуске программы:

# Сделать новый токен clarifai PAT и вставить его в backend/api_keys.py , после
# этого запустить api. На один токен максимум 1000 картин, поэтому если в папке
# картин больше, то надо несколько раз запускать программу с разными токенами.

# Сюда написать такой список из 33 уникальных артистов (эти уже юзаны)
new_artists = [
    {"rus": "Ян Ковальски", "eng": "JanKowalski"},
    {"rus": "Анна Новак", "eng": "AnnaNowak"},
    {"rus": "Кшиштоф Висневски", "eng": "KrzysztofWisniewski"},
    {"rus": "Мария Домбровска", "eng": "MariaDabrowska"},
    {"rus": "Пётр Левандовски", "eng": "PiotrLewandowski"},
    {"rus": "Агнешка Вуйцик", "eng": "AgnieszkaWojcik"},
    {"rus": "Томаш Каминьски", "eng": "TomaszKaminski"},
    {"rus": "Эва Завадска", "eng": "EwaZawadzka"},
    {"rus": "Михал Соколовски", "eng": "MichalSokolowski"},
    {"rus": "Катажина Козловска", "eng": "KatarzynaKozlowska"},
    {"rus": "Гжегож Яворски", "eng": "GrzegorzJaworski"},
    {"rus": "Барбара Врубель", "eng": "BarbaraWrobel"},
    {"rus": "Адам Малиновски", "eng": "AdamMalinowski"},
    {"rus": "Юстина Гурска", "eng": "JustynaGorska"},
    {"rus": "Марцин Зайонц", "eng": "MarcinZajac"},
    {"rus": "Ивона Борковска", "eng": "IwonaBorkowska"},
    {"rus": "Павел Домбровски", "eng": "PawelDabrowski"},
    {"rus": "Зофья Квятковска", "eng": "ZofiaKwiatkowska"},
    {"rus": "Рафал Ольшевски", "eng": "RafalOlszewski"},
    {"rus": "Малгожата Витковска", "eng": "MalgorzataWitkowska"},
    {"rus": "Дариуш Прушак", "eng": "DariuszPrusak"},
    {"rus": "Алиция Бартошек", "eng": "AlicjaBartoszek"},
    {"rus": "Станислав Вишневски", "eng": "StanislawWisniewski"},
    {"rus": "Беата Ковальчук", "eng": "BeataKowalczyk"},
    {"rus": "Аркадиуш Завада", "eng": "ArkadiuszZawada"},
    {"rus": "Ханна Сенкевич", "eng": "HannaSienkiewicz"},
    {"rus": "Лех Мазур", "eng": "LechMazur"},
    {"rus": "Моника Яскульска", "eng": "MonikaJaskulska"},
    {"rus": "Войцех Гурски", "eng": "WojciechGorski"},
    {"rus": "Эльжбета Вальчак", "eng": "ElzbietaWalczak"},
    {"rus": "Якуб Бжезински", "eng": "JakubBrzezinski"},
    {"rus": "Рената Круль", "eng": "RenataKrol"},
    {"rus": "Себастьян Лис", "eng": "SebastianLis"}
]


# Дальше можно ничего не менять, и запускать этот файл (api должно быть запущено на этот момент)









NUM_ARTISTS = len(new_artists)
if NUM_ARTISTS > 33:
    raise Exception("Артистов должно быть не больше 33, иначе токена clarifai "
                    "не хватит чтобы добавить все картины. "
                    "Токен максимум на 1000 изображений")


BASE_URL = "http://localhost:8000"
PASSWORD = "password123"

def get_avatar_url(idx):
    return f"https://storage.yandexcloud.net/artloom-storage/test_avatars/{idx % 56 + 1}.jpg"

def get_background_url(idx):
    return f"https://storage.yandexcloud.net/artloom-storage/test_backgrounds/{idx % 56 + 1}.jpg"


PAINTINGS_PER_ARTIST = 30

paintings_dir_empty = False
for idx, artist in enumerate(new_artists, start=1):
    if paintings_dir_empty:
        break

    login = artist["eng"]
    rus_name = artist["rus"]

    avatar_url = get_avatar_url(idx + 56)       # 57–86
    background_url = get_background_url(idx + 56)

    # 1. Регистрация аккаунта
    print(f"[{login}] Регистрируем аккаунт...")
    reg_resp = requests.post(
        f"{BASE_URL}/register/",
        json={"login": login, "password": PASSWORD, "avatar_img_path": avatar_url}
    )
    if reg_resp.status_code != 200:
        print(f"  Ошибка регистрации: {reg_resp.status_code} — {reg_resp.text}")
        continue

    # 2. Авторизация
    print(f"[{login}] Авторизуемся...")
    auth_resp = requests.post(
        f"{BASE_URL}/auth/",
        data={"username": login, "password": PASSWORD}
    )
    if auth_resp.status_code != 200:
        print(f"  Ошибка авторизации: {auth_resp.status_code} — {auth_resp.text}")
        continue
    token = auth_resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Создание объекта художника
    print(f"[{login}] Создаём профиль художника «{rus_name}»...")
    art_resp = requests.post(
        f"{BASE_URL}/artists/",
        json={"name": rus_name, "img_path": background_url, "description": ""},
        headers=headers
    )
    if art_resp.status_code != 200:
        print(f"  Ошибка создания artist: {art_resp.status_code} — {art_resp.text}")
        continue

    # 4. Загрузка и добавление картин
    print(f"[{login}] Начинаем загрузку {PAINTINGS_PER_ARTIST} картин...")
    for _ in range(PAINTINGS_PER_ARTIST):
        try:
            filename = next(f for f in os.listdir(PAINTINGS_DIR) if f.lower().endswith(('.jpg', '.png', '.jpeg')))
        except StopIteration:
            paintings_dir_empty = True
            print("  Файлы в папке закончились.")
            break

        local_path = os.path.join(PAINTINGS_DIR, filename)

        with open(local_path, "rb") as f:
            upload_resp = requests.post(
                f"{BASE_URL}/upload-photo/",
                files={"file": f}
            )
        if upload_resp.status_code != 200:
            print(f"  Ошибка загрузки {filename}: {upload_resp.status_code} — {upload_resp.text}")
            time.sleep(2)
            continue

        img_url = upload_resp.json().get("img_url")
        if not img_url:
            print(f"  В ответе нет img_url для {filename}")
            time.sleep(2)
            continue

        paint_resp = requests.post(
            f"{BASE_URL}/paintings/",
            json={"img_path": img_url, "description": ""},
            headers=headers
        )
        if paint_resp.status_code == 200:
            print(f"  Успешно добавлена картина: {filename}")
            os.remove(local_path)
        else:
            print(f"  Ошибка добавления {filename}: {paint_resp.status_code} — {paint_resp.text}")

        time.sleep(0.5)

    print(f"[{login}] Готово.\n")

print("Все новые художники и их картины обработаны!")

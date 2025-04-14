import os

def decrease_file_numbers(directory_path, decrease_by=9):
    # Получаем список всех файлов в директории
    files = os.listdir(directory_path)

    # Фильтруем только файлы с расширением .jpg
    jpg_files = [f for f in files if f.lower().endswith('.jpg')]

    # Сортируем файлы по числовому порядку
    jpg_files.sort(key=lambda x: int(x.split('.')[0]))

    # Переименовываем файлы
    for filename in jpg_files:
        # Получаем текущий номер файла
        current_number = int(filename.split('.')[0])

        # Вычисляем новый номер
        new_number = current_number - decrease_by

        # Если новый номер меньше или равен 0, пропускаем файл
        if new_number <= 0:
            print(f"Skipping '{filename}' as new number would be less than or equal to 0")
            continue

        # Формируем новое имя файла
        new_name = f"{new_number}.jpg"

        # Полные пути к старому и новому файлам
        old_file = os.path.join(directory_path, filename)
        new_file = os.path.join(directory_path, new_name)

        # Проверяем, существует ли файл с новым именем
        if not os.path.exists(new_file):
            # Переименовываем файл
            os.rename(old_file, new_file)
            print(f"Renamed '{filename}' to '{new_name}'")
        else:
            print(f"File '{new_name}' already exists. Skipping renaming for '{filename}'")

# Пример использования функции
directory_path = 'C:\\Users\\admin\\Desktop\\fiit\\Artloom\\backend\\domain\\logic\\test_paintings'
decrease_file_numbers(directory_path)

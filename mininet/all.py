import os

# Путь к директории output
output_dir = 'output'
# Имя итогового файла
combined_file_path = 'combined.dat'

# Открытие файла для записи результатов
with open(combined_file_path, 'w') as combined_file:
    # Проход по всем директориям и файлам
    for i in range(1, 41, 2): # Начиная с h1_to_h2 и до h39_to_h40
        # Формирование имени директории
        dir_name = f'h{i}_to_h{i+1}/results'
        # Путь к файлу в текущей директории
        file_path = os.path.join(output_dir, dir_name, '1.dat')

        # Проверка на существование файла
        if os.path.exists(file_path):
            # Чтение и запись содержимого файла
            with open(file_path, 'r') as file:
                combined_file.write(file.read())
        else:
            print(f'File {file_path} not found. Skipping.')

print(f'All files have been combined into {combined_file_path}')

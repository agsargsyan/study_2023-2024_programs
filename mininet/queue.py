import re
from main import iperf_time


def extract_numbers(s):
    """Извлекает числа из строки, включая отрицательные и дробные."""
    return re.findall(r'-?\d+\.?\d*', s)

def process_qdisc_data(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()

    # Разделение данных на блоки
    blocks = content.split('\n\n')  # Два переноса строки как разделитель блоков
    total_blocks = len([b for b in blocks if b.strip() != ""])  # Подсчет непустых блоков

    # Вычисление коэффициента масштабирования для индексов
    scale_factor = iperf_time / total_blocks if total_blocks > 0 else 0

    with open(output_file, 'w') as f:
        for i, block in enumerate(blocks):
            if block.strip() == "":  # Пропускаем пустые блоки
                continue
            numbers = extract_numbers(block)
            if len(numbers) > 5:  # Убедимся, что есть числа для пропуска
                numbers = numbers[5:]  # Пропускаем первые 5 чисел
            numbers_str = ' '.join(numbers)
            # Масштабирование индекса
            scaled_index = (i + 1) * scale_factor
            # Запись данных с масштабированным индексом и числами
            f.write(f'{scaled_index:.2f} {numbers_str}\n')

# Путь к входному файлу и выходному файлу
input_file = 'queue_monitor.txt'
output_file = 'queue.dat'

process_qdisc_data(input_file, output_file)


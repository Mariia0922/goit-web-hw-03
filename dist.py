import os
import shutil
import sys
import concurrent.futures
from multiprocessing import Process, Queue, cpu_count

def copy_files(source_dir, target_dir):
    """
    Функція для копіювання файлів з вихідної директорії в цільову.
    """
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_path = os.path.join(root, file)
            # Отримуємо розширення файлу
            _, ext = os.path.splitext(file)
            # Створюємо піддиректорію в цільовій директорії за розширенням
            target_subdir = os.path.join(target_dir, ext[1:])
            os.makedirs(target_subdir, exist_ok=True)
            target_path = os.path.join(target_subdir, file)
            # Копіюємо файл
            shutil.copy2(source_path, target_path)

def factorize(num, output_queue):
    """
    Функція, яка факторизує число та повертає результат через чергу.
    """
    factors = []
    for i in range(1, num + 1):
        if num % i == 0:
            factors.append(i)
    output_queue.put((num, factors))

def main_copy_and_factorize(source_dir, target_dir, numbers):
    """
    Основна функція для копіювання файлів та факторизації чисел.
    """
    # Копіюємо файли з вихідної директорії в цільову
    copy_files(source_dir, target_dir)

    # Створення черги для отримання результатів факторизації
    output_queue = Queue()

    # Створення та запуск процесів для факторизації чисел
    processes = []
    for num in numbers:
        process = Process(target=factorize, args=(num, output_queue))
        process.start()
        processes.append(process)

    # Очікування завершення процесів та виведення результатів
    for process in processes:
        process.join()

    # Отримання та виведення результатів з черги
    results = []
    while not output_queue.empty():
        results.append(output_queue.get())

    # Виведення результатів факторизації
    print("Результати факторизації:")
    for num, factors in results:
        print(f"{num}: {factors}")

if __name__ == "__main__":
    # Перевірка наявності аргументів командного рядка
    if len(sys.argv) < 2:
        print("Потрібно вказати шлях до директорії з файлами та числа для факторизації.")
        sys.exit(1)

    # Отримання аргументів командного рядка
    source_dir = sys.argv[1]
    target_dir = sys.argv[2] if len(sys.argv) > 2 else "dist"
    numbers = [int(arg) for arg in sys.argv[3:]]

    # Виклик основної функції програми
    main_copy_and_factorize(source_dir, target_dir, numbers)

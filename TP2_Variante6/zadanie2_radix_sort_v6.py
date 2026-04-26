# -*- coding: utf-8 -*-
# Лабораторная работа №2
# Вариант 6
# Задание 2: Поразрядная сортировка (Radix Sort)
# Студент: Тамекло Коку Эдмон
# Группа: МИС-25-1

def counting_sort_for_radix(arr, exp):
    """
    Вспомогательная функция: устойчивая сортировка подсчетом
    для определенного разряда (exp = 1, 10, 100, ...).
    
    Параметры:
        arr: список целых чисел
        exp: текущий разряд (1 - единицы, 10 - десятки, 100 - сотни, ...)
    
    Возвращает:
        список, отсортированный по текущему разряду
    """
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    # Подсчет количества элементов с каждой цифрой в текущем разряде
    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1
    
    # Изменение count[i] так, чтобы он содержал позицию следующего элемента
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Построение выходного массива (идем с конца для устойчивости)
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        count[digit] -= 1
        output[count[digit]] = arr[i]
    
    return output


def radix_sort(arr):
    """
    Поразрядная сортировка (Radix Sort) для целых неотрицательных чисел.
    
    Параметры:
        arr: список целых неотрицательных чисел
    
    Возвращает:
        отсортированный список
    """
    if not arr:
        return arr
    
    # Находим максимальное число для определения количества разрядов
    max_num = max(arr)
    
    # Показываем шаги
    print(f"Исходный массив: {arr}")
    print(f"Максимальное число: {max_num}")
    
    # Сортировка по каждому разряду
    exp = 1
    step = 1
    
    while max_num // exp > 0:
        arr = counting_sort_for_radix(arr, exp)
        print(f"Шаг {step} (разряд {exp}): {arr}")
        exp *= 10
        step += 1
    
    return arr


def radix_sort_with_negatives(arr):
    """
    Поразрядная сортировка для целых чисел (включая отрицательные).
    Отдельно сортирует отрицательные и неотрицательные числа.
    """
    if not arr:
        return arr
    
    # Разделяем на отрицательные и неотрицательные
    negative = [-x for x in arr if x < 0]
    non_negative = [x for x in arr if x >= 0]
    
    print(f"\nОтрицательные числа (по модулю): {negative}")
    print(f"Неотрицательные числа: {non_negative}")
    
    # Сортируем отдельно
    if negative:
        negative = radix_sort(negative)
        negative = [-x for x in reversed(negative)]
    
    if non_negative:
        non_negative = radix_sort(non_negative)
    
    return negative + non_negative


# =============================================
# ДЕМОНСТРАЦИЯ РАБОТЫ
# =============================================

print("=" * 60)
print("ЛАБОРАТОРНАЯ РАБОТА №2")
print("Вариант 6")
print("Задание 2: Поразрядная сортировка (Radix Sort)")
print("=" * 60)

# Тест 1: Неотрицательные числа
print("\n--- Тест 1: Неотрицательные числа ---")
arr1 = [170, 45, 75, 90, 802, 24, 2, 66]
print(f"\nИсходный массив: {arr1}")
sorted1 = radix_sort(arr1.copy())
print(f"\nОтсортированный массив: {sorted1}")
print(f"Проверка встроенной сортировкой: {sorted1 == sorted(arr1)}")

# Тест 2: Массив с повторяющимися числами
print("\n\n--- Тест 2: Повторяющиеся числа ---")
arr2 = [53, 89, 150, 36, 53, 633, 233, 150]
print(f"\nИсходный массив: {arr2}")
sorted2 = radix_sort(arr2.copy())
print(f"\nОтсортированный массив: {sorted2}")
print(f"Проверка встроенной сортировкой: {sorted2 == sorted(arr2)}")

# Тест 3: Короткий массив
print("\n\n--- Тест 3: Короткий массив ---")
arr3 = [9, 3, 7, 1, 5]
print(f"\nИсходный массив: {arr3}")
sorted3 = radix_sort(arr3.copy())
print(f"\nОтсортированный массив: {sorted3}")
print(f"Проверка встроенной сортировкой: {sorted3 == sorted(arr3)}")

# Тест 4: Массив из одного элемента
print("\n\n--- Тест 4: Один элемент ---")
arr4 = [42]
print(f"Исходный массив: {arr4}")
sorted4 = radix_sort(arr4.copy())
print(f"Отсортированный массив: {sorted4}")

# Тест 5: Пустой массив
print("\n\n--- Тест 5: Пустой массив ---")
arr5 = []
print(f"Исходный массив: {arr5}")
sorted5 = radix_sort(arr5.copy())
print(f"Отсортированный массив: {sorted5}")

print("\n" + "=" * 60)
print("Демонстрация завершена успешно!")
print("=" * 60)

input("\nНажмите Enter для выхода...")

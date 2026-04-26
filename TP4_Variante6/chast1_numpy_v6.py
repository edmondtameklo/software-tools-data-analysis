# -*- coding: utf-8 -*-
# Лабораторная работа №4 - Часть 1
# Инженерные и научные расчеты на базе NumPy
# Вариант 6 (N=6)
# Студент: Тамекло Коку Эдмон
# Группа: МИС-25-1

import numpy as np

print("=" * 60)
print("ЛАБОРАТОРНАЯ РАБОТА №4 - ЧАСТЬ 1")
print("NumPy - инженерные и научные расчеты")
print("Вариант 6 (N=6)")
print("=" * 60)

N = 6

# 1. Импортировать NumPy под именем np
print("\n1. NumPy импортирован как np")
print(f"   Версия NumPy: {np.__version__}")

# 2. Создать вектор размера N*10, заполненный нулями
print(f"\n2. Вектор размера {N}*10 = {N*10}, заполненный нулями:")
vec_zeros = np.zeros(N * 10)
print(f"   {vec_zeros}")
print(f"   Размер: {vec_zeros.size}")

# 3. Создать вектор размера 10, заполненный числом N
print(f"\n3. Вектор размера 10, заполненный числом {N}:")
vec_n = np.full(10, N)
print(f"   {vec_n}")

# 4. Создать вектор со значениями от N*5 до N*10
print(f"\n4. Вектор со значениями от {N}*5={N*5} до {N}*10={N*10}:")
vec_range = np.arange(N * 5, N * 10 + 1)
print(f"   {vec_range}")

# 5. Создать матрицу N*5 x N*5, заполнить числами (обязательно наличие нулей)
print(f"\n5. Матрица {N*5}x{N*5} со случайными числами (включая нули):")
np.random.seed(42)
mat = np.random.randint(-10, 10, size=(N*5, N*5))
print(f"   Размер матрицы: {mat.shape}")
print(f"   Количество нулей: {np.count_nonzero(mat == 0)}")
print(f"   Первые 5 строк:\n{mat[:5, :5]}...")

# 6. Найти индексы ненулевых элементов в матрице
print(f"\n6. Индексы ненулевых элементов в матрице:")
nonzero_indices = np.nonzero(mat)
print(f"   Количество ненулевых элементов: {len(nonzero_indices[0])}")
print(f"   Первые 10 индексов (строка, столбец):")
for i in range(min(10, len(nonzero_indices[0]))):
    print(f"   ({nonzero_indices[0][i]}, {nonzero_indices[1][i]})")

# 7. Создать случайный вектор размера N*15 и найти среднее значение
print(f"\n7. Случайный вектор размера {N}*15={N*15} и его среднее значение:")
vec_random = np.random.rand(N * 15)
mean_val = np.mean(vec_random)
print(f"   Среднее значение: {mean_val:.6f}")
print(f"   Минимум: {np.min(vec_random):.6f}")
print(f"   Максимум: {np.max(vec_random):.6f}")

# 8. Дан массив размерности (N*5, N*5, N*5). Индекс N*10 элемента
print(f"\n8. Массив размерности ({N*5}, {N*5}, {N*5}). Индекс {N}*10={N*10}-го элемента:")
arr_3d = np.arange(1, (N*5)**3 + 1).reshape(N*5, N*5, N*5)
flat_index = N * 10
# Индекс в плоском представлении
idx_3d = np.unravel_index(flat_index, arr_3d.shape)
print(f"   Индекс (x,y,z) для {N*10}-го элемента: {idx_3d}")
print(f"   Значение элемента: {arr_3d[idx_3d]}")

# 9. Создать две матрицы N*5 x N*3, умножить разными способами
print(f"\n9. Две матрицы {N*5}x{N*3}, перемножение разными способами:")
mat1 = np.random.randint(1, 10, size=(N*5, N*3))
mat2 = np.random.randint(1, 10, size=(N*5, N*3))
print(f"   Матрица 1: {mat1.shape}")
print(f"   Матрица 2: {mat2.shape}")

# Поэлементное умножение
elem_mult = mat1 * mat2
print(f"   Поэлементное умножение: {elem_mult.shape}")

# Матричное умножение (mat1 @ mat2.T)
mat_mult = mat1 @ mat2.T
print(f"   Матричное умножение (mat1 @ mat2.T): {mat_mult.shape}")

# Умножение через np.dot
dot_mult = np.dot(mat1, mat2.T)
print(f"   Умножение через np.dot: {dot_mult.shape}")

# 10. Отсортировать вектор из п.4 в обратном порядке
print(f"\n10. Вектор из п.4, отсортированный в обратном порядке:")
vec_reversed = np.sort(vec_range)[::-1]
print(f"   {vec_reversed}")

# 11. Функция, генерирующая два массива и проверяющая их на идентичность
print(f"\n11. Функция сравнения двух массивов:")
def compare_arrays():
    arr1 = np.random.randint(0, 10, size=5)
    arr2 = np.random.randint(0, 10, size=5)
    print(f"   Массив 1: {arr1}")
    print(f"   Массив 2: {arr2}")
    print(f"   Массивы одинаковы: {np.array_equal(arr1, arr2)}")
    return arr1, arr2

a1, a2 = compare_arrays()

# Ручная правка
print(f"   После ручной правки (a2 = a1.copy()):")
a2 = a1.copy()
print(f"   Массив 1: {a1}")
print(f"   Массив 2: {a2}")
print(f"   Массивы одинаковы: {np.array_equal(a1, a2)}")

# 12. Заменить максимальный элемент массива из п.7 на ноль
print(f"\n12. Замена максимального элемента массива из п.7 на ноль:")
vec_modified = vec_random.copy()
max_idx = np.argmax(vec_modified)
old_max = vec_modified[max_idx]
vec_modified[max_idx] = 0
print(f"   Старый максимум: {old_max:.6f} (индекс {max_idx})")
print(f"   Новый максимум: {np.max(vec_modified):.6f}")
print(f"   Проверка: на позиции {max_idx} теперь {vec_modified[max_idx]}")

# 13. Найти ближайшее к заданному значению число в массиве
print(f"\n13. Поиск ближайшего числа к заданному значению в массиве из п.5:")
target = 5
flat_mat = mat.flatten()
nearest_idx = np.argmin(np.abs(flat_mat - target))
nearest_val = flat_mat[nearest_idx]
print(f"   Заданное значение: {target}")
print(f"   Ближайшее число: {nearest_val}")
print(f"   Индекс в плоском массиве: {nearest_idx}")

# 14. Сформировать массив с распределением Гаусса
print(f"\n14. Массив с распределением Гаусса (нормальное распределение):")
gauss_arr = np.random.normal(loc=0, scale=1, size=100)
print(f"   Размер: {gauss_arr.size}")
print(f"   Среднее: {np.mean(gauss_arr):.6f}")
print(f"   Стандартное отклонение: {np.std(gauss_arr):.6f}")
print(f"   Первые 10 значений: {gauss_arr[:10]}")

# 15. Функция для определения диагональных элементов произведения матриц
print(f"\n15. Диагональные элементы произведения матриц:")
def diagonal_of_product(m1, m2):
    if m1.shape[1] != m2.shape[0]:
        m2 = m2.T
    prod = m1 @ m2
    diag = np.diag(prod)
    return diag

m_a = np.random.randint(1, 5, size=(4, 4))
m_b = np.random.randint(1, 5, size=(4, 4))
diag_result = diagonal_of_product(m_a, m_b)
print(f"   Матрица A:\n{m_a}")
print(f"   Матрица B:\n{m_b}")
print(f"   Диагональ A @ B: {diag_result}")

# 16. Найти наиболее частое и наименее частое значение матрицы из п.5
print(f"\n16. Наиболее и наименее частое значение в матрице из п.5:")
unique, counts = np.unique(mat, return_counts=True)
most_freq = unique[np.argmax(counts)]
least_freq = unique[np.argmin(counts)]
print(f"   Уникальные значения: {len(unique)}")
print(f"   Наиболее частое: {most_freq} (встречается {np.max(counts)} раз)")
print(f"   Наименее частое: {least_freq} (встречается {np.min(counts)} раз)")

# 17. Найти N наибольших и N наименьших значений
print(f"\n17. {N} наибольших и {N} наименьших значений в массиве:")
arr_for_extreme = np.random.randint(1, 1000, size=50)
n_largest = np.sort(arr_for_extreme)[-N:]
n_smallest = np.sort(arr_for_extreme)[:N]
print(f"   Массив: {arr_for_extreme}")
print(f"   {N} наибольших: {n_largest}")
print(f"   {N} наименьших: {n_smallest}")

# 18. Обработка прямоугольной матрицы A (N строк, N*2 столбцов)
print(f"\n18. Обработка матрицы A ({N}x{N*2}):")
mat_A = np.random.randint(-5, 5, size=(N, N*2))
print(f"   Исходная матрица A:\n{mat_A}")

# Подсчет нулей в строках и столбцах
zeros_rows = np.sum(mat_A == 0, axis=1)
zeros_cols = np.sum(mat_A == 0, axis=0)

print(f"   Нулей в каждой строке: {zeros_rows}")
print(f"   Нулей в каждом столбце: {zeros_cols}")

# Формирование результирующей матрицы (N+1) x (N*2+1)
result_mat = np.zeros((N+1, N*2+1), dtype=int)
result_mat[:N, :N*2] = mat_A
result_mat[:N, N*2] = zeros_rows
result_mat[N, :N*2] = zeros_cols
result_mat[N, N*2] = np.sum(zeros_rows)

print(f"\n   Результирующая матрица (N+1)x(N*2+1):")
print(f"   {result_mat}")
print(f"   Последний столбец - нули в строках")
print(f"   Последняя строка - нули в столбцах")

print("\n" + "=" * 60)
print("ЧАСТЬ 1 ЗАВЕРШЕНА!")
print("=" * 60)

input("\nНажмите Enter для выхода...")

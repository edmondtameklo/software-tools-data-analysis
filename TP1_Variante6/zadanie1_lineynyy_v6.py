# -*- coding: utf-8 -*-
# Лабораторная работа №1 - Часть 1
# Задание 1: Линейный алгоритм
# Вариант 6
# Студент: Тамекло Коку Эдмон
# Группа: МИС-25-1

import math

print("=" * 60)
print("ЗАДАНИЕ 1: ВЫЧИСЛЕНИЕ ФУНКЦИИ F(x)")
print("Вариант 6")
print("F = cos(1.5x) - e^(sin(x + 4/3)) + sqrt(x + 7/6)")
print("=" * 60)

x_str = input("\nВведите значение x (через точку, например 2.5): ")
x = float(x_str)

pod_kornem = x + 7.0/6.0
if pod_kornem < 0:
    print(f"\nОШИБКА: Под корнем отрицательное число ({pod_kornem:.4f} < 0)!")
    print("Программа завершена.")
    exit()

chast1 = math.cos(1.5 * x)
chast2 = math.exp(math.sin(x + 4.0/3.0))
chast3 = math.sqrt(pod_kornem)

F = chast1 - chast2 + chast3

print("\n--- Пошаговое вычисление ---")
print(f"1) cos(1.5 * {x}) = cos({1.5 * x:.4f}) = {chast1:.6f}")
print(f"2) e^(sin({x} + 4/3)) = e^(sin({x + 4.0/3.0:.4f})) = e^({math.sin(x + 4.0/3.0):.6f}) = {chast2:.6f}")
print(f"3) sqrt({x} + 7/6) = sqrt({pod_kornem:.4f}) = {chast3:.6f}")
print("\n--- Результат ---")
print(f"F({x}) = {chast1:.6f} - {chast2:.6f} + {chast3:.6f} = {F:.6f}")

print("\n--- Контрольные точки ---")
test_x = [0.0, 1.0, -0.5]
for tx in test_x:
    pk = tx + 7.0/6.0
    if pk >= 0:
        F_test = math.cos(1.5 * tx) - math.exp(math.sin(tx + 4.0/3.0)) + math.sqrt(pk)
        print(f"F({tx}) = {F_test:.6f}")

input("\nНажмите Enter для выхода...")

# -*- coding: utf-8 -*-
# Лабораторная работа №1 - Часть 1
# Задание 2: Условный оператор
# Вариант 6
# Студент: Тамекло Коку Эдмон
# Группа: МИС-25-1

print("=" * 60)
print("ЗАДАНИЕ 2: ВЫЧИСЛЕНИЕ КУСОЧНОЙ ФУНКЦИИ")
print("Вариант 6")
print("=" * 60)

x_str = input("\nВведите значение x: ")
x = float(x_str)

print(f"\n--- Определение условия для x = {x} ---")

if x < -9:
    print(f"x = {x} < -9")
    print("Используется формула: y = 13x^3 + 71")
    x3 = x ** 3
    y = 13 * x3 + 71
    print(f"  1) {x}^3 = {x3:.4f}")
    print(f"  2) 13 * {x3:.4f} = {13 * x3:.4f}")
    print(f"  3) {13 * x3:.4f} + 71 = {y:.4f}")

elif -9 <= x <= 17:
    print(f"x = {x} находится в диапазоне [-9; 17]")
    print("Используется формула: y = 7x^4 - 15x + 25")
    x4 = x ** 4
    chast1 = 7 * x4
    chast2 = -15 * x
    chast3 = 25
    y = chast1 + chast2 + chast3
    print(f"  1) {x}^4 = {x4:.4f}  →  7 * {x4:.4f} = {chast1:.4f}")
    print(f"  2) -15 * {x} = {chast2:.4f}")
    print(f"  3) Константа: 25")
    print(f"  4) Сумма: {chast1:.4f} + ({chast2:.4f}) + 25 = {y:.4f}")

else:
    print(f"x = {x} > 17")
    print("Используется формула: y = (6/33)x^2 - x + 41")
    x2 = x ** 2
    chast1 = (6.0 / 33.0) * x2
    chast2 = -x
    chast3 = 41
    y = chast1 + chast2 + chast3
    print(f"  1) {x}^2 = {x2:.4f}  →  (6/33) * {x2:.4f} = {chast1:.4f}")
    print(f"  2) -x = {chast2:.4f}")
    print(f"  3) Константа: 41")
    print(f"  4) Сумма: {chast1:.4f} + ({chast2:.4f}) + 41 = {y:.4f}")

print(f"\n--- Результат ---")
print(f"y({x}) = {y:.6f}")

print("\n--- Демонстрация для разных значений x ---")
test_x = [-10.0, 0.0, 20.0]
for tx in test_x:
    if tx < -9:
        y_test = 13 * tx**3 + 71
    elif -9 <= tx <= 17:
        y_test = 7 * tx**4 - 15 * tx + 25
    else:
        y_test = (6.0/33.0) * tx**2 - tx + 41
    print(f"x = {tx:5.1f}  →  y = {y_test:.2f}")

input("\nНажмите Enter для выхода...")

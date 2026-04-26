# -*- coding: utf-8 -*-
# Лабораторная работа №1 - Часть 1
# Задание 3: Цикл
# Вариант 6
# Студент: Тамекло Коку Эдмон
# Группа: МИС-25-1

print("=" * 60)
print("ЗАДАНИЕ 3: ТАБУЛИРОВАНИЕ ФУНКЦИИ")
print("Вариант 6")
print("=" * 60)

x_nachalo = 6.0
x_konec = 13.0
shag = 2.0

print(f"\nПараметры вычислений:")
print(f"  Диапазон: [{x_nachalo}; {x_konec}]")
print(f"  Шаг h: {shag}")
print(f"  Функция: y = x^2 / (8x)")

print("\n--- Таблица значений ---")
print("-" * 45)
print(f"{'x':<12} {'x^2':<12} {'8x':<12} {'y = x^2/(8x)':<15}")
print("-" * 45)

x = x_nachalo
nomer_stroki = 1

while x <= x_konec + 0.0001:
    x2 = x ** 2
    vosem_x = 8 * x
    y = x2 / vosem_x
    
    print(f"{x:<12.1f} {x2:<12.2f} {vosem_x:<12.2f} {y:<15.4f}")
    
    x = x + shag
    nomer_stroki = nomer_stroki + 1

print("-" * 45)
print(f"Всего вычислено точек: {nomer_stroki - 1}")

print("\n--- Проверка (упрощенная формула) ---")
print("Так как x^2/(8x) = x/8 при x ≠ 0:")
print("-" * 30)
x = x_nachalo
while x <= x_konec + 0.0001:
    y_proverka = x / 8
    print(f"x = {x:<5.1f}  →  x/8 = {y_proverka:.4f}")
    x = x + shag
print("-" * 30)

input("\nНажмите Enter для выхода...")

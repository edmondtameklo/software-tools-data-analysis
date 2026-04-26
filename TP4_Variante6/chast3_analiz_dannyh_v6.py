# -*- coding: utf-8 -*-
# Лабораторная работа №4 - Часть 3
# Обработка и анализ данных в Python
# Вариант 6: Договоры продажи
# Студент: Тамекло Коку Эдмон
# Группа: МИС-25-1

import pandas as pd
import numpy as np
import os

print("=" * 60)
print("ЛАБОРАТОРНАЯ РАБОТА №4 - ЧАСТЬ 3")
print("Обработка и анализ данных")
print("Вариант 6: Договоры продажи")
print("=" * 60)

# =============================================
# ЗАГРУЗКА ДАННЫХ
# =============================================

print("\n--- Загрузка данных ---")

filename = None
for f in ['Договоры_продажи.csv', 'dogovory.csv', 'online_sales.csv']:
    if os.path.exists(f):
        filename = f
        break

if filename is None:
    print("Файл с данными не найден!")
    print("Поместите файл в папку TP4_Variante6")
    input("\nНажмите Enter для выхода...")
    exit()

df = None
encodings = ['utf-8', 'windows-1251', 'cp1251', 'latin-1']
separators = [';', ',']

for enc in encodings:
    for sep in separators:
        try:
            df = pd.read_csv(filename, encoding=enc, sep=sep,
                           on_bad_lines='skip', engine='python')
            print(f"✓ Загружен: {filename} (кодировка: {enc}, разделитель: '{sep}')")
            break
        except:
            continue
    if df is not None:
        break

if df is None:
    print("Не удалось загрузить CSV. Проверьте файл!")
    input("\nНажмите Enter для выхода...")
    exit()

print(f"Загружено записей: {len(df)}")
print(f"Исходные колонки: {list(df.columns)}")

# =============================================
# ПЕРЕИМЕНОВАНИЕ КОЛОНОК
# =============================================

# Si les colonnes ont des noms standard, on les garde
# Sinon, on utilise la position
expected_cols = ['Товар', 'Единица_измерения', 'Количество_в_упаковке',
                 'Группа_товаров', 'Количество', 'Цена', 'Предоплата',
                 'Продавец', 'Город', 'Банк']

if len(df.columns) == 10:
    df.columns = expected_cols
    print(f"Колонки переименованы: {list(df.columns)}")
elif len(df.columns) > 10:
    df = df.iloc[:, :10]
    df.columns = expected_cols
    print(f"Взяты первые 10 колонок: {list(df.columns)}")

# Conversion en nombres
if 'Количество' in df.columns:
    df['Количество'] = pd.to_numeric(df['Количество'], errors='coerce').fillna(0)
if 'Цена' in df.columns:
    df['Цена'] = pd.to_numeric(df['Цена'], errors='coerce').fillna(0)
if 'Предоплата' in df.columns:
    df['Предоплата'] = pd.to_numeric(df['Предоплата'], errors='coerce').fillna(0)

# Colonne Сумма
df['Сумма'] = df['Количество'] * df['Цена']

# Supprimer lignes vides
df = df.dropna(subset=['Товар'])
df = df[df['Товар'].astype(str).str.strip() != '']

print(f"Записей после очистки: {len(df)}")
print(f"\nПервые 5 строк:")
print(df.head())

# =============================================
# 1. СОРТИРОВКА
# =============================================

print("\n" + "=" * 50)
print("1. СОРТИРОВКА ДАННЫХ")
print("=" * 50)

# 1.1
print("\n--- Сортировка 1: Товар, Город ---")
sorted1 = df.sort_values(['Товар', 'Город'])
cols_show = ['Товар', 'Город', 'Продавец', 'Количество', 'Цена', 'Сумма']
print(sorted1[cols_show].head(15))
sorted1.to_csv('sort_tovar_gorod.csv', index=False, encoding='utf-8')
print("✓ Сохранено в sort_tovar_gorod.csv")

# 1.2
print("\n--- Сортировка 2: Товар, Продавец, Единица_измерения ---")
sorted2 = df.sort_values(['Товар', 'Продавец', 'Единица_измерения'])
print(sorted2[['Товар', 'Продавец', 'Единица_измерения', 'Количество', 'Цена']].head(15))
sorted2.to_csv('sort_tovar_prodavec_edizm.csv', index=False, encoding='utf-8')
print("✓ Сохранено в sort_tovar_prodavec_edizm.csv")

# =============================================
# 2. ИТОГИ
# =============================================

print("\n" + "=" * 50)
print("2. ИТОГИ: КОЛИЧЕСТВО ПРОДАННЫХ ТОВАРОВ ПО ГОРОДАМ")
print("=" * 50)

itogi_gorod = df.groupby('Город').agg(
    Общее_количество=('Количество', 'sum'),
    Общая_сумма=('Сумма', 'sum'),
    Число_продаж=('Товар', 'count')
).round(2).sort_values('Общее_количество', ascending=False)

print(itogi_gorod)
itogi_gorod.to_csv('itogi_po_gorodam.csv', encoding='utf-8')
print("✓ Сохранено в itogi_po_gorodam.csv")

# =============================================
# 3. ФИЛЬТРЫ
# =============================================

print("\n" + "=" * 50)
print("3. ФИЛЬТРЫ")
print("=" * 50)

# 3.1
print("\n--- Фильтр 1: Топ-10 максимальных по сумме продаж ---")
top10 = df.nlargest(10, 'Сумма')
print(top10[cols_show])
top10.to_csv('top10_max_sales.csv', index=False, encoding='utf-8')
print("✓ Сохранено в top10_max_sales.csv")

# 3.2
print("\n--- Фильтр 2: Продажи с банком Богатырский или Надежный ---")
filter_bank = df[df['Банк'].astype(str).str.contains('Богатырский|Надежный', case=False, na=False)]
print(f"Найдено: {len(filter_bank)} из {len(df)} ({len(filter_bank)/len(df)*100:.1f}%)")
print(filter_bank[['Товар', 'Город', 'Банк', 'Сумма']].head(10))
filter_bank.to_csv('filter_banki.csv', index=False, encoding='utf-8')
print("✓ Сохранено в filter_banki.csv")

# =============================================
# 4. ОТЧЕТЫ
# =============================================

print("\n" + "=" * 50)
print("4. ОТЧЕТЫ")
print("=" * 50)

# 4.1
print("\n--- Отчет 1: Количество проданных круп в Иркутске ---")
krupy_irkutsk = df[(df['Город'].astype(str) == 'Иркутск') &
                    (df['Группа_товаров'].astype(str).str.contains('Круп', case=False, na=False))]
total_krupy = krupy_irkutsk['Количество'].sum()
print(f"Общее количество круп в Иркутске: {total_krupy}")
print(f"Общая сумма: {krupy_irkutsk['Сумма'].sum():.2f}")
print(f"Сделок: {len(krupy_irkutsk)}")
print("\nПо товарам:")
krupy_detail = krupy_irkutsk.groupby('Товар').agg(
    Количество=('Количество', 'sum'),
    Сумма=('Сумма', 'sum')
).sort_values('Количество', ascending=False)
print(krupy_detail)
krupy_detail.to_csv('otchet_krupy_irkutsk.csv', encoding='utf-8')
print("✓ Сохранено в otchet_krupy_irkutsk.csv")

# 4.2
print("\n--- Отчет 2: Сумма продаж организации Единство ---")
edinstvo = df[df['Продавец'].astype(str) == 'Единство']
sum_edinstvo = edinstvo['Сумма'].sum()
print(f"Общая сумма продаж Единства: {sum_edinstvo:.2f}")
print(f"Сделок: {len(edinstvo)}")
print("\nПо городам:")
edinstvo_gorod = edinstvo.groupby('Город').agg(
    Количество=('Количество', 'sum'),
    Сумма=('Сумма', 'sum')
).sort_values('Сумма', ascending=False)
print(edinstvo_gorod)
edinstvo_gorod.to_csv('otchet_edinstvo.csv', encoding='utf-8')
print("✓ Сохранено в otchet_edinstvo.csv")

# 4.3
print("\n--- Отчет 3: Продажи в разрезе товара и фирмы ---")
tovar_firma = df.groupby(['Товар', 'Продавец']).agg(
    Всего_количество=('Количество', 'sum'),
    Общая_сумма=('Сумма', 'sum'),
    Число_продаж=('Товар', 'count')
).sort_values('Всего_количество', ascending=False)

print(f"Комбинаций товар-фирма: {len(tovar_firma)}")
print("\nТоп-20:")
print(tovar_firma.head(20))
tovar_firma.to_csv('otchet_tovar_firma.csv', encoding='utf-8')
print("✓ Сохранено в otchet_tovar_firma.csv")

# =============================================
# 5. ОБЩАЯ СТАТИСТИКА
# =============================================

print("\n" + "=" * 50)
print("5. ОБЩАЯ СТАТИСТИКА")
print("=" * 50)

print(f"\nЗаписей: {len(df)}")
print(f"Единиц продано: {df['Количество'].sum():.0f}")
print(f"Общая сумма: {df['Сумма'].sum():.2f} руб")
print(f"Средняя цена: {df['Цена'].mean():.2f} руб")
print(f"Городов: {df['Город'].nunique()} - {list(df['Город'].unique())}")
print(f"Продавцов: {df['Продавец'].nunique()} - {list(df['Продавец'].unique())}")
print(f"Банков: {df['Банк'].nunique()} - {list(df['Банк'].unique())}")

print("\nГруппы товаров:")
gruppy = df.groupby('Группа_товаров').agg(
    Количество=('Количество', 'sum'),
    Сумма=('Сумма', 'sum')
).sort_values('Сумма', ascending=False)
print(gruppy)

print("\n" + "=" * 60)
print("АНАЛИЗ ЗАВЕРШЕН!")
print("Все отчеты сохранены в CSV-файлы")
print("=" * 60)

input("\nНажмите Enter для выхода...")

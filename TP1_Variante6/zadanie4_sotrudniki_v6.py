# -*- coding: utf-8 -*-
# Лабораторная работа №1 - Часть 2
# Работа с файлами
# Вариант 6: Информация о сотрудниках фирмы
# Студент: Тамекло Коку Эдмон
# Группа: МИС-25-1

import os

IMYA_FILA = "sotrudniki.txt"
RAZDELITEL = "|"

def prochitat_fayl():
    """Читает данные сотрудников из файла."""
    sotrudniki = []
    if not os.path.exists(IMYA_FILA):
        return sotrudniki
    with open(IMYA_FILA, 'r', encoding='utf-8') as f:
        for stroka in f:
            stroka = stroka.strip()
            if stroka:
                chasti = stroka.split(RAZDELITEL)
                if len(chasti) == 4:
                    sotrudniki.append({
                        'fio': chasti[0],
                        'tabel': chasti[1],
                        'chasy': float(chasti[2]),
                        'tarif': float(chasti[3])
                    })
    return sotrudniki

def zapisat_fayl(sotrudniki):
    """Записывает данные сотрудников в файл."""
    with open(IMYA_FILA, 'w', encoding='utf-8') as f:
        for s in sotrudniki:
            stroka = RAZDELITEL.join([
                s['fio'], s['tabel'],
                str(s['chasy']), str(s['tarif'])
            ])
            f.write(stroka + '\n')

def rasschitat_zarplatu(chasy, tarif):
    """Рассчитывает зарплату с учетом сверхурочных."""
    if chasy <= 144:
        return chasy * tarif
    else:
        sverhurochnye = chasy - 144
        return 144 * tarif + sverhurochnye * tarif * 2

def dobavit_sotrudnika():
    """Добавляет нового сотрудника."""
    print("\n" + "=" * 50)
    print("ДОБАВЛЕНИЕ НОВОГО СОТРУДНИКА")
    print("=" * 50)
    
    fio = input("Введите Ф.И.О.: ")
    tabel = input("Введите табельный номер: ")
    
    try:
        chasy = float(input("Введите количество отработанных часов: "))
        tarif = float(input("Введите почасовой тариф (руб/час): "))
    except ValueError:
        print("Ошибка: часы и тариф должны быть числами!")
        return
    
    sotrudniki = prochitat_fayl()
    sotrudniki.append({
        'fio': fio, 'tabel': tabel,
        'chasy': chasy, 'tarif': tarif
    })
    zapisat_fayl(sotrudniki)
    
    zarplata = rasschitat_zarplatu(chasy, tarif)
    print(f"\nСотрудник успешно добавлен!")
    print(f"  Ф.И.О.: {fio}")
    print(f"  Табельный номер: {tabel}")
    print(f"  Отработано часов: {chasy:.1f}")
    print(f"  Почасовой тариф: {tarif:.2f} руб/час")
    print(f"  Рассчитанная зарплата: {zarplata:.2f} руб")

def udalit_sotrudnika():
    """Удаляет сотрудника по номеру."""
    sotrudniki = prochitat_fayl()
    
    if not sotrudniki:
        print("\nСписок сотрудников пуст! Удалять нечего.")
        return
    
    pokazat_spisok()
    
    try:
        nomer = int(input(f"\nВведите номер сотрудника для удаления (1-{len(sotrudniki)}): "))
        if 1 <= nomer <= len(sotrudniki):
            udalennyy = sotrudniki.pop(nomer - 1)
            zapisat_fayl(sotrudniki)
            print(f"\nСотрудник успешно удален:")
            print(f"  {udalennyy['fio']} (таб. №{udalennyy['tabel']})")
        else:
            print(f"Ошибка: введите число от 1 до {len(sotrudniki)}")
    except ValueError:
        print("Ошибка: введите корректный номер!")

def pokazat_spisok():
    """Выводит список всех сотрудников."""
    sotrudniki = prochitat_fayl()
    
    if not sotrudniki:
        print("\nСписок сотрудников пуст!")
        return
    
    print("\n" + "=" * 95)
    print("СПИСОК СОТРУДНИКОВ ФИРМЫ")
    print("=" * 95)
    zagolovok = f"{'№':<4} {'Ф.И.О.':<25} {'Таб.№':<8} {'Часы':<8} {'Тариф':<10} {'Зарплата':<12} {'Сверхурочно':<12}"
    print(zagolovok)
    print("-" * 95)
    
    obshaya_zarplata = 0
    obshie_chasy = 0
    
    for i, s in enumerate(sotrudniki, 1):
        zarplata = rasschitat_zarplatu(s['chasy'], s['tarif'])
        obshaya_zarplata += zarplata
        obshie_chasy += s['chasy']
        
        sverh = ""
        if s['chasy'] > 144:
            sverh = f"{s['chasy'] - 144:.1f} ч"
        else:
            sverh = "нет"
        
        print(f"{i:<4} {s['fio']:<25} {s['tabel']:<8} {s['chasy']:<8.1f} "
              f"{s['tarif']:<10.2f} {zarplata:<12.2f} {sverh:<12}")
    
    print("-" * 95)
    print(f"ИТОГО: {len(sotrudniki)} сотрудников | {obshie_chasy:.1f} часов | {obshaya_zarplata:.2f} руб")
    print("=" * 95)

def inicializaciya_demo():
    """Создает демо-данные при первом запуске."""
    if not os.path.exists(IMYA_FILA):
        print("\nПервый запуск программы!")
        print("Создаю файл с демонстрационными данными...")
        demo = [
            {'fio': 'Иванов Иван Иванович', 'tabel': '001',
             'chasy': 160.0, 'tarif': 250.0},
            {'fio': 'Петрова Анна Сергеевна', 'tabel': '002',
             'chasy': 140.0, 'tarif': 300.0},
            {'fio': 'Сидоров Петр Алексеевич', 'tabel': '003',
             'chasy': 200.0, 'tarif': 200.0}
        ]
        zapisat_fayl(demo)
        print("Добавлено 3 сотрудника!\n")

def glavnoe_menu():
    """Отображает главное меню программы."""
    while True:
        print("\n" + "=" * 45)
        print("=== ГЛАВНОЕ МЕНЮ - УЧЕТ СОТРУДНИКОВ ===")
        print("Вариант 6")
        print("=" * 45)
        print("1 - Показать всех сотрудников")
        print("2 - Добавить нового сотрудника")
        print("3 - Удалить сотрудника")
        print("4 - Выход из программы")
        print("-" * 45)
        
        vybor = input("Ваш выбор (1-4): ")
        
        if vybor == '1':
            pokazat_spisok()
        elif vybor == '2':
            dobavit_sotrudnika()
        elif vybor == '3':
            udalit_sotrudnika()
        elif vybor == '4':
            print("\nПрограмма завершена. До свидания!")
            break
        else:
            print("\nОшибка! Введите число от 1 до 4.")

# ========================================
# ЗАПУСК ПРОГРАММЫ
# ========================================
print("=" * 60)
print("ПРОГРАММА УЧЕТА СОТРУДНИКОВ ФИРМЫ")
print("Вариант 6")
print("Правило: сверхурочные (свыше 144 ч) оплачиваются вдвойне")
print("=" * 60)

inicializaciya_demo()
glavnoe_menu()

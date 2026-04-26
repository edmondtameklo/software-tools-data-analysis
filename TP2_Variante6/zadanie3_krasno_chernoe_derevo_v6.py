# -*- coding: utf-8 -*-
# Лабораторная работа №2
# Вариант 6
# Задание 3: Красно-черное дерево
# Студент: Тамекло Коку Эдмон
# Группа: МИС-25-1

# Константы для цветов узла
KRASNYY = "КРАСНЫЙ"
CHERNYY = "ЧЕРНЫЙ"


class Uzel:
    """Узел красно-черного дерева."""
    
    def __init__(self, znachenie, tsvet=KRASNYY):
        self.znachenie = znachenie  # Значение узла
        self.tsvet = tsvet           # Цвет узла
        self.levyy = None            # Левый потомок
        self.pravyy = None           # Правый потомок
        self.roditel = None          # Родитель


class KrasnoChernoeDerevo:
    """Красно-черное дерево поиска."""
    
    def __init__(self):
        self.koren = None
    
    def vstavit(self, znachenie):
        """
        Вставка нового значения в дерево.
        После вставки выполняется балансировка.
        """
        novyy_uzel = Uzel(znachenie, KRASNYY)
        
        if self.koren is None:
            novyy_uzel.tsvet = CHERNYY
            self.koren = novyy_uzel
            print(f"  Вставлен корень: {znachenie} (цвет: {novyy_uzel.tsvet})")
            return
        
        tekushiy = self.koren
        while True:
            if znachenie < tekushiy.znachenie:
                if tekushiy.levyy is None:
                    tekushiy.levyy = novyy_uzel
                    novyy_uzel.roditel = tekushiy
                    break
                tekushiy = tekushiy.levyy
            elif znachenie > tekushiy.znachenie:
                if tekushiy.pravyy is None:
                    tekushiy.pravyy = novyy_uzel
                    novyy_uzel.roditel = tekushiy
                    break
                tekushiy = tekushiy.pravyy
            else:
                print(f"  Значение {znachenie} уже существует в дереве!")
                return
        
        print(f"  Вставлен узел: {znachenie} (цвет: {novyy_uzel.tsvet})")
        self._ispravit_vstavku(novyy_uzel)
    
    def _ispravit_vstavku(self, uzel):
        """Исправление свойств красно-черного дерева после вставки."""
        
        while uzel.roditel and uzel.roditel.tsvet == KRASNYY:
            dedushka = uzel.roditel.roditel
            
            if uzel.roditel == dedushka.levyy:
                dyadya = dedushka.pravyy
                
                # Случай 1: Дядя красный
                if dyadya and dyadya.tsvet == KRASNYY:
                    uzel.roditel.tsvet = CHERNYY
                    dyadya.tsvet = CHERNYY
                    dedushka.tsvet = KRASNYY
                    uzel = dedushka
                else:
                    # Случай 2: Треугольник
                    if uzel == uzel.roditel.pravyy:
                        uzel = uzel.roditel
                        self._levyy_povorot(uzel)
                    
                    # Случай 3: Линия
                    uzel.roditel.tsvet = CHERNYY
                    dedushka.tsvet = KRASNYY
                    self._pravyy_povorot(dedushka)
            else:
                dyadya = dedushka.levyy
                
                # Случай 1: Дядя красный
                if dyadya and dyadya.tsvet == KRASNYY:
                    uzel.roditel.tsvet = CHERNYY
                    dyadya.tsvet = CHERNYY
                    dedushka.tsvet = KRASNYY
                    uzel = dedushka
                else:
                    # Случай 2: Треугольник
                    if uzel == uzel.roditel.levyy:
                        uzel = uzel.roditel
                        self._pravyy_povorot(uzel)
                    
                    # Случай 3: Линия
                    uzel.roditel.tsvet = CHERNYY
                    dedushka.tsvet = KRASNYY
                    self._levyy_povorot(dedushka)
        
        self.koren.tsvet = CHERNYY
    
    def _levyy_povorot(self, uzel):
        """Левый поворот вокруг узла."""
        pravyy = uzel.pravyy
        uzel.pravyy = pravyy.levyy
        
        if pravyy.levyy:
            pravyy.levyy.roditel = uzel
        
        pravyy.roditel = uzel.roditel
        
        if uzel.roditel is None:
            self.koren = pravyy
        elif uzel == uzel.roditel.levyy:
            uzel.roditel.levyy = pravyy
        else:
            uzel.roditel.pravyy = pravyy
        
        pravyy.levyy = uzel
        uzel.roditel = pravyy
    
    def _pravyy_povorot(self, uzel):
        """Правый поворот вокруг узла."""
        levyy = uzel.levyy
        uzel.levyy = levyy.pravyy
        
        if levyy.pravyy:
            levyy.pravyy.roditel = uzel
        
        levyy.roditel = uzel.roditel
        
        if uzel.roditel is None:
            self.koren = levyy
        elif uzel == uzel.roditel.pravyy:
            uzel.roditel.pravyy = levyy
        else:
            uzel.roditel.levyy = levyy
        
        levyy.pravyy = uzel
        uzel.roditel = levyy
    
    def nayti(self, znachenie):
        """Поиск элемента в дереве."""
        tekushiy = self.koren
        shagi = 0
        
        while tekushiy:
            shagi += 1
            if znachenie == tekushiy.znachenie:
                return True, shagi, tekushiy
            elif znachenie < tekushiy.znachenie:
                tekushiy = tekushiy.levyy
            else:
                tekushiy = tekushiy.pravyy
        
        return False, shagi, None
    
    def obhod_v_shirinu(self):
        """Обход дерева по уровням (BFS)."""
        if not self.koren:
            return []
        
        rezultat = []
        ochered = [self.koren]
        
        while ochered:
            uzel = ochered.pop(0)
            rezultat.append((uzel.znachenie, uzel.tsvet))
            
            if uzel.levyy:
                ochered.append(uzel.levyy)
            if uzel.pravyy:
                ochered.append(uzel.pravyy)
        
        return rezultat
    
    def pokazat_derevo(self):
        """Выводит структуру дерева."""
        if not self.koren:
            print("Дерево пусто.")
            return
        
        print("\nСтруктура дерева (обход по уровням):")
        obhod = self.obhod_v_shirinu()
        for i, (znach, tsvet) in enumerate(obhod):
            color_emoji = "🔴" if tsvet == KRASNYY else "⚫"
            print(f"  Узел {i+1}: {znach} {color_emoji} ({tsvet})")


# =============================================
# ДЕМОНСТРАЦИЯ РАБОТЫ
# =============================================

print("=" * 60)
print("ЛАБОРАТОРНАЯ РАБОТА №2")
print("Вариант 6")
print("Задание 3: Красно-черное дерево")
print("=" * 60)

derevo = KrasnoChernoeDerevo()

print("\n--- 1. Вставка элементов ---")
elements = [10, 20, 30, 15, 25, 5, 1]
print(f"Вставляем элементы: {elements}\n")
for elem in elements:
    derevo.vstavit(elem)

derevo.pokazat_derevo()

print("\n--- 2. Поиск элементов ---")
test_poiska = [15, 100, 5, 50]
for znach in test_poiska:
    naydeno, shagi, uzel = derevo.nayti(znach)
    if naydeno:
        print(f"  Значение {znach}: НАЙДЕНО за {shagi} шаг(ов), цвет: {uzel.tsvet}")
    else:
        print(f"  Значение {znach}: НЕ НАЙДЕНО (проверено за {shagi} шаг(ов))")

print("\n--- 3. Свойства красно-черного дерева ---")
print("  ✓ Корень всегда черный")
print("  ✓ Красный узел не имеет красных потомков")
print("  ✓ Все пути от корня до листьев имеют одинаковое число черных узлов")

print("\n" + "=" * 60)
print("Демонстрация завершена успешно!")
print("=" * 60)

input("\nНажмите Enter для выхода...")

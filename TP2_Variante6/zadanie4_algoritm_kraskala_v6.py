# -*- coding: utf-8 -*-
# Лабораторная работа №2
# Вариант 6
# Задание 4: Алгоритм Краскала
# Студент: Тамекло Коку Эдмон
# Группа: МИС-25-1

class UnionFind:
    """
    Система непересекающихся множеств (Disjoint Set Union).
    Используется для проверки принадлежности вершин к одному множеству.
    """
    
    def __init__(self, n):
        self.roditel = list(range(n))
        self.rang = [0] * n
    
    def nayti(self, x):
        """Находит представителя множества, содержащего x (с сжатием пути)."""
        if self.roditel[x] != x:
            self.roditel[x] = self.nayti(self.roditel[x])
        return self.roditel[x]
    
    def obedinit(self, x, y):
        """Объединяет множества, содержащие x и y."""
        koren_x = self.nayti(x)
        koren_y = self.nayti(y)
        
        if koren_x == koren_y:
            return False
        
        if self.rang[koren_x] < self.rang[koren_y]:
            self.roditel[koren_x] = koren_y
        elif self.rang[koren_x] > self.rang[koren_y]:
            self.roditel[koren_y] = koren_x
        else:
            self.roditel[koren_y] = koren_x
            self.rang[koren_x] += 1
        
        return True


def algoritm_kraskala(vershiny, rebra):
    """
    Алгоритм Краскала для поиска минимального остовного дерева.
    
    Параметры:
        vershiny: список вершин графа
        rebra: список ребер в формате (ves, u, v), где ves - вес, u и v - вершины
    
    Возвращает:
        (minimalnye_rebra, obshiy_ves) - список ребер МОД и общий вес
    """
    if not rebra:
        return [], 0
    
    n = len(vershiny)
    
    # Словарь для сопоставления вершин с индексами
    vershina_v_index = {v: i for i, v in enumerate(vershiny)}
    
    # Сортируем ребра по весу (от меньшего к большему)
    sortirovannye_rebra = sorted(rebra, key=lambda x: x[0])
    
    print("\nШаг 1: Сортировка ребер по весу:")
    for i, (ves, u, v) in enumerate(sortirovannye_rebra):
        print(f"  {i+1}. {u} --({ves})-- {v}")
    
    uf = UnionFind(n)
    minimalnye_rebra = []
    obshiy_ves = 0
    
    print("\nШаг 2: Построение минимального остовного дерева:")
    
    for ves, u, v in sortirovannye_rebra:
        idx_u = vershina_v_index[u]
        idx_v = vershina_v_index[v]
        
        if uf.obedinit(idx_u, idx_v):
            minimalnye_rebra.append((ves, u, v))
            obshiy_ves += ves
            print(f"  ✓ Добавлено ребро: {u} --({ves})-- {v}")
        else:
            print(f"  ✗ Пропущено (создает цикл): {u} --({ves})-- {v}")
    
    return minimalnye_rebra, obshiy_ves


# =============================================
# ДЕМОНСТРАЦИЯ РАБОТЫ
# =============================================

print("=" * 60)
print("ЛАБОРАТОРНАЯ РАБОТА №2")
print("Вариант 6")
print("Задание 4: Алгоритм Краскала")
print("=" * 60)

# Тест 1: Граф из 7 вершин
print("\n--- Тест 1: Граф с 7 вершинами ---")

vershiny_1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
rebra_1 = [
    (7, 'A', 'B'),
    (5, 'A', 'D'),
    (7, 'B', 'A'),
    (8, 'B', 'C'),
    (9, 'B', 'D'),
    (7, 'B', 'E'),
    (8, 'C', 'B'),
    (5, 'C', 'E'),
    (5, 'D', 'A'),
    (9, 'D', 'B'),
    (7, 'D', 'E'),
    (6, 'D', 'F'),
    (7, 'E', 'B'),
    (5, 'E', 'C'),
    (7, 'E', 'D'),
    (8, 'E', 'F'),
    (9, 'E', 'G'),
    (6, 'F', 'D'),
    (8, 'F', 'E'),
    (11, 'F', 'G'),
    (9, 'G', 'E'),
    (11, 'G', 'F')
]

# Удаляем дубликаты (неориентированный граф)
unikalnye_rebra = []
seen = set()
for ves, u, v in rebra_1:
    if (u, v) not in seen and (v, u) not in seen:
        seen.add((u, v))
        unikalnye_rebra.append((ves, u, v))

print(f"Вершины: {vershiny_1}")
print(f"Количество уникальных ребер: {len(unikalnye_rebra)}")

resultat_1, ves_1 = algoritm_kraskala(vershiny_1, unikalnye_rebra)

print(f"\n--- Результат ---")
print(f"Ребра минимального остовного дерева:")
for ves, u, v in resultat_1:
    print(f"  {u} --({ves})-- {v}")
print(f"Общий вес дерева: {ves_1}")

# Тест 2: Простой граф из 4 вершин
print("\n\n--- Тест 2: Простой граф с 4 вершинами ---")

vershiny_2 = ['X', 'Y', 'Z', 'W']
rebra_2 = [
    (1, 'X', 'Y'),
    (2, 'X', 'Z'),
    (3, 'Y', 'Z'),
    (4, 'Z', 'W'),
    (5, 'Y', 'W')
]

print(f"Вершины: {vershiny_2}")
print(f"Ребра: {rebra_2}")

resultat_2, ves_2 = algoritm_kraskala(vershiny_2, rebra_2)

print(f"\n--- Результат ---")
print(f"Ребра минимального остовного дерева:")
for ves, u, v in resultat_2:
    print(f"  {u} --({ves})-- {v}")
print(f"Общий вес дерева: {ves_2}")

print("\n" + "=" * 60)
print("Демонстрация завершена успешно!")
print("=" * 60)

input("\nНажмите Enter для выхода...")

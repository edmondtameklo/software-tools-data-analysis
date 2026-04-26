# -*- coding: utf-8 -*-
# Лабораторная работа №2
# Вариант 6
# Задание 1: Очередь с приоритетами на основе кучи
# Студент: Тамекло Коку Эдмон
# Группа: МИС-25-1

class PriorityQueue:
    """
    Очередь с приоритетами на основе минимальной кучи (min-heap).
    
    Куча хранится в виде списка, где для элемента с индексом i:
      - левый потомок: 2*i + 1
      - правый потомок: 2*i + 2
      - родитель: (i-1) // 2
    """
    
    def __init__(self):
        """Инициализация пустой очереди."""
        self.heap = []
    
    def is_empty(self):
        """Проверка на пустоту."""
        return len(self.heap) == 0
    
    def size(self):
        """Возвращает количество элементов."""
        return len(self.heap)
    
    def peek(self):
        """Возвращает элемент с наивысшим приоритетом (минимальный) без удаления."""
        if self.is_empty():
            return None
        return self.heap[0]
    
    def push(self, item):
        """
        Добавляет элемент в очередь.
        Временная сложность: O(log n)
        """
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)
    
    def pop(self):
        """
        Удаляет и возвращает элемент с наивысшим приоритетом (минимальный).
        Временная сложность: O(log n)
        """
        if self.is_empty():
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        
        return root
    
    def _sift_up(self, index):
        """Всплытие элемента вверх для восстановления свойства кучи."""
        parent = (index - 1) // 2
        
        while index > 0 and self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2
    
    def _sift_down(self, index):
        """Погружение элемента вниз для восстановления свойства кучи."""
        n = len(self.heap)
        
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2
            
            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right
            
            if smallest == index:
                break
            
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest
    
    def display(self):
        """Выводит содержимое кучи."""
        if self.is_empty():
            print("Очередь пуста.")
            return
        
        print(f"Куча (список): {self.heap}")
        print(f"Минимальный элемент (корень): {self.peek()}")
        print(f"Размер очереди: {self.size()}")


# =============================================
# ДЕМОНСТРАЦИЯ РАБОТЫ
# =============================================

print("=" * 60)
print("ЛАБОРАТОРНАЯ РАБОТА №2")
print("Вариант 6")
print("Задание 1: Очередь с приоритетами на основе кучи")
print("=" * 60)

pq = PriorityQueue()

print("\n--- 1. Добавление элементов ---")
elements = [5, 3, 8, 1, 9, 2, 7]
print(f"Добавляем элементы: {elements}")
for elem in elements:
    pq.push(elem)
    print(f"  Добавлен {elem}, куча: {pq.heap}")

pq.display()

print("\n--- 2. Просмотр минимального элемента (peek) ---")
print(f"Минимальный элемент: {pq.peek()}")

print("\n--- 3. Извлечение элементов по приоритету ---")
print("Извлекаем элементы (должны выходить в порядке возрастания):")
result = []
while not pq.is_empty():
    elem = pq.pop()
    result.append(elem)
    print(f"  Извлечен: {elem}, оставшаяся куча: {pq.heap}")

print(f"\nРезультат извлечения: {result}")
print(f"Отсортированы по возрастанию: {result == sorted(elements)}")

print("\n--- 4. Очередь с буквенными приоритетами ---")
pq_letters = PriorityQueue()
letters = ['привет', 'а', 'мир', 'я', 'здравствуй']
print(f"Добавляем слова: {letters}")
for word in letters:
    pq_letters.push(word)
    print(f"  Добавлено '{word}', куча: {pq_letters.heap}")

print("\nИзвлекаем слова в алфавитном порядке:")
while not pq_letters.is_empty():
    print(f"  Извлечено: '{pq_letters.pop()}'")

print("\n" + "=" * 60)
print("Демонстрация завершена успешно!")
print("=" * 60)

input("\nНажмите Enter для выхода...")

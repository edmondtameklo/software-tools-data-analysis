# -*- coding: utf-8 -*-
# Лабораторная работа №3
# Объектно-ориентированное программирование
# Вариант 6: Система управления авиакомпанией
# Студент: Тамекло Коку Эдмон
# Группа: МИС-25-1

import os
from abc import ABC, abstractmethod

# =============================================
# КОНСТАНТЫ (ИМЕНА ФАЙЛОВ)
# =============================================
FILE_AIRCRAFTS = "aircrafts.txt"
FILE_FLIGHTS = "flights.txt"
FILE_PILOTS = "pilots.txt"
FILE_CREW = "crew.txt"
FILE_PASSENGERS = "passengers.txt"

SEPARATOR = "|"

# =============================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ РАБОТЫ С ФАЙЛАМИ
# =============================================

def read_file(filename):
    """Читает строки из файла. Возвращает список строк."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Ошибка чтения файла {filename}: {e}")
        return []


def write_file(filename, lines):
    """Записывает список строк в файл."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + '\n')
    except Exception as e:
        print(f"Ошибка записи в файл {filename}: {e}")


def append_file(filename, line):
    """Добавляет одну строку в конец файла."""
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except Exception as e:
        print(f"Ошибка добавления в файл {filename}: {e}")


# =============================================
# КЛАСС 1: Aircraft (АБСТРАКТНЫЙ КЛАСС)
# =============================================

class Aircraft(ABC):
    """Абстрактный класс для самолетов."""
    
    def __init__(self, model, capacity, max_range, tail_number):
        self._model = model              # Модель самолета
        self._capacity = capacity        # Грузоподъемность или пассажировместимость
        self._max_range = max_range      # Максимальная дальность полета (км)
        self._tail_number = tail_number  # Бортовой номер (уникальный)
    
    @property
    def model(self):
        return self._model
    
    @property
    def capacity(self):
        return self._capacity
    
    @property
    def max_range(self):
        return self._max_range
    
    @property
    def tail_number(self):
        return self._tail_number
    
    @abstractmethod
    def get_type(self):
        """Возвращает тип самолета."""
        pass
    
    @abstractmethod
    def get_info(self):
        """Возвращает полную информацию о самолете."""
        pass
    
    def to_string(self):
        """Сериализация для сохранения в файл."""
        return SEPARATOR.join([
            self.get_type(),
            self._model,
            str(self._capacity),
            str(self._max_range),
            self._tail_number
        ])
    
    def __str__(self):
        return self.get_info()


# =============================================
# КЛАСС 2: PassengerPlane (НАСЛЕДУЕТСЯ ОТ Aircraft)
# =============================================

class PassengerPlane(Aircraft):
    """Пассажирский самолет."""
    
    def __init__(self, model, passenger_capacity, max_range, tail_number, seat_classes):
        super().__init__(model, passenger_capacity, max_range, tail_number)
        self._seat_classes = seat_classes  # Список классов мест (эконом, бизнес, первый)
    
    @property
    def seat_classes(self):
        return self._seat_classes
    
    def get_type(self):
        return "Пассажирский"
    
    def get_info(self):
        classes_str = ", ".join(self._seat_classes)
        return (f"Пассажирский самолет | Модель: {self._model} | "
                f"Борт: {self._tail_number} | "
                f"Пассажиров: {self._capacity} | "
                f"Дальность: {self._max_range} км | "
                f"Классы: {classes_str}")
    
    @classmethod
    def from_string(cls, line):
        """Создает объект из строки файла."""
        parts = line.split(SEPARATOR)
        if len(parts) >= 6:
            model = parts[1]
            capacity = int(parts[2])
            max_range = int(parts[3])
            tail_number = parts[4]
            seat_classes = parts[5].split(",")
            return cls(model, capacity, max_range, tail_number, seat_classes)
        return None


# =============================================
# КЛАСС 3: CargoPlane (НАСЛЕДУЕТСЯ ОТ Aircraft)
# =============================================

class CargoPlane(Aircraft):
    """Грузовой самолет."""
    
    def __init__(self, model, cargo_capacity_kg, max_range, tail_number, has_refrigeration):
        super().__init__(model, cargo_capacity_kg, max_range, tail_number)
        self._has_refrigeration = has_refrigeration  # Наличие холодильной установки
    
    @property
    def has_refrigeration(self):
        return self._has_refrigeration
    
    def get_type(self):
        return "Грузовой"
    
    def get_info(self):
        refr = "Да" if self._has_refrigeration else "Нет"
        return (f"Грузовой самолет | Модель: {self._model} | "
                f"Борт: {self._tail_number} | "
                f"Грузоподъемность: {self._capacity} кг | "
                f"Дальность: {self._max_range} км | "
                f"Холодильник: {refr}")
    
    @classmethod
    def from_string(cls, line):
        """Создает объект из строки файла."""
        parts = line.split(SEPARATOR)
        if len(parts) >= 6:
            model = parts[1]
            capacity = int(parts[2])
            max_range = int(parts[3])
            tail_number = parts[4]
            has_refrigeration = parts[5] == "True"
            return cls(model, capacity, max_range, tail_number, has_refrigeration)
        return None


# =============================================
# КЛАСС 4: Pilot
# =============================================

class Pilot:
    """Класс для пилотов."""
    
    def __init__(self, pilot_id, name, license_number, flight_hours, rank):
        self._pilot_id = pilot_id          # ID пилота
        self._name = name                  # Ф.И.О.
        self._license_number = license_number  # Номер лицензии
        self._flight_hours = flight_hours  # Налет часов
        self._rank = rank                  # Звание (командир, второй пилот)
    
    @property
    def pilot_id(self):
        return self._pilot_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def license_number(self):
        return self._license_number
    
    @property
    def flight_hours(self):
        return self._flight_hours
    
    @property
    def rank(self):
        return self._rank
    
    def add_flight_hours(self, hours):
        """Добавляет часы налета."""
        self._flight_hours += hours
    
    def get_info(self):
        return (f"Пилот | ID: {self._pilot_id} | "
                f"Ф.И.О.: {self._name} | "
                f"Лицензия: {self._license_number} | "
                f"Налет: {self._flight_hours} ч | "
                f"Звание: {self._rank}")
    
    def to_string(self):
        return SEPARATOR.join([
            self._pilot_id,
            self._name,
            self._license_number,
            str(self._flight_hours),
            self._rank
        ])
    
    @classmethod
    def from_string(cls, line):
        parts = line.split(SEPARATOR)
        if len(parts) >= 5:
            return cls(parts[0], parts[1], parts[2], int(parts[3]), parts[4])
        return None
    
    def __str__(self):
        return self.get_info()


# =============================================
# КЛАСС 5: CrewMember
# =============================================

class CrewMember:
    """Класс для членов экипажа (бортпроводники, инженеры и т.д.)."""
    
    def __init__(self, crew_id, name, position, experience_years, languages):
        self._crew_id = crew_id          # ID члена экипажа
        self._name = name                # Ф.И.О.
        self._position = position        # Должность (бортпроводник, инженер)
        self._experience_years = experience_years  # Стаж работы (лет)
        self._languages = languages      # Список языков, которыми владеет
    
    @property
    def crew_id(self):
        return self._crew_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def position(self):
        return self._position
    
    @property
    def experience_years(self):
        return self._experience_years
    
    @property
    def languages(self):
        return self._languages
    
    def get_info(self):
        langs = ", ".join(self._languages)
        return (f"Член экипажа | ID: {self._crew_id} | "
                f"Ф.И.О.: {self._name} | "
                f"Должность: {self._position} | "
                f"Стаж: {self._experience_years} лет | "
                f"Языки: {langs}")
    
    def to_string(self):
        return SEPARATOR.join([
            self._crew_id,
            self._name,
            self._position,
            str(self._experience_years),
            ",".join(self._languages)
        ])
    
    @classmethod
    def from_string(cls, line):
        parts = line.split(SEPARATOR)
        if len(parts) >= 5:
            languages = parts[4].split(",") if parts[4] else []
            return cls(parts[0], parts[1], parts[2], int(parts[3]), languages)
        return None
    
    def __str__(self):
        return self.get_info()


# =============================================
# КЛАСС 6: Passenger
# =============================================

class Passenger:
    """Класс для пассажиров."""
    
    def __init__(self, passenger_id, name, passport, ticket_number, seat, flight_number, meal_preference):
        self._passenger_id = passenger_id      # ID пассажира
        self._name = name                      # Ф.И.О.
        self._passport = passport              # Номер паспорта
        self._ticket_number = ticket_number    # Номер билета
        self._seat = seat                      # Место (например, 12A)
        self._flight_number = flight_number    # Номер рейса
        self._meal_preference = meal_preference  # Предпочтения по питанию
    
    @property
    def passenger_id(self):
        return self._passenger_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def passport(self):
        return self._passport
    
    @property
    def ticket_number(self):
        return self._ticket_number
    
    @property
    def seat(self):
        return self._seat
    
    @property
    def flight_number(self):
        return self._flight_number
    
    @property
    def meal_preference(self):
        return self._meal_preference
    
    def get_info(self):
        return (f"Пассажир | ID: {self._passenger_id} | "
                f"Ф.И.О.: {self._name} | "
                f"Паспорт: {self._passport} | "
                f"Билет: {self._ticket_number} | "
                f"Место: {self._seat} | "
                f"Рейс: {self._flight_number} | "
                f"Питание: {self._meal_preference}")
    
    def to_string(self):
        return SEPARATOR.join([
            self._passenger_id,
            self._name,
            self._passport,
            self._ticket_number,
            self._seat,
            self._flight_number,
            self._meal_preference
        ])
    
    @classmethod
    def from_string(cls, line):
        parts = line.split(SEPARATOR)
        if len(parts) >= 7:
            return cls(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6])
        return None
    
    def __str__(self):
        return self.get_info()


# =============================================
# КЛАСС 7: Flight
# =============================================

class Flight:
    """Класс для рейсов."""
    
    def __init__(self, flight_number, departure, destination, departure_time, 
                 arrival_time, aircraft_tail, pilot_ids, crew_ids):
        self._flight_number = flight_number      # Номер рейса
        self._departure = departure              # Аэропорт вылета
        self._destination = destination          # Аэропорт назначения
        self._departure_time = departure_time    # Время вылета
        self._arrival_time = arrival_time        # Время прибытия
        self._aircraft_tail = aircraft_tail      # Бортовой номер самолета
        self._pilot_ids = pilot_ids              # Список ID пилотов
        self._crew_ids = crew_ids                # Список ID членов экипажа
    
    @property
    def flight_number(self):
        return self._flight_number
    
    @property
    def departure(self):
        return self._departure
    
    @property
    def destination(self):
        return self._destination
    
    @property
    def departure_time(self):
        return self._departure_time
    
    @property
    def arrival_time(self):
        return self._arrival_time
    
    @property
    def aircraft_tail(self):
        return self._aircraft_tail
    
    @property
    def pilot_ids(self):
        return self._pilot_ids
    
    @property
    def crew_ids(self):
        return self._crew_ids
    
    def assign_pilot(self, pilot_id):
        """Назначает пилота на рейс."""
        if pilot_id not in self._pilot_ids:
            self._pilot_ids.append(pilot_id)
    
    def assign_crew(self, crew_id):
        """Назначает члена экипажа на рейс."""
        if crew_id not in self._crew_ids:
            self._crew_ids.append(crew_id)
    
    def get_info(self):
        return (f"Рейс {self._flight_number} | "
                f"{self._departure} → {self._destination} | "
                f"Вылет: {self._departure_time} | "
                f"Прибытие: {self._arrival_time} | "
                f"Борт: {self._aircraft_tail} | "
                f"Пилоты: {len(self._pilot_ids)} | "
                f"Экипаж: {len(self._crew_ids)}")
    
    def to_string(self):
        return SEPARATOR.join([
            self._flight_number,
            self._departure,
            self._destination,
            self._departure_time,
            self._arrival_time,
            self._aircraft_tail,
            ",".join(self._pilot_ids),
            ",".join(self._crew_ids)
        ])
    
    @classmethod
    def from_string(cls, line):
        parts = line.split(SEPARATOR)
        if len(parts) >= 8:
            pilot_ids = parts[6].split(",") if parts[6] else []
            crew_ids = parts[7].split(",") if parts[7] else []
            return cls(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], pilot_ids, crew_ids)
        return None
    
    def __str__(self):
        return self.get_info()


# =============================================
# ГЛАВНЫЙ КЛАСС: AirlineManager
# =============================================

class AirlineManager:
    """Главный класс управления авиакомпанией."""
    
    def __init__(self):
        self.aircrafts = []     # Список самолетов
        self.flights = []       # Список рейсов
        self.pilots = []        # Список пилотов
        self.crew_members = []  # Список членов экипажа
        self.passengers = []    # Список пассажиров
        self._load_all_data()
    
    # ==========================================
    # ЗАГРУЗКА ДАННЫХ ИЗ ФАЙЛОВ
    # ==========================================
    
    def _load_all_data(self):
        """Загружает все данные из файлов."""
        self._load_aircrafts()
        self._load_flights()
        self._load_pilots()
        self._load_crew()
        self._load_passengers()
    
    def _load_aircrafts(self):
        """Загружает самолеты из файла."""
        lines = read_file(FILE_AIRCRAFTS)
        self.aircrafts = []
        for line in lines:
            if line.startswith("Пассажирский"):
                aircraft = PassengerPlane.from_string(line)
            elif line.startswith("Грузовой"):
                aircraft = CargoPlane.from_string(line)
            else:
                continue
            if aircraft:
                self.aircrafts.append(aircraft)
    
    def _load_flights(self):
        """Загружает рейсы из файла."""
        lines = read_file(FILE_FLIGHTS)
        self.flights = []
        for line in lines:
            flight = Flight.from_string(line)
            if flight:
                self.flights.append(flight)
    
    def _load_pilots(self):
        """Загружает пилотов из файла."""
        lines = read_file(FILE_PILOTS)
        self.pilots = []
        for line in lines:
            pilot = Pilot.from_string(line)
            if pilot:
                self.pilots.append(pilot)
    
    def _load_crew(self):
        """Загружает экипаж из файла."""
        lines = read_file(FILE_CREW)
        self.crew_members = []
        for line in lines:
            crew = CrewMember.from_string(line)
            if crew:
                self.crew_members.append(crew)
    
    def _load_passengers(self):
        """Загружает пассажиров из файла."""
        lines = read_file(FILE_PASSENGERS)
        self.passengers = []
        for line in lines:
            passenger = Passenger.from_string(line)
            if passenger:
                self.passengers.append(passenger)
    
    # ==========================================
    # СОХРАНЕНИЕ ДАННЫХ В ФАЙЛЫ
    # ==========================================
    
    def _save_aircrafts(self):
        """Сохраняет самолеты в файл."""
        lines = [aircraft.to_string() for aircraft in self.aircrafts]
        write_file(FILE_AIRCRAFTS, lines)
    
    def _save_flights(self):
        """Сохраняет рейсы в файл."""
        lines = [flight.to_string() for flight in self.flights]
        write_file(FILE_FLIGHTS, lines)
    
    def _save_pilots(self):
        """Сохраняет пилотов в файл."""
        lines = [pilot.to_string() for pilot in self.pilots]
        write_file(FILE_PILOTS, lines)
    
    def _save_crew(self):
        """Сохраняет экипаж в файл."""
        lines = [crew.to_string() for crew in self.crew_members]
        write_file(FILE_CREW, lines)
    
    def _save_passengers(self):
        """Сохраняет пассажиров в файл."""
        lines = [passenger.to_string() for passenger in self.passengers]
        write_file(FILE_PASSENGERS, lines)
    
    def _save_all(self):
        """Сохраняет все данные."""
        self._save_aircrafts()
        self._save_flights()
        self._save_pilots()
        self._save_crew()
        self._save_passengers()
    
    # ==========================================
    # ПОИСК ОБЪЕКТОВ
    # ==========================================
    
    def _find_aircraft(self, tail_number):
        """Находит самолет по бортовому номеру."""
        for a in self.aircrafts:
            if a.tail_number == tail_number:
                return a
        return None
    
    def _find_flight(self, flight_number):
        """Находит рейс по номеру."""
        for f in self.flights:
            if f.flight_number == flight_number:
                return f
        return None
    
    def _find_pilot(self, pilot_id):
        """Находит пилота по ID."""
        for p in self.pilots:
            if p.pilot_id == pilot_id:
                return p
        return None
    
    def _find_crew_member(self, crew_id):
        """Находит члена экипажа по ID."""
        for c in self.crew_members:
            if c.crew_id == crew_id:
                return c
        return None
    
    # ==========================================
    # ОПЕРАЦИИ С САМОЛЕТАМИ
    # ==========================================
    
    def add_aircraft(self):
        """Добавляет новый самолет."""
        print("\n" + "=" * 50)
        print("ДОБАВЛЕНИЕ НОВОГО САМОЛЕТА")
        print("=" * 50)
        
        print("Тип самолета:")
        print("1 - Пассажирский")
        print("2 - Грузовой")
        
        try:
            tip = input("Выберите тип (1-2): ")
            
            if tip not in ('1', '2'):
                print("Ошибка: неверный тип самолета!")
                return
            
            model = input("Введите модель самолета: ")
            if not model:
                print("Ошибка: модель не может быть пустой!")
                return
            
            capacity = int(input("Введите вместимость (пассажиров или кг): "))
            if capacity <= 0:
                print("Ошибка: вместимость должна быть положительным числом!")
                return
            
            max_range = int(input("Введите максимальную дальность (км): "))
            if max_range <= 0:
                print("Ошибка: дальность должна быть положительным числом!")
                return
            
            tail_number = input("Введите бортовой номер: ")
            if not tail_number:
                print("Ошибка: бортовой номер не может быть пустым!")
                return
            
            if self._find_aircraft(tail_number):
                print(f"Ошибка: самолет с бортовым номером {tail_number} уже существует!")
                return
            
            if tip == '1':
                classes_input = input("Введите классы мест через запятую (эконом,бизнес,первый): ")
                seat_classes = [c.strip() for c in classes_input.split(",") if c.strip()]
                if not seat_classes:
                    seat_classes = ["эконом"]
                aircraft = PassengerPlane(model, capacity, max_range, tail_number, seat_classes)
            else:
                refr_input = input("Наличие холодильной установки (да/нет): ").lower()
                has_refrigeration = refr_input in ('да', 'yes', '1', 'y')
                aircraft = CargoPlane(model, capacity, max_range, tail_number, has_refrigeration)
            
            self.aircrafts.append(aircraft)
            self._save_aircrafts()
            print(f"\n✓ Самолет успешно добавлен!")
            print(f"  {aircraft.get_info()}")
        
        except ValueError:
            print("Ошибка: введите корректные числовые значения!")
    
    def show_aircrafts(self):
        """Показывает все самолеты."""
        print("\n" + "=" * 70)
        print("СПИСОК САМОЛЕТОВ АВИАКОМПАНИИ")
        print("=" * 70)
        
        if not self.aircrafts:
            print("Список самолетов пуст.")
            return
        
        for i, aircraft in enumerate(self.aircrafts, 1):
            print(f"{i}. {aircraft.get_info()}")
        
        print("=" * 70)
        print(f"Всего самолетов: {len(self.aircrafts)}")
    
    # ==========================================
    # ОПЕРАЦИИ С ПИЛОТАМИ
    # ==========================================
    
    def add_pilot(self):
        """Добавляет нового пилота."""
        print("\n" + "=" * 50)
        print("ДОБАВЛЕНИЕ НОВОГО ПИЛОТА")
        print("=" * 50)
        
        try:
            pilot_id = input("Введите ID пилота: ")
            if not pilot_id:
                print("Ошибка: ID не может быть пустым!")
                return
            
            if self._find_pilot(pilot_id):
                print(f"Ошибка: пилот с ID {pilot_id} уже существует!")
                return
            
            name = input("Введите Ф.И.О. пилота: ")
            if not name:
                print("Ошибка: имя не может быть пустым!")
                return
            
            license_number = input("Введите номер лицензии: ")
            flight_hours = int(input("Введите налет часов: "))
            if flight_hours < 0:
                print("Ошибка: налет часов не может быть отрицательным!")
                return
            
            print("Звание:")
            print("1 - Командир воздушного судна")
            print("2 - Второй пилот")
            rank_choice = input("Выберите звание (1-2): ")
            
            if rank_choice == '1':
                rank = "Командир ВС"
            elif rank_choice == '2':
                rank = "Второй пилот"
            else:
                print("Ошибка: неверный выбор звания!")
                return
            
            pilot = Pilot(pilot_id, name, license_number, flight_hours, rank)
            self.pilots.append(pilot)
            self._save_pilots()
            print(f"\n✓ Пилот успешно добавлен!")
            print(f"  {pilot.get_info()}")
        
        except ValueError:
            print("Ошибка: введите корректные числовые значения!")
    
    def show_pilots(self):
        """Показывает всех пилотов."""
        print("\n" + "=" * 70)
        print("СПИСОК ПИЛОТОВ")
        print("=" * 70)
        
        if not self.pilots:
            print("Список пилотов пуст.")
            return
        
        for i, pilot in enumerate(self.pilots, 1):
            print(f"{i}. {pilot.get_info()}")
        
        print("=" * 70)
        print(f"Всего пилотов: {len(self.pilots)}")
    
    # ==========================================
    # ОПЕРАЦИИ С ЧЛЕНАМИ ЭКИПАЖА
    # ==========================================
    
    def add_crew_member(self):
        """Добавляет нового члена экипажа."""
        print("\n" + "=" * 50)
        print("ДОБАВЛЕНИЕ ЧЛЕНА ЭКИПАЖА")
        print("=" * 50)
        
        try:
            crew_id = input("Введите ID члена экипажа: ")
            if not crew_id:
                print("Ошибка: ID не может быть пустым!")
                return
            
            if self._find_crew_member(crew_id):
                print(f"Ошибка: член экипажа с ID {crew_id} уже существует!")
                return
            
            name = input("Введите Ф.И.О.: ")
            if not name:
                print("Ошибка: имя не может быть пустым!")
                return
            
            position = input("Введите должность (бортпроводник, инженер, старший бортпроводник): ")
            if not position:
                print("Ошибка: должность не может быть пустой!")
                return
            
            experience = int(input("Введите стаж работы (лет): "))
            if experience < 0:
                print("Ошибка: стаж не может быть отрицательным!")
                return
            
            langs_input = input("Введите языки через запятую (русский,английский): ")
            languages = [l.strip() for l in langs_input.split(",") if l.strip()]
            if not languages:
                languages = ["русский"]
            
            crew = CrewMember(crew_id, name, position, experience, languages)
            self.crew_members.append(crew)
            self._save_crew()
            print(f"\n✓ Член экипажа успешно добавлен!")
            print(f"  {crew.get_info()}")
        
        except ValueError:
            print("Ошибка: введите корректные числовые значения!")
    
    def show_crew(self):
        """Показывает всех членов экипажа."""
        print("\n" + "=" * 70)
        print("СПИСОК ЧЛЕНОВ ЭКИПАЖА")
        print("=" * 70)
        
        if not self.crew_members:
            print("Список экипажа пуст.")
            return
        
        for i, crew in enumerate(self.crew_members, 1):
            print(f"{i}. {crew.get_info()}")
        
        print("=" * 70)
        print(f"Всего членов экипажа: {len(self.crew_members)}")
    
    # ==========================================
    # ОПЕРАЦИИ С РЕЙСАМИ
    # ==========================================
    
    def add_flight(self):
        """Добавляет новый рейс."""
        print("\n" + "=" * 50)
        print("ДОБАВЛЕНИЕ НОВОГО РЕЙСА")
        print("=" * 50)
        
        flight_number = input("Введите номер рейса: ")
        if not flight_number:
            print("Ошибка: номер рейса не может быть пустым!")
            return
        
        if self._find_flight(flight_number):
            print(f"Ошибка: рейс {flight_number} уже существует!")
            return
        
        departure = input("Введите аэропорт вылета: ")
        destination = input("Введите аэропорт назначения: ")
        departure_time = input("Введите время вылета (ГГГГ-ММ-ДД ЧЧ:ММ): ")
        arrival_time = input("Введите время прибытия (ГГГГ-ММ-ДД ЧЧ:ММ): ")
        aircraft_tail = input("Введите бортовой номер самолета: ")
        
        if not self._find_aircraft(aircraft_tail):
            print(f"Ошибка: самолет с бортовым номером {aircraft_tail} не найден!")
            return
        
        flight = Flight(flight_number, departure, destination, departure_time, 
                       arrival_time, aircraft_tail, [], [])
        self.flights.append(flight)
        self._save_flights()
        print(f"\n✓ Рейс успешно добавлен!")
        print(f"  {flight.get_info()}")
    
    def show_flights(self):
        """Показывает все рейсы."""
        print("\n" + "=" * 70)
        print("РАСПИСАНИЕ РЕЙСОВ")
        print("=" * 70)
        
        if not self.flights:
            print("Список рейсов пуст.")
            return
        
        for i, flight in enumerate(self.flights, 1):
            print(f"{i}. {flight.get_info()}")
        
        print("=" * 70)
        print(f"Всего рейсов: {len(self.flights)}")
    
    # ==========================================
    # НАЗНАЧЕНИЕ ЭКИПАЖА НА РЕЙС
    # ==========================================
    
    def assign_crew_to_flight(self):
        """Назначает экипаж и пилотов на рейс."""
        print("\n" + "=" * 50)
        print("НАЗНАЧЕНИЕ ЭКИПАЖА НА РЕЙС")
        print("=" * 50)
        
        flight_number = input("Введите номер рейса: ")
        flight = self._find_flight(flight_number)
        
        if not flight:
            print(f"Ошибка: рейс {flight_number} не найден!")
            return
        
        print(f"\nТекущий рейс: {flight.get_info()}")
        
        # Назначение пилотов
        print("\n--- Назначение пилотов ---")
        self.show_pilots()
        pilot_ids_input = input("Введите ID пилотов через запятую: ")
        pilot_ids = [pid.strip() for pid in pilot_ids_input.split(",") if pid.strip()]
        
        valid_pilots = []
        for pid in pilot_ids:
            pilot = self._find_pilot(pid)
            if pilot:
                valid_pilots.append(pid)
            else:
                print(f"  Предупреждение: пилот с ID {pid} не найден, пропущен.")
        
        flight._pilot_ids = valid_pilots
        
        # Назначение экипажа
        print("\n--- Назначение членов экипажа ---")
        self.show_crew()
        crew_ids_input = input("Введите ID членов экипажа через запятую: ")
        crew_ids = [cid.strip() for cid in crew_ids_input.split(",") if cid.strip()]
        
        valid_crew = []
        for cid in crew_ids:
            crew = self._find_crew_member(cid)
            if crew:
                valid_crew.append(cid)
            else:
                print(f"  Предупреждение: член экипажа с ID {cid} не найден, пропущен.")
        
        flight._crew_ids = valid_crew
        self._save_flights()
        
        print(f"\n✓ Экипаж назначен на рейс {flight_number}!")
        print(f"  Пилоты: {len(valid_pilots)}")
        print(f"  Члены экипажа: {len(valid_crew)}")
    
    # ==========================================
    # БРОНИРОВАНИЕ БИЛЕТОВ
    # ==========================================
    
    def book_ticket(self):
        """Бронирует билет для пассажира."""
        print("\n" + "=" * 50)
        print("БРОНИРОВАНИЕ БИЛЕТА")
        print("=" * 50)
        
        # Показываем доступные рейсы
        self.show_flights()
        
        if not self.flights:
            return
        
        try:
            passenger_id = input("Введите ID пассажира: ")
            if not passenger_id:
                print("Ошибка: ID не может быть пустым!")
                return
            
            name = input("Введите Ф.И.О. пассажира: ")
            if not name:
                print("Ошибка: имя не может быть пустым!")
                return
            
            passport = input("Введите номер паспорта: ")
            flight_number = input("Введите номер рейса: ")
            
            flight = self._find_flight(flight_number)
            if not flight:
                print(f"Ошибка: рейс {flight_number} не найден!")
                return
            
            seat = input("Введите место (например, 12A): ")
            ticket_number = f"TKT-{flight_number}-{passenger_id}"
            
            print("\nПредпочтения по питанию:")
            print("1 - Стандартное")
            print("2 - Вегетарианское")
            print("3 - Безглютеновое")
            meal_choice = input("Выберите (1-3): ")
            
            meal_map = {'1': 'Стандартное', '2': 'Вегетарианское', '3': 'Безглютеновое'}
            meal_preference = meal_map.get(meal_choice, 'Стандартное')
            
            passenger = Passenger(passenger_id, name, passport, ticket_number, 
                                 seat, flight_number, meal_preference)
            self.passengers.append(passenger)
            self._save_passengers()
            
            print(f"\n✓ Билет успешно забронирован!")
            print(f"  Пассажир: {name}")
            print(f"  Номер билета: {ticket_number}")
            print(f"  Рейс: {flight_number}")
            print(f"  Маршрут: {flight.departure} → {flight.destination}")
            print(f"  Место: {seat}")
            print(f"  Питание: {meal_preference}")
        
        except Exception as e:
            print(f"Ошибка при бронировании: {e}")
    
    def show_passengers(self):
        """Показывает всех пассажиров."""
        print("\n" + "=" * 70)
        print("СПИСОК ПАССАЖИРОВ")
        print("=" * 70)
        
        if not self.passengers:
            print("Список пассажиров пуст.")
            return
        
        for i, p in enumerate(self.passengers, 1):
            print(f"{i}. {p.get_info()}")
        
        print("=" * 70)
        print(f"Всего пассажиров: {len(self.passengers)}")
    
    # ==========================================
    # ДЕМОНСТРАЦИОННЫЕ ДАННЫЕ
    # ==========================================
    
    def _init_demo_data(self):
        """Загружает демо-данные при первом запуске."""
        if not os.path.exists(FILE_AIRCRAFTS):
            print("\nПервый запуск! Добавляю демонстрационные данные...\n")
            
            # Самолеты
            demo_aircrafts = [
                PassengerPlane("Boeing 737-800", 189, 5765, "RA-73123", 
                              ["эконом", "бизнес"]),
                PassengerPlane("Airbus A320", 180, 6150, "RA-73245", 
                              ["эконом", "бизнес"]),
                CargoPlane("Boeing 747-400F", 124000, 8230, "RA-76321", True),
            ]
            self.aircrafts = demo_aircrafts
            self._save_aircrafts()
            
            # Пилоты
            demo_pilots = [
                Pilot("P001", "Иванов Сергей Петрович", "LIC-12345", 8500, "Командир ВС"),
                Pilot("P002", "Смирнова Елена Алексеевна", "LIC-23456", 6200, "Второй пилот"),
                Pilot("P003", "Козлов Дмитрий Иванович", "LIC-34567", 9100, "Командир ВС"),
            ]
            self.pilots = demo_pilots
            self._save_pilots()
            
            # Члены экипажа
            demo_crew = [
                CrewMember("C001", "Петрова Анна Викторовна", "Старший бортпроводник", 8, 
                          ["русский", "английский"]),
                CrewMember("C002", "Соколов Алексей Игоревич", "Бортпроводник", 3, 
                          ["русский"]),
                CrewMember("C003", "Михайлова Татьяна Сергеевна", "Бортпроводник", 5, 
                          ["русский", "английский", "французский"]),
                CrewMember("C004", "Новиков Павел Андреевич", "Бортинженер", 12, 
                          ["русский", "английский"]),
            ]
            self.crew_members = demo_crew
            self._save_crew()
            
            # Рейсы
            demo_flights = [
                Flight("SU-1234", "Москва (SVO)", "Санкт-Петербург (LED)", 
                      "2024-12-01 08:00", "2024-12-01 09:30", "RA-73123", 
                      ["P001", "P002"], ["C001", "C002"]),
                Flight("SU-5678", "Москва (SVO)", "Сочи (AER)", 
                      "2024-12-01 10:00", "2024-12-01 13:00", "RA-73245", 
                      ["P003"], ["C003"]),
            ]
            self.flights = demo_flights
            self._save_flights()
            
            # Пассажиры
            demo_passengers = [
                Passenger("PAX001", "Иванов Иван Иванович", "4512-123456", 
                         "TKT-SU-1234-PAX001", "12A", "SU-1234", "Стандартное"),
                Passenger("PAX002", "Петрова Анна Сергеевна", "4512-654321", 
                         "TKT-SU-1234-PAX002", "12B", "SU-1234", "Вегетарианское"),
            ]
            self.passengers = demo_passengers
            self._save_passengers()
            
            print("✓ Загружено демо-данных:")
            print(f"  Самолетов: {len(self.aircrafts)}")
            print(f"  Пилоты: {len(self.pilots)}")
            print(f"  Членов экипажа: {len(self.crew_members)}")
            print(f"  Рейсов: {len(self.flights)}")
            print(f"  Пассажиров: {len(self.passengers)}")


# =============================================
# ГЛАВНОЕ МЕНЮ
# =============================================

def main_menu():
    """Отображает главное меню программы."""
    manager = AirlineManager()
    manager._init_demo_data()
    
    while True:
        print("\n" + "=" * 55)
        print("=== СИСТЕМА УПРАВЛЕНИЯ АВИАКОМПАНИЕЙ ===")
        print("Вариант 6")
        print("=" * 55)
        print(" 1. Показать все самолеты")
        print(" 2. Добавить самолет")
        print(" 3. Показать всех пилотов")
        print(" 4. Добавить пилота")
        print(" 5. Показать членов экипажа")
        print(" 6. Добавить члена экипажа")
        print(" 7. Показать расписание рейсов")
        print(" 8. Добавить рейс")
        print(" 9. Назначить экипаж на рейс")
        print("10. Забронировать билет")
        print("11. Показать пассажиров")
        print("12. Выход")
        print("-" * 55)
        
        choice = input("Выберите действие (1-12): ")
        
        if choice == '1':
            manager.show_aircrafts()
        elif choice == '2':
            manager.add_aircraft()
        elif choice == '3':
            manager.show_pilots()
        elif choice == '4':
            manager.add_pilot()
        elif choice == '5':
            manager.show_crew()
        elif choice == '6':
            manager.add_crew_member()
        elif choice == '7':
            manager.show_flights()
        elif choice == '8':
            manager.add_flight()
        elif choice == '9':
            manager.assign_crew_to_flight()
        elif choice == '10':
            manager.book_ticket()
        elif choice == '11':
            manager.show_passengers()
        elif choice == '12':
            print("\nПрограмма завершена. До свидания!")
            break
        else:
            print("\nОшибка: выберите число от 1 до 12!")


# =============================================
# ЗАПУСК ПРОГРАММЫ
# =============================================

if __name__ == "__main__":
    print("=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА №3")
    print("Объектно-ориентированное программирование")
    print("Вариант 6: Система управления авиакомпанией")
    print("=" * 60)
    main_menu()

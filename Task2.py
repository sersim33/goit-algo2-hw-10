class Teacher:
    def __init__(self, first_name, last_name, age, email, can_teach_subjects):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.can_teach_subjects = set(can_teach_subjects)

    def __repr__(self):
        # Додамо repr для зручного відображення об'єктів викладачів
        return f"Teacher({self.first_name} {self.last_name}, Age: {self.age})"


def create_schedule(subjects, teachers):
    """
    Призначає викладачів на предмети за допомогою модифікованого жадібного алгоритму.

    Args:
        subjects (list): Список предметів для призначення.
        teachers (list): Список об'єктів класу Teacher.

    Returns:
        dict: Словник, де ключ - об'єкт викладача, значення - список призначених предметів.
    """
    schedule = {teacher: [] for teacher in teachers}
    unassigned_subjects = set(subjects)

    # Поки є непризначені предмети
    while unassigned_subjects:
        best_teacher = None
        max_uncovered_subjects = -1
        youngest_age = float('inf') # Нескінченність для пошуку наймолодшого

        # Знаходимо найкращого викладача для поточного етапу
        for teacher in teachers:
            # Кількість предметів, які може викладати викладач і які ще не призначені
            can_teach_uncovered = teacher.can_teach_subjects.intersection(unassigned_subjects)
            num_uncovered_subjects = len(can_teach_uncovered)

            # Критерій вибору:
            # 1. Більше непризначених предметів, які може викладати
            # 2. Молодший вік при однаковій кількості непризначених предметів
            if num_uncovered_subjects > max_uncovered_subjects:
                max_uncovered_subjects = num_uncovered_subjects
                best_teacher = teacher
                youngest_age = teacher.age
            elif num_uncovered_subjects == max_uncovered_subjects and teacher.age < youngest_age:
                 best_teacher = teacher
                 youngest_age = teacher.age

        # Якщо не знайдено жодного викладача, який може викладати будь-який з непризначених предметів
        if best_teacher is None:
            print("Помилка: Неможливо призначити всі предмети.")
            return schedule # Повертаємо поточний частковий розклад

        # Призначаємо найкращому викладачеві всі непризначені предмети, які він може викладати
        assigned_to_best_teacher = best_teacher.can_teach_subjects.intersection(unassigned_subjects)
        schedule[best_teacher].extend(list(assigned_to_best_teacher))
        unassigned_subjects -= assigned_to_best_teacher # Видаляємо призначені предмети зі списку непризначених

    return schedule


# Основна частина
if __name__ == "__main__":

    # Множина предметів
    subjects = {"Математика", "Фізика", "Хімія", "Інформатика", "Біологія"}

    ## Створення списку викладачів
    teachers = [
        Teacher(
            "Олександр",
            "Іваненко",
            45,
            "o.ivanenko@example.com",
            {"Математика", "Фізика"},
        ),
        Teacher("Марія", "Петренко", 38, "m.petrenko@example.com", {"Хімія"}),
        Teacher(
            "Сергій",
            "Коваленко",
            50,
            "s.kovalenko@example.com",
            {"Інформатика", "Математика"},
        ),
        Teacher(
            "Наталія", "Шевченко", 29, "n.shevchenko@example.com", {"Біологія", "Хімія"}
        ),
        Teacher(
            "Дмитро",
            "Бондаренко",
            35,
            "d.bondarenko@example.com",
            {"Фізика", "Інформатика"},
        ),
        Teacher("Олена", "Гриценко", 42, "o.grytsenko@example.com", {"Біологія"}),
    ]

    # Виклик функції створення розкладу
    schedule = create_schedule(subjects, teachers)

# Виведення результату
if schedule:
    print("Розклад занять:")
    for teacher in schedule:
        # Check if the teacher has any assigned subjects
        if schedule[teacher]:
            print(
                f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}"
            )
            print(
                f"   Викладає предмети: {', '.join(sorted(schedule[teacher]))}\n"
            )
else:
    print("Неможливо покрити всі предмети наявними викладачами.")

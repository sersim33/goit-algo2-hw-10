import random
import time
import statistics
import matplotlib.pyplot as plt  

# Функція для генерації масиву випадкових цілих чисел 
def generate_random_array(size):
  """
  Генерує масив заданого розміру, заповнений випадковими цілими числами.
  """
  return [random.randint(0, size) for _ in range(size)]

# Створення тестових масивів різного розміру 
array_sizes = [10000, 50000, 100000, 500000]
test_arrays = {}

for size in array_sizes:
    test_arrays[size] = generate_random_array(size)

# Функція рандомізованого швидкого сортування з вимірюванням часу
def randomized_quick_sort_with_time(arr):
    start_time = time.time()
    arr_copy = arr[:]

    def quicksort_recursive(data):
        if len(data) < 2:
            return data
        pivot_index = random.randint(0, len(data) - 1)
        pivot = data[pivot_index]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return quicksort_recursive(left) + middle + quicksort_recursive(right)

    sorted_arr = quicksort_recursive(arr_copy)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return sorted_arr, elapsed_time

# Функція для детермінованого швидкого сортування з вимірюванням часу
def deterministic_quick_sort_with_time(arr, pivot_choice="middle"):
    """
    Виконує детерміноване швидке сортування з фіксованим вибором опорного елемента
    (перший, останній або середній) і вимірює час виконання.
    Повертає відсортований масив і час виконання у секундах.
    """
    start_time = time.time()
    arr_copy = arr[:] # Створюємо копію масиву

    def quicksort_recursive(data):
        if len(data) < 2:
            return data

        # Вибір опорного елемента за фіксованим правилом
        if pivot_choice == "first":
            pivot = data[0]
        elif pivot_choice == "last":
            pivot = data[-1]
        elif pivot_choice == "middle":
            pivot = data[len(data) // 2]
        else:
            raise ValueError("Невірний вибір опорного елемента. Дозволені: 'first', 'last', 'middle'.")

        left = []
        right = []
        middle = []

        for x in data:
            if x < pivot:
                left.append(x)
            elif x == pivot:
                middle.append(x)
            else:
                right.append(x)

        return quicksort_recursive(left) + middle + quicksort_recursive(right)

    sorted_arr = quicksort_recursive(arr_copy)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return sorted_arr, elapsed_time

# Вимірювання часу виконання для обох алгоритмів на кожному масиві
num_runs = 5
results = {}

for size, arr in test_arrays.items():
    print(f"\nТестування масиву розміром {size}:")
    randomized_times = []
    deterministic_middle_times = []
    deterministic_first_times = []
    deterministic_last_times = []

    for _ in range(num_runs):
        # Randomized Quick Sort
        _, time_rand = randomized_quick_sort_with_time(arr)
        randomized_times.append(time_rand)

        # Deterministic Quick Sort (middle pivot)
        _, time_det_middle = deterministic_quick_sort_with_time(arr, pivot_choice="middle")
        deterministic_middle_times.append(time_det_middle)

        # Deterministic Quick Sort (first pivot)
        _, time_det_first = deterministic_quick_sort_with_time(arr, pivot_choice="first")
        deterministic_first_times.append(time_det_first)

        # Deterministic Quick Sort (last pivot)
        _, time_det_last = deterministic_quick_sort_with_time(arr, pivot_choice="last")
        deterministic_last_times.append(time_det_last)


    # Обчислення середнього часу
    avg_randomized_time = statistics.mean(randomized_times)
    avg_deterministic_middle_time = statistics.mean(deterministic_middle_times)
    avg_deterministic_first_time = statistics.mean(deterministic_first_times)
    avg_deterministic_last_time = statistics.mean(deterministic_last_times)


    results[size] = {
        "randomized": avg_randomized_time,
        "deterministic_middle": avg_deterministic_middle_time,
        "deterministic_first": avg_deterministic_first_time,
        "deterministic_last": avg_deterministic_last_time,
    }

    print(f"  Середній час randomized_quick_sort: {avg_randomized_time:.6f} секунд")
    print(f"  Середній час deterministic_quick_sort (середній опорний): {avg_deterministic_middle_time:.6f} секунд")
    print(f"  Середній час deterministic_quick_sort (перший опорний): {avg_deterministic_first_time:.6f} секунд")
    print(f"  Середній час deterministic_quick_sort (останній опорний): {avg_deterministic_last_time:.6f} секунд")


# Виведення зведених результатів
print("\nЗведені результати середнього часу сортування:")
for size, times in results.items():
    print(f"Розмір {size}:")
    print(f"  Randomized: {times['randomized']:.6f} секунд")
    print(f"  Deterministic (середній): {times['deterministic_middle']:.6f} секунд")
    print(f"  Deterministic (перший): {times['deterministic_first']:.6f} секунд")
    print(f"  Deterministic (останній): {times['deterministic_last']:.6f} секунд")

# Побудова графіків
plt.figure(figsize=(10, 6))

# Отримуємо розміри масивів для осі X
sizes = sorted(results.keys())

# Отримуємо часи сортування для кожного алгоритму
randomized_times = [results[size]["randomized"] for size in sizes]
deterministic_middle_times = [results[size]["deterministic_middle"] for size in sizes]
deterministic_first_times = [results[size]["deterministic_first"] for size in sizes]
deterministic_last_times = [results[size]["deterministic_last"] for size in sizes]


# Побудова ліній для кожного алгоритму
plt.plot(sizes, randomized_times, marker='o', label='Randomized Quick Sort')
plt.plot(sizes, deterministic_middle_times, marker='o', label='Deterministic Quick Sort (Середній опорний)')
plt.plot(sizes, deterministic_first_times, marker='o', label='Deterministic Quick Sort (Перший опорний)')
plt.plot(sizes, deterministic_last_times, marker='o', label='Deterministic Quick Sort (Останній опорний)')


# Додавання підписів до осей та заголовка
plt.xlabel("Розмір масиву")
plt.ylabel("Середній час виконання (секунди)")
plt.title("Порівняння часу виконання швидкого сортування")

# Додавання легенди
plt.legend()

# Додавання сітки для кращої читабельності
plt.grid(True)

# Відображення графіку
plt.show()

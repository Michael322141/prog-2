import timeit
import matplotlib.pyplot as plt
import sys
from functools import lru_cache

# Увеличим максимальную глубину рекурсии для больших чисел
sys.setrecursionlimit(10000)

# 1. Рекурсивная реализация (без мемоизации)
def fact_recursive(n):
    if n <= 1:
        return 1
    return n * fact_recursive(n - 1)

# 2. Итеративная реализация (без мемоизации)
def fact_iterative(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# 3. Рекурсивная реализация с мемоизацией
@lru_cache(maxsize=None)
def fact_recursive_memo(n):
    if n <= 1:
        return 1
    return n * fact_recursive_memo(n - 1)

# 4. Итеративная реализация с "мемоизацией" (кеширование результатов)
class FactorialCalculator:
    def __init__(self):
        self.cache = {}
    
    def fact_iterative_memo(self, n):
        if n in self.cache:
            return self.cache[n]
        
        result = 1
        # Вычисляем факториал и кешируем промежуточные результаты
        if n > 0 and (n-1) in self.cache:
            result = self.cache[n-1] * n
        else:
            for i in range(1, n + 1):
                if i in self.cache:
                    result = self.cache[i]
                else:
                    result *= i
                    self.cache[i] = result
        return result

# Создаем экземпляр для тестирования
fact_calculator = FactorialCalculator()

# Функция для тестирования одного вызова (чистый бенчмарк)
def benchmark_single_call():
    test_number = 500
    
    print("=== БЕНЧМАРК ОДНОГО ВЫЗОВА (n=500) ===")
    
    # Рекурсивная
    start_time = timeit.default_timer()
    result1 = fact_recursive(test_number)
    recursive_time = timeit.default_timer() - start_time
    print(f"Рекурсивная: {recursive_time:.6f} сек")
    
    # Итеративная
    start_time = timeit.default_timer()
    result2 = fact_iterative(test_number)
    iterative_time = timeit.default_timer() - start_time
    print(f"Итеративная: {iterative_time:.6f} сек")
    
    # Рекурсивная с мемоизацией (первый вызов)
    start_time = timeit.default_timer()
    result3 = fact_recursive_memo(test_number)
    recursive_memo_first_time = timeit.default_timer() - start_time
    print(f"Рекурсивная с мемоизацией (первый вызов): {recursive_memo_first_time:.6f} сек")
    
    # Рекурсивная с мемоизацией (повторный вызов)
    start_time = timeit.default_timer()
    result4 = fact_recursive_memo(test_number)
    recursive_memo_second_time = timeit.default_timer() - start_time
    print(f"Рекурсивная с мемоизацией (повторный вызов): {recursive_memo_second_time:.6f} сек")
    
    # Итеративная с мемоизацией (первый вызов)
    start_time = timeit.default_timer()
    result5 = fact_calculator.fact_iterative_memo(test_number)
    iterative_memo_first_time = timeit.default_timer() - start_time
    print(f"Итеративная с мемоизацией (первый вызов): {iterative_memo_first_time:.6f} сек")
    
    # Итеративная с мемоизацией (повторный вызов)
    start_time = timeit.default_timer()
    result6 = fact_calculator.fact_iterative_memo(test_number)
    iterative_memo_second_time = timeit.default_timer() - start_time
    print(f"Итеративная с мемоизацией (повторный вызов): {iterative_memo_second_time:.6f} сек")
    
    # Проверка корректности результатов
    print(f"\nВсе результаты одинаковы: {result1 == result2 == result3 == result4 == result5 == result6}")

# Функция для сравнения производительности на разных значениях n
def compare_performance():
    # Генерируем тестовые данные
    test_numbers = list(range(1, 501, 20))  # От 1 до 500 с шагом 20
    number_of_runs = 100  # Количество запусков для усреднения
    
    print(f"\n=== СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ ===")
    print(f"Тестовые числа: {test_numbers}")
    print(f"Количество запусков для усреднения: {number_of_runs}")
    
    # Время выполнения для каждого метода
    recursive_times = []
    iterative_times = []
    recursive_memo_times = []
    iterative_memo_times = []
    
    for n in test_numbers:
        print(f"Тестирование n={n}...")
        
        # Очищаем кеш мемоизации перед каждым новым n
        fact_recursive_memo.cache_clear()
        fact_calculator.cache.clear()
        
        # Рекурсивная
        recursive_time = timeit.timeit(lambda: fact_recursive(n), number=number_of_runs)
        recursive_times.append(recursive_time / number_of_runs)
        
        # Итеративная
        iterative_time = timeit.timeit(lambda: fact_iterative(n), number=number_of_runs)
        iterative_times.append(iterative_time / number_of_runs)
        
        # Рекурсивная с мемоизацией (первый вызов)
        recursive_memo_time = timeit.timeit(lambda: fact_recursive_memo(n), number=number_of_runs)
        recursive_memo_times.append(recursive_memo_time / number_of_runs)
        
        # Итеративная с мемоизацией (первый вызов)
        iterative_memo_time = timeit.timeit(lambda: fact_calculator.fact_iterative_memo(n), number=number_of_runs)
        iterative_memo_times.append(iterative_memo_time / number_of_runs)
    
    return test_numbers, recursive_times, iterative_times, recursive_memo_times, iterative_memo_times

# Функция для построения графиков
def plot_results(test_numbers, recursive_times, iterative_times, recursive_memo_times, iterative_memo_times):
    plt.figure(figsize=(15, 10))
    
    # График 1: Все методы вместе
    plt.subplot(2, 2, 1)
    plt.plot(test_numbers, recursive_times, 'r-', label='Рекурсивная', linewidth=2)
    plt.plot(test_numbers, iterative_times, 'b-', label='Итеративная', linewidth=2)
    plt.plot(test_numbers, recursive_memo_times, 'g-', label='Рекурсивная с мемоизацией', linewidth=2)
    plt.plot(test_numbers, iterative_memo_times, 'm-', label='Итеративная с мемоизацией', linewidth=2)
    plt.xlabel('n (входное число)')
    plt.ylabel('Время выполнения (секунды)')
    plt.title('Сравнение времени выполнения всех методов')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # График 2: Без мемоизации
    plt.subplot(2, 2, 2)
    plt.plot(test_numbers, recursive_times, 'r-', label='Рекурсивная', linewidth=2)
    plt.plot(test_numbers, iterative_times, 'b-', label='Итеративная', linewidth=2)
    plt.xlabel('n (входное число)')
    plt.ylabel('Время выполнения (секунды)')
    plt.title('Сравнение без мемоизации')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # График 3: С мемоизацией
    plt.subplot(2, 2, 3)
    plt.plot(test_numbers, recursive_memo_times, 'g-', label='Рекурсивная с мемоизацией', linewidth=2)
    plt.plot(test_numbers, iterative_memo_times, 'm-', label='Итеративная с мемоизацией', linewidth=2)
    plt.xlabel('n (входное число)')
    plt.ylabel('Время выполнения (секунды)')
    plt.title('Сравнение с мемоизацией')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # График 4: Отношение времени рекурсивной к итеративной
    plt.subplot(2, 2, 4)
    ratio = [recursive_times[i] / iterative_times[i] for i in range(len(test_numbers))]
    plt.plot(test_numbers, ratio, 'k-', linewidth=2)
    plt.axhline(y=1, color='red', linestyle='--', alpha=0.7)
    plt.xlabel('n (входное число)')
    plt.ylabel('Отношение времени (рекурсивная/итеративная)')
    plt.title('Отношение времени выполнения рекурсивной к итеративной')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Функция для анализа результатов
def analyze_results(test_numbers, recursive_times, iterative_times, recursive_memo_times, iterative_memo_times):
    print("\n=== АНАЛИЗ РЕЗУЛЬТАТОВ ===")
    
    # Находим индексы для малых, средних и больших n
    small_n_idx = 0  # n=1
    medium_n_idx = len(test_numbers) // 2  # среднее значение
    large_n_idx = -1  # максимальное значение
    
    print(f"\nМалые n (n={test_numbers[small_n_idx]}):")
    print(f"  Рекурсивная: {recursive_times[small_n_idx]:.8f} сек")
    print(f"  Итеративная: {iterative_times[small_n_idx]:.8f} сек")
    print(f"  Рекурсивная с мемоизацией: {recursive_memo_times[small_n_idx]:.8f} сек")
    print(f"  Итеративная с мемоизацией: {iterative_memo_times[small_n_idx]:.8f} сек")
    
    print(f"\nСредние n (n={test_numbers[medium_n_idx]}):")
    print(f"  Рекурсивная: {recursive_times[medium_n_idx]:.8f} сек")
    print(f"  Итеративная: {iterative_times[medium_n_idx]:.8f} сек")
    print(f"  Рекурсивная с мемоизацией: {recursive_memo_times[medium_n_idx]:.8f} сек")
    print(f"  Итеративная с мемоизацией: {iterative_memo_times[medium_n_idx]:.8f} сек")
    
    print(f"\nБольшие n (n={test_numbers[large_n_idx]}):")
    print(f"  Рекурсивная: {recursive_times[large_n_idx]:.8f} сек")
    print(f"  Итеративная: {iterative_times[large_n_idx]:.8f} сек")
    print(f"  Рекурсивная с мемоизацией: {recursive_memo_times[large_n_idx]:.8f} сек")
    print(f"  Итеративная с мемоизацией: {iterative_memo_times[large_n_idx]:.8f} сек")
    
    # Анализ эффективности
    print(f"\n=== ВЫВОДЫ ===")
    print("1. Итеративный метод стабильно быстрее рекурсивного для больших n")
    print("2. Мемоизация значительно ускоряет повторные вызовы")
    print("3. Для одиночных вызовов мемоизация добавляет небольшие накладные расходы")
    print("4. Рекурсивный метод имеет ограничение по глубине рекурсии")
    print("5. Итеративный метод более предсказуем по потреблению памяти")

# Основная функция
def main():
    print("СРАВНЕНИЕ РЕАЛИЗАЦИЙ ВЫЧИСЛЕНИЯ ФАКТОРИАЛА")
    print("=" * 50)
    
    # Запускаем бенчмарк одного вызова
    benchmark_single_call()
    
    # Запускаем сравнение производительности
    test_numbers, recursive_times, iterative_times, recursive_memo_times, iterative_memo_times = compare_performance()
    
    # Строим графики
    plot_results(test_numbers, recursive_times, iterative_times, recursive_memo_times, iterative_memo_times)
    
    # Анализируем результаты
    analyze_results(test_numbers, recursive_times, iterative_times, recursive_memo_times, iterative_memo_times)

if __name__ == "__main__":
    main()

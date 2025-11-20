
import math

def twoOpt(path, dist):
    """Функция улучшения маршрута методом 2-opt"""
    n = len(path)
    improved = True
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                if j - i == 1:
                    continue
                # Текущая длина ребер (i-1, i) и (j, j+1)
                current = dist[path[i-1]][path[i]] + dist[path[j]][path[(j+1)%n]]
                # Новая длина ребер (i-1, j) и (i, j+1)
                new = dist[path[i-1]][path[j]] + dist[path[i]][path[(j+1)%n]]
                if new < current:
                    # Переворачиваем сегмент между i и j
                    path[i:j+1] = reversed(path[i:j+1])
                    improved = True
    return path

def calculate_distance(city1, city2):
    """Вычисление евклидова расстояния между двумя городами"""
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

def create_distance_matrix(cities):
    """Создание матрицы расстояний между всеми городами"""
    n = len(cities)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = calculate_distance(cities[i], cities[j])
    return dist

def tsp_hybrid(dist):
    n = len(dist)
    # Шаг 1: ближайший сосед
    path = [0]
    visited = [False] * n
    visited[0] = True
    for _ in range(n - 1):
        curr = path[-1]
        next_city = -1
        min_dist = float('inf')
        for j in range(n):
            if not visited[j] and dist[curr][j] < min_dist:
                min_dist = dist[curr][j]
                next_city = j
        path.append(next_city)
        visited[next_city] = True
    # Шаг 2: 2-opt улучшение
    path = twoOpt(path, dist)
    return path

def calculate_total_distance(path, dist):
    """Вычисление общей длины маршрута"""
    total = 0
    n = len(path)
    for i in range(n):
        total += dist[path[i]][path[(i + 1) % n]]
    return total

def main():
    print("=== TSP: Метод ближайшего соседа с улучшением 2-opt ===")
    
    # Ввод количества городов
    while True:
        try:
            n = int(input("Введите количество городов: "))
            if n > 1:
                break
            else:
                print("Количество городов должно быть больше 1")
        except ValueError:
            print("Пожалуйста, введите целое число")
    
    # Ввод координат городов
    cities = []
    print("\nВведите координаты городов (x y):")
    for i in range(n):
        while True:
            try:
                coords = input(f"Город {i}: ").split()
                if len(coords) == 2:
                    x = float(coords[0])
                    y = float(coords[1])
                    cities.append((x, y))
                    break
                else:
                    print("Пожалуйста, введите две координаты через пробел")
            except ValueError:
                print("Пожалуйста, введите числа")
    
    # Создание матрицы расстояний
    dist_matrix = create_distance_matrix(cities)
    
    print("\nМатрица расстояний:")
    for i in range(n):
        for j in range(n):
            print(f"{dist_matrix[i][j]:8.2f}", end=" ")
        print()
    
    # Построение маршрута
    print("\nПостроение маршрута...")
    path = tsp_hybrid(dist_matrix)
    
    # Вывод результатов
    print(f"\nОптимальный маршрут: {path}")
    print(f"Общая длина маршрута: {calculate_total_distance(path, dist_matrix):.2f}")
    
    # Вывод маршрута по порядку
    print("\nПорядок посещения городов:")
    for i, city_idx in enumerate(path):
        print(f"{i+1}. Город {city_idx} ({cities[city_idx][0]}, {cities[city_idx][1]})")
    print(f"Возврат в город {path[0]}")

if __name__ == "__main__":
    main()

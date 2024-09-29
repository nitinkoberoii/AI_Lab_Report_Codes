def tsp_greedy(distances):
    n = len(distances)
    visited = [False] * n
    current_city = 0
    visited[0] = True
    tour = [0]
    total_cost = 0

    for _ in range(n - 1):
        next_city = None
        min_distance = float('inf')

        for city in range(n):
            if not visited[city] and distances[current_city][city] < min_distance:
                next_city = city
                min_distance = distances[current_city][city]

        tour.append(next_city)
        total_cost += min_distance
        visited[next_city] = True
        current_city = next_city

    total_cost += distances[current_city][0]
    tour.append(0)

    return total_cost, tour

# Get user input for number of cities and distances
def get_input():
    n = int(input("Enter the number of cities: "))
    distances = []
    for i in range(n):
        row = list(map(int, input(f"Enter distances from city {i + 1} to other cities (space-separated): ").split()))
        distances.append(row)
    return distances

# Example Usage
distances = get_input()
cost, path = tsp_greedy(distances)
print("Tour cost (Greedy):", cost)
print("Tour path (Greedy):", path)

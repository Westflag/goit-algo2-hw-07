import random
import time
from functools import lru_cache

# --- Config ---
N = 100_000
Q = 50_000
random.seed(42)

# --- Generate initial array ---
array = [random.randint(1, 100) for _ in range(N)]
array_tuple = tuple(array)  # immutable for lru_cache use
array_no_cache = list(array)  # separate for non-cached variant

# --- Generate requests ---
requests = []
precomputed_ranges = []

# Precompute commonly used ranges
for _ in range(1000):
    L = random.randint(0, N - 100)
    R = L + random.randint(1, 100)
    precomputed_ranges.append((L, R))

# Mix of repeated and unique range/update requests
for _ in range(Q):
    if random.random() < 0.85:  # mostly range queries
        if random.random() < 0.6:
            L, R = random.choice(precomputed_ranges)
        else:
            L = random.randint(0, N - 100)
            R = L + random.randint(1, 100)
        requests.append(('Range', L, R))
    else:
        index = random.randint(0, N - 1)
        value = random.randint(1, 100)
        requests.append(('Update', index, value))


# --- Cached using @lru_cache ---
@lru_cache(maxsize=1000)
def range_sum_with_lru_cache(array_tuple, L, R):
    return sum(array_tuple[L:R+1])

def update_array_and_clear_cache(array, index, value):
    array[index] = value
    range_sum_with_lru_cache.cache_clear()
    return tuple(array)


# --- No cache version ---
def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value


# --- Measure time without cache ---
start_no_cache = time.time()
for req in requests:
    if req[0] == 'Range':
        range_sum_no_cache(array_no_cache, req[1], req[2])
    else:
        update_no_cache(array_no_cache, req[1], req[2])
time_no_cache = time.time() - start_no_cache

# --- Measure time with @lru_cache ---
array_lru = list(array)
array_tuple = tuple(array_lru)

start_with_cache = time.time()
for req in requests:
    if req[0] == 'Range':
        range_sum_with_lru_cache(array_tuple, req[1], req[2])
    else:
        array_lru[req[1]] = req[2]
        array_tuple = update_array_and_clear_cache(array_lru, req[1], req[2])
time_with_cache = time.time() - start_with_cache

# --- Results ---
import pandas as pd

if __name__ == '__main__':
    results = pd.DataFrame({
        "Метод": ["Без кешу", "З LRU-кешем"],
        "Час виконання (секунди)": [round(time_no_cache, 4), round(time_with_cache, 4)]
    })
    print("Порівняння часу виконання")
    print(results)

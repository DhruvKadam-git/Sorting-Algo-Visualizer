from flask import Flask, jsonify, request, send_from_directory
import time

app = Flask(__name__, static_folder='static')


# Sorting Algorithms
def bubble_sort(arr):
    steps = []
    n = len(arr)
    start_time = time.time()  # Start timing
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                steps.append(arr[:])  # Capture the state after swap
    end_time = time.time()  # End timing
    return steps, end_time - start_time  # Return time taken


def insertion_sort(arr):
    steps = []
    n = len(arr)
    start_time = time.time()  # Start timing
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            steps.append(arr[:])  # Capture the state after each shift
            j -= 1
        arr[j + 1] = key
        steps.append(arr[:])  # Capture the state after inserting the key
    end_time = time.time()  # End timing
    return steps, end_time - start_time  # Return time taken


def selection_sort(arr):
    steps = []
    n = len(arr)
    start_time = time.time()  # Start timing
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append(arr[:])  # Capture the state after each swap
    end_time = time.time()  # End timing
    return steps, end_time - start_time  # Return time taken


def quick_sort(arr):
    steps = []
    start_time = time.time()  # Start timing

    def quicksort_helper(low, high):
        if low < high:
            pivot_index = partition(low, high)
            quicksort_helper(low, pivot_index - 1)
            quicksort_helper(pivot_index + 1, high)

    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                steps.append(arr[:])  # Capture the state after each swap
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append(arr[:])  # Capture the state after placing the pivot
        return i + 1

    quicksort_helper(0, len(arr) - 1)
    end_time = time.time()  # End timing
    return steps, end_time - start_time  # Return time taken


# API Endpoint for Sorting
@app.route('/sort', methods=['POST'])
def sort_array():
    data = request.json
    array = data.get('array', [])
    algorithm = data.get('algorithm', 'bubble')

    if not array:
        return jsonify({"error": "No array provided"}), 400

    try:
        if algorithm == 'bubble':
            steps, time_taken = bubble_sort(array.copy())
        elif algorithm == 'insertion':
            steps, time_taken = insertion_sort(array.copy())
        elif algorithm == 'selection':
            steps, time_taken = selection_sort(array.copy())
        elif algorithm == 'quick':
            steps, time_taken = quick_sort(array.copy())
        else:
            return jsonify({"error": "Algorithm not supported"}), 400
        return jsonify({"steps": steps, "time_taken": time_taken})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Serve the HTML File
@app.route('/')
def home():
    return send_from_directory('templates', 'index.html')  # Ensure the file exists


if __name__ == '__main__':
    app.run(debug=True, port=2000)

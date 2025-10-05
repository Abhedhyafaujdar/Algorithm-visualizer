# backend.py

def bubble_sort(arr):
    """Yields states for bubble sort visualization."""
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            yield arr[:], (j, j + 1), "Comparing"
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr[:], (j, j + 1), "Swapping"
    yield arr[:], (), "Finished"


def insertion_sort(arr):
    """Yields states for insertion sort visualization."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        yield arr[:], (i, j if j >= 0 else i), "Selecting key"
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr[:], (j + 1, j + 2), "Shifting"
        arr[j + 1] = key
        yield arr[:], (j + 1,), "Placed key"
    yield arr[:], (), "Finished"


# --- NEW AND IMPROVED QUICK SORT ---
def _partition(arr, low, high):
    """
    Partition generator. It yields visualization steps and, upon completion,
    returns the final pivot index.
    """
    pivot_index = high
    pivot_value = arr[pivot_index]
    yield arr[:], (pivot_index,), f"Pivot: {pivot_value}"

    i = low - 1
    for j in range(low, high):
        yield arr[:], (j, pivot_index), "Comparing"
        if arr[j] <= pivot_value:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            yield arr[:], (i, j), "Swapping"

    i += 1
    arr[i], arr[pivot_index] = arr[pivot_index], arr[i]
    yield arr[:], (i, pivot_index), "Placing pivot"

    return i  # Return the pivot index via StopIteration


def _quick_sort_recursive(arr, low, high):
    """A recursive generator that yields steps from the quick sort process."""
    if low < high:
        # The partition process yields its own steps and returns the pivot index
        partition_generator = _partition(arr, low, high)
        pi = 0
        while True:
            try:
                yield next(partition_generator)
            except StopIteration as e:
                pi = e.value  # Get return value from generator
                break

        yield from _quick_sort_recursive(arr, low, pi - 1)
        yield from _quick_sort_recursive(arr, pi + 1, high)


def quick_sort(arr):
    """Wrapper for the recursive quick sort to add the final 'Finished' state."""
    yield from _quick_sort_recursive(arr, 0, len(arr) - 1)
    yield arr[:], (), "Finished"
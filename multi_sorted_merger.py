import heapq
from typing import List

def merge_k_sorted_lists(lists: List[List[int]]) -> List[int]:
    """
    Merges multiple sorted lists into a single sorted list using a min-heap.

    This function efficiently combines K sorted lists containing a total of N elements
    into one sorted list. It uses a priority queue (min-heap) to always select the smallest
    available element from the fronts of the lists, ensuring O(N log K) time complexity.

    For stability, when elements are equal, the order is preserved based on the original
    list order (earlier lists take precedence).

    Args:
        lists: A list of sorted lists to merge. Each inner list should be sorted in ascending order.

    Returns:
        A single sorted list containing all elements from the input lists.

    Raises:
        ValueError: If any inner list is not sorted.

    Example:
        >>> merge_k_sorted_lists([[1, 3, 5], [2, 4, 6], [0, 7]])
        [0, 1, 2, 3, 4, 5, 6, 7]
    """
    # Validate input: ensure all lists are sorted
    for i, lst in enumerate(lists):
        if lst != sorted(lst):
            raise ValueError(f"List at index {i} is not sorted: {lst}")

    # Initialize the min-heap with the first element of each list
    # Each heap entry is a tuple: (value, list_index, element_index)
    # list_index ensures stability by preferring earlier lists for equal values
    heap = []
    for list_idx, lst in enumerate(lists):
        if lst:  # Only add if the list is not empty
            heapq.heappush(heap, (lst[0], list_idx, 0))

    result = []
    while heap:
        # Extract the smallest element
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        # If there are more elements in the same list, push the next one
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return result
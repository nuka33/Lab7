## 1. Multi-Sorted Plan
A multi-sorted list merger can be implemented using a priority queue (min-heap) to efficiently track the smallest element from the front of each sorted list, combined with a result list to accumulate the merged output in order. This approach achieves O(N log K) time complexity, where N is the total number of elements across all lists and K is the number of lists, while ensuring stability by preserving the original order of equal elements from their respective input lists.

## 2. Implementation Code
```python
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
```

## 3. Verification Analysis
Line-by-line, the logic starts by importing `heapq`, which gives the function a min-heap so it can always remove the smallest available value first. The `List` import is only for type hints and does not enforce the input at runtime.

The function definition `merge_k_sorted_lists(lists: List[List[int]]) -> List[int]` says the expected input is a list of sorted integer lists, and the expected output is one sorted integer list. However, Python type hints are not automatic validation, so invalid values like `None` can still be passed in unless the function checks for them.

The first `for i, lst in enumerate(lists):` loop verifies that every inner list is sorted. For each inner list, it compares `lst` with `sorted(lst)`. If they are different, the function raises a `ValueError`, which prevents the merge from continuing with unsorted data. If the outer input list is empty, this loop simply does not run, which is fine.

After validation, `heap = []` creates the priority queue. The next loop, `for list_idx, lst in enumerate(lists):`, goes through each inner list. The condition `if lst:` skips empty lists, so an input like `[[], [1, 2], []]` only pushes values from `[1, 2]`. For non-empty lists, `heapq.heappush(heap, (lst[0], list_idx, 0))` stores the first value, the index of the list it came from, and the index of the value inside that list.

The tuple `(value, list_index, element_index)` is important for duplicate priority values. Python compares tuples from left to right. If two values are equal, it compares `list_index` next, so the value from the earlier input list is popped first. This means duplicate values are handled in sorted order, and the implementation is stable across lists because earlier lists win ties. If duplicates appear inside the same list, the function pushes the next value only after the current one is popped, so the original order within that list is also preserved.

`result = []` creates the final merged output. The `while heap:` loop runs until there are no more values waiting to be merged. Each pass pops the smallest tuple, appends its value to `result`, and then checks whether there is another value in the same source list. If there is, it pushes that next value into the heap. This keeps at most one active value from each list in the heap at a time.

For empty input lists, the current implementation handles them correctly. If the input is `[]`, no values are pushed into the heap, the `while heap:` loop never runs, and the function returns `[]`. If some inner lists are empty, they are skipped by `if lst:` and do not cause an error.

For lists with duplicate priority values, the current implementation also handles them correctly. Equal numbers are not lost or combined. They are all appended to the result, and ties are resolved by the original list index. For example, `[[1, 3], [1, 2]]` would output `[1, 1, 2, 3]`, with the first `1` coming from list index `0`.

For null entries, the current implementation does not handle them safely. If the outer input is `None`, `enumerate(lists)` raises a `TypeError` because `None` is not iterable. If one of the inner lists is `None`, then `sorted(lst)` raises a `TypeError` because `None` cannot be sorted. If an inner list contains `None`, such as `[1, None, 3]`, sorting or heap comparison can also raise a `TypeError` because Python cannot compare `None` with integers. So null values are edge cases that currently fail with runtime errors instead of a custom validation message.

In my own words, I think the main algorithm is solid for the normal expected input because it checks sorted lists first and then uses the heap in a careful way. Empty lists do not break it, and duplicate values are actually handled pretty nicely because of the tuple ordering. The weak spot is null input. The function assumes the caller gives it real lists of numbers, so if `None` shows up, Python throws an error instead of the function explaining the problem. If I were improving this, I would add clear validation for `lists is None`, inner lists being `None`, and elements being `None` before trying to sort or merge.

## 4. Quality Assurance Test Suite
As a Senior QA Engineer, I would focus these tests on reliability and security boundaries instead of only testing the happy path. The current `mapUsersById` function has a high-risk loop condition: `i <= users.length`. Since JavaScript arrays are zero-indexed, the last valid index is `users.length - 1`. Using `<=` causes the loop to read one position past the end of the array, so `users[users.length]` becomes `undefined`, and then `user.id` throws a `TypeError`.

The tests below are written with Node's built-in `node:test` and `assert` modules. They intentionally try to trigger out-of-bounds access, null dereferences, and invalid input type exceptions. These tests do not fix the function; they only expose the current behavior.

```javascript
const test = require("node:test");
const assert = require("node:assert/strict");

// Function under test:
// function mapUsersById(users) {
//   const userMap = {};
//   for (let i = 0; i <= users.length; i++) {
//     const user = users[i];
//     userMap[user.id] = user;
//   }
//   return userMap;
// }

test("throws TypeError for a normal one-user array because loop reads past the end", () => {
  assert.throws(
    () => mapUsersById([{ id: 1, name: "Alice" }]),
    TypeError
  );
});

test("throws TypeError for an empty array because index 0 is out of bounds", () => {
  assert.throws(
    () => mapUsersById([]),
    TypeError
  );
});

test("throws TypeError for multiple valid users after processing the last valid item", () => {
  assert.throws(
    () => mapUsersById([
      { id: 1, name: "Alice" },
      { id: 2, name: "Bob" }
    ]),
    TypeError
  );
});

test("throws TypeError when users argument is null", () => {
  assert.throws(
    () => mapUsersById(null),
    TypeError
  );
});

test("throws TypeError when users argument is undefined", () => {
  assert.throws(
    () => mapUsersById(undefined),
    TypeError
  );
});

test("throws TypeError when users argument is a number", () => {
  assert.throws(
    () => mapUsersById(42),
    TypeError
  );
});

test("throws TypeError when users argument is a plain object without length", () => {
  assert.throws(
    () => mapUsersById({ id: 1, name: "Alice" }),
    TypeError
  );
});

test("throws TypeError when an array contains a null user entry", () => {
  assert.throws(
    () => mapUsersById([{ id: 1, name: "Alice" }, null]),
    TypeError
  );
});

test("throws TypeError when an array contains an undefined user entry", () => {
  assert.throws(
    () => mapUsersById([{ id: 1, name: "Alice" }, undefined]),
    TypeError
  );
});

test("handles a user object missing id before still failing on out-of-bounds access", () => {
  assert.throws(
    () => mapUsersById([{ name: "Missing ID" }]),
    TypeError
  );
});

test("throws TypeError for a sparse array because a hole returns undefined", () => {
  const users = [];
  users[1] = { id: 2, name: "Bob" };

  assert.throws(
    () => mapUsersById(users),
    TypeError
  );
});

test("throws TypeError for an array-like object with length but missing index 0", () => {
  assert.throws(
    () => mapUsersById({ length: 1 }),
    TypeError
  );
});

test("throws TypeError for a string input because characters do not have id properties and the loop still goes out of bounds", () => {
  assert.throws(
    () => mapUsersById("abc"),
    TypeError
  );
});

test("does not protect against dangerous id keys such as __proto__", () => {
  assert.throws(
    () => mapUsersById([{ id: "__proto__", name: "Prototype Attack" }]),
    TypeError
  );
});
```

## 4A. ReAct Refinement Log (mapUsersById)

### Reasoning for Test Failures
The original `mapUsersById` function fails due to an off-by-one error in the loop condition: `i <= users.length` instead of `i < users.length`. This causes the loop to access `users[users.length]`, which is `undefined` in JavaScript arrays, leading to a `TypeError` when attempting `user.id` on `undefined`. Additionally, the function lacks input validation, making it vulnerable to null/undefined inputs, non-array arguments, and invalid user objects (e.g., missing `id` or null entries), resulting in runtime errors rather than graceful handling.

### Strategy for Remediation
1. **Fix Loop Condition**: Change `i <= users.length` to `i < users.length` to prevent out-of-bounds access.
2. **Add Input Validation**: Check if `users` is an array; throw a `TypeError` for invalid types.
3. **Validate User Objects**: Ensure each user is not null/undefined and has a valid `id` property.
4. **Maintain Robustness**: Use descriptive error messages for better debugging, while keeping the function simple and efficient.

### Corrected Code
```javascript
// Corrected function: converts array of users to a map by ID
function mapUsersById(users) {
  // Validate input: ensure users is an array and not null/undefined
  if (!Array.isArray(users)) {
    throw new TypeError("Input must be an array of users.");
  }

  const userMap = {};
  for (let i = 0; i < users.length; i++) {
    const user = users[i];
    // Validate each user has an id
    if (!user || typeof user.id === 'undefined') {
      throw new TypeError(`User at index ${i} is invalid or missing id.`);
    }
    userMap[user.id] = user;
  }
  return userMap;
}
```

Expected QA findings:

- The normal happy-path input currently fails because the loop reads past the final array element.
- Empty arrays fail immediately because `users[0]` is `undefined`.
- `null`, `undefined`, numbers, strings, and plain objects are not validated before the function reads `.length` or `.id`.
- Arrays containing `null`, `undefined`, or sparse holes fail because the function does not check whether each entry is a real user object.
- The function accepts dangerous object keys like `__proto__`, which could become a prototype pollution concern if the out-of-bounds bug were fixed without adding safer map creation or key validation.
- These tests are intentionally failure-focused because the assignment asks for reliability and security test coverage before fixing the implementation.

## 5. Debugging Analysis
The function being debugged is:

```javascript
function mapUsersById(users) {
  const userMap = {};
  for (let i = 0; i <= users.length; i++) {
    const user = users[i];
    userMap[user.id] = user;
  }
  return userMap;
}
```

Using the current example input:

```javascript
mapUsersById([{ id: 1, name: "Alice" }]);
```

Initial state:

- `users = [{ id: 1, name: "Alice" }]`
- `users.length = 1`
- `userMap = {}`

Step-by-step trace:

| Step | `i` | Loop condition | `users[i]` | `userMap` before assignment | Result |
|---|---:|---|---|---|---|
| Start | none | none | none | `{}` | Function creates an empty map. |
| Iteration 1 | `0` | `0 <= 1` is `true` | `{ id: 1, name: "Alice" }` | `{}` | Assigns `userMap[1] = { id: 1, name: "Alice" }`. |
| After iteration 1 | `0` | none | `{ id: 1, name: "Alice" }` | `{ "1": { id: 1, name: "Alice" } }` | This part is correct. |
| Iteration 2 | `1` | `1 <= 1` is `true` | `undefined` | `{ "1": { id: 1, name: "Alice" } }` | Code tries to read `user.id`, but `user` is `undefined`. |

The logic goes wrong in this line:

```javascript
for (let i = 0; i <= users.length; i++) {
```

The problem is the `<=` comparison. Array indexes start at `0`, so for an array with length `1`, the only valid index is `0`. When `i` becomes `1`, the loop still runs because `1 <= users.length` is true. But `users[1]` is outside the array, so it returns `undefined`.

Then this line fails:

```javascript
userMap[user.id] = user;
```

At that moment:

- `i = 1`
- `users[i] = undefined`
- `user = undefined`
- `userMap = { "1": { id: 1, name: "Alice" } }`

The function is not accumulating correctly because it crashes after processing the valid user but before reaching `return userMap`. The map actually does contain Alice briefly, but the extra out-of-bounds loop iteration causes a `TypeError`, so the caller never receives the accumulated result.

In my own words, the loop is going one step too far. It should stop before `i` reaches `users.length`, because `users.length` is a count, not the last index. The last valid index is always `users.length - 1`.

## 6. Agent B Test Findings
As Agent B, the Test Generation Agent, I reviewed `weighted_stats.py` and focused on edge-case inputs that could break `calculate_weighted_stats(values, weights)` or expose missing validation. The function checks for mismatched lengths, empty `values`, non-positive weights, and zero total weight. However, it does not explicitly check whether every value and weight is numeric and finite.

Recommended edge-case test inputs:

| Test Case | `values` | `weights` | Expected Behavior / Risk |
|---|---|---|---|
| Empty arrays | `[]` | `[]` | Should raise `ValueError` because the function checks `if not values`. |
| Empty values with non-empty weights | `[]` | `[1.0]` | Should raise `ValueError` for mismatched lengths before the empty-list check. |
| Non-empty values with empty weights | `[10.0]` | `[]` | Should raise `ValueError` for mismatched lengths. |
| Mismatched lengths, extra value | `[1.0, 2.0, 3.0]` | `[1.0, 2.0]` | Should raise `ValueError` because lengths are not equal. |
| Mismatched lengths, extra weight | `[1.0, 2.0]` | `[1.0, 2.0, 3.0]` | Should raise `ValueError` because lengths are not equal. |
| Zero weight | `[1.0, 2.0, 3.0]` | `[1.0, 0.0, 1.0]` | Should raise `ValueError` because the function rejects `w <= 0`. |
| All zero weights | `[1.0, 2.0, 3.0]` | `[0.0, 0.0, 0.0]` | Should raise `ValueError` during the positive-weight validation. |
| Negative weight | `[1.0, 2.0, 3.0]` | `[1.0, -2.0, 1.0]` | Should raise `ValueError` because negative weights are invalid. |
| Very small positive weights | `[1.0, 2.0]` | `[1e-300, 1e-300]` | May work, but this tests floating-point underflow/precision risk. |
| Very large floating-point values | `[1e308, 1e308]` | `[1.0, 1.0]` | `weighted_sum` may become `inf`, which can lead to `inf` mean and unreliable standard deviation. |
| Mixed huge positive and negative values | `[1e308, -1e308]` | `[1.0, 1.0]` | May return a mean near `0`, but variance calculation can overflow to `inf`. |
| Infinite value | `[1.0, float("inf")]` | `[1.0, 1.0]` | Current function does not reject infinity; result may become `inf` or `nan`. |
| NaN value | `[1.0, float("nan")]` | `[1.0, 1.0]` | Current function does not reject `nan`; result likely becomes `nan`. |
| Infinite weight | `[1.0, 2.0]` | `[1.0, float("inf")]` | Current function does not reject infinity; division may produce `nan` or misleading results. |
| NaN weight | `[1.0, 2.0]` | `[1.0, float("nan")]` | `w <= 0` is false for `nan`, so it can pass validation and poison the result as `nan`. |
| Non-numeric string in values | `[1.0, "bad", 3.0]` | `[1.0, 1.0, 1.0]` | Should raise `TypeError` during multiplication or subtraction because strings are not valid numeric values. |
| Numeric-looking string in values | `[1.0, "2.0", 3.0]` | `[1.0, 1.0, 1.0]` | Current function does not convert strings; likely raises `TypeError`. |
| Non-numeric string in weights | `[1.0, 2.0, 3.0]` | `[1.0, "bad", 1.0]` | Should raise `TypeError` during `w <= 0` because a string cannot be compared with an integer. |
| `None` in values | `[1.0, None, 3.0]` | `[1.0, 1.0, 1.0]` | Should raise `TypeError` during arithmetic. |
| `None` in weights | `[1.0, 2.0, 3.0]` | `[1.0, None, 1.0]` | Should raise `TypeError` during `w <= 0`. |

Example unit tests I would generate:

```python
import math
import pytest

from weighted_stats import calculate_weighted_stats


def test_empty_arrays_raise_value_error():
    with pytest.raises(ValueError):
        calculate_weighted_stats([], [])


def test_mismatched_lengths_extra_value_raise_value_error():
    with pytest.raises(ValueError):
        calculate_weighted_stats([1.0, 2.0, 3.0], [1.0, 2.0])


def test_mismatched_lengths_extra_weight_raise_value_error():
    with pytest.raises(ValueError):
        calculate_weighted_stats([1.0, 2.0], [1.0, 2.0, 3.0])


def test_zero_weight_raises_value_error():
    with pytest.raises(ValueError):
        calculate_weighted_stats([1.0, 2.0, 3.0], [1.0, 0.0, 1.0])


def test_negative_weight_raises_value_error():
    with pytest.raises(ValueError):
        calculate_weighted_stats([1.0, 2.0, 3.0], [1.0, -2.0, 1.0])


def test_non_numeric_string_value_raises_type_error():
    with pytest.raises(TypeError):
        calculate_weighted_stats([1.0, "bad", 3.0], [1.0, 1.0, 1.0])


def test_non_numeric_string_weight_raises_type_error():
    with pytest.raises(TypeError):
        calculate_weighted_stats([1.0, 2.0, 3.0], [1.0, "bad", 1.0])


def test_none_value_raises_type_error():
    with pytest.raises(TypeError):
        calculate_weighted_stats([1.0, None, 3.0], [1.0, 1.0, 1.0])


def test_none_weight_raises_type_error():
    with pytest.raises(TypeError):
        calculate_weighted_stats([1.0, 2.0, 3.0], [1.0, None, 1.0])


def test_nan_weight_produces_non_finite_result_current_behavior():
    mean, std_dev = calculate_weighted_stats([1.0, 2.0], [1.0, float("nan")])
    assert math.isnan(mean)
    assert math.isnan(std_dev)


def test_very_large_values_can_overflow_current_behavior():
    mean, std_dev = calculate_weighted_stats([1e308, 1e308], [1.0, 1.0])
    assert not math.isfinite(mean) or not math.isfinite(std_dev)
```

Agent B finding: the implementation is mostly protected against basic shape errors like empty arrays, mismatched lengths, zero weights, and negative weights. The bigger reliability gap is that it trusts the contents of the arrays too much. Non-numeric strings and `None` values cause raw `TypeError`s, while `nan` and `inf` can pass through and create non-finite results instead of being rejected with a clear validation error.

## 7. Agent A Refinement (Weighted Stats)
### Reasoning for Test Failures (Python calculate_weighted_stats)
The original `calculate_weighted_stats` function handles basic validations like mismatched lengths, empty lists, non-positive weights, and zero sum weights. However, it does not validate that all values and weights are numeric types (int or float) or finite numbers. Non-numeric strings, None, nan, or inf values cause TypeError during arithmetic operations or allow invalid computations that produce nan/inf results, leading to unreliable outputs instead of clear error messages.

### Strategy for Remediation (Python calculate_weighted_stats)
1. **Add Type Validation**: Ensure all values and weights are instances of int or float.
2. **Add Finiteness Validation**: Use `math.isfinite()` to reject nan and inf values.
3. **Raise Descriptive Errors**: Provide clear ValueError messages for invalid inputs.
4. **Maintain Efficiency**: Perform validations early to avoid unnecessary computations.

### Corrected Code (Python calculate_weighted_stats)
```python
from typing import List, Tuple
import math

def calculate_weighted_stats(values: List[float], weights: List[float]) -> Tuple[float, float]:
    """
    Calculates the weighted average and weighted standard deviation of a dataset.

    This function computes the weighted mean and the weighted standard deviation
    for a set of values with corresponding weights. The weighted mean is the sum
    of each value multiplied by its weight, divided by the sum of the weights.
    The weighted standard deviation is the square root of the weighted variance,
    where the variance is the sum of weights times squared differences from the mean,
    divided by the sum of weights.

    Args:
        values: A list of numerical values (floats or ints).
        weights: A list of positive weights corresponding to each value. Must be the same length as values.

    Returns:
        A tuple containing:
        - weighted_average: The weighted average of the values.
        - weighted_std_dev: The weighted standard deviation of the values.

    Raises:
        ValueError: If the lengths of values and weights do not match, if weights contain non-positive values,
                    if values or weights are empty, if the sum of weights is zero, if any value or weight is not
                    a finite number, or if any value or weight is not numeric.

    Example:
        >>> values = [1.0, 2.0, 3.0]
        >>> weights = [1.0, 2.0, 3.0]
        >>> mean, std = calculate_weighted_stats(values, weights)
        >>> print(f"Mean: {mean:.2f}, Std Dev: {std:.2f}")
        Mean: 2.33, Std Dev: 0.82
    """
    # Validate input lengths
    if len(values) != len(weights):
        raise ValueError("The lengths of values and weights must be equal.")

    # Validate non-empty inputs
    if not values:
        raise ValueError("Values and weights lists cannot be empty.")

    # Validate all values and weights are numeric and finite
    for i, v in enumerate(values):
        if not isinstance(v, (int, float)):
            raise ValueError(f"Value at index {i} is not a number: {v}")
        if not math.isfinite(v):
            raise ValueError(f"Value at index {i} is not finite: {v}")

    for i, w in enumerate(weights):
        if not isinstance(w, (int, float)):
            raise ValueError(f"Weight at index {i} is not a number: {w}")
        if not math.isfinite(w):
            raise ValueError(f"Weight at index {i} is not finite: {w}")

    # Validate weights are positive
    if any(w <= 0 for w in weights):
        raise ValueError("All weights must be positive numbers.")

    # Calculate sum of weights
    sum_weights = sum(weights)
    if sum_weights == 0:
        raise ValueError("The sum of weights cannot be zero.")

    # Calculate weighted mean
    weighted_sum = sum(v * w for v, w in zip(values, weights))
    weighted_mean = weighted_sum / sum_weights

    # Calculate weighted variance
    variance_sum = sum(w * (v - weighted_mean) ** 2 for v, w in zip(values, weights))
    weighted_variance = variance_sum / sum_weights

    # Calculate weighted standard deviation
    weighted_std_dev = math.sqrt(weighted_variance)

    return weighted_mean, weighted_std_dev
```

## 8. Final Conclusion and Reflection
Overall, this lab showed me why an autonomous workflow needs more structure than just asking an AI to write code. In Phase 1, the Plan, Execute, Verify, and Report process made the multi-sorted merger more predictable because the design was explained before code was generated. That helped me focus on the min-heap approach, time complexity, and stability instead of jumping straight into implementation. The verification step also made the remaining risks easier to see, especially around `None` inputs and type validation.

For Phase 2, the QA and debugging work showed the 70 Percent Problem clearly. The `mapUsersById` function looked simple and almost correct, but the line-by-line trace showed that `i <= users.length` caused an out-of-bounds read. The function briefly builds the right map, but it crashes before returning it. This helped me understand that code can look finished while still failing on a basic happy-path input.

For Phase 3, I used Agent A as the code-generation/refinement agent through Copilot in VS Code, and I used Codex as Agent B, the test-generation agent. This multi-agent setup was useful because Agent B was intentionally more aggressive and looked for edge cases such as empty arrays, mismatched lengths, zero and negative weights, huge floating-point numbers, `nan`, `inf`, `None`, and non-numeric strings. Then Agent A could use those findings to refine the weighted statistics function with better validation.

Completeness check:

- Multi-Sorted Plan: included in Section 1.
- Implementation Code: included in Section 2 with a standard Markdown Python code block.
- Verification Analysis: included in Section 3.
- Quality Assurance Test Suite: included in Section 4.
- Rubber Duck Debugging Analysis: included in Section 5.
- Agent B Test Findings: included in Section 6.
- ReAct Refinement Log: included in Sections 4A and 7, with the weighted stats refinement showing the main Agent A/Agent B orchestration loop.
- Remaining technical debt: `merge_k_sorted_lists` should still add clearer validation for `None` and non-list inputs, and `mapUsersById` should avoid prototype pollution risks by using safer map creation or key validation if it is repaired in the actual source file.

My final takeaway is that structured prompting made the work feel more like an engineering process instead of a guessing process. Planning helped set the direction, verification caught hidden assumptions, and the separate Agent B testing role pushed the code harder than I probably would have on my own. In the future, I think autonomous agents could automate more of the verification stage by generating edge-case tests, running them, summarizing failures, and sending only the evidence-based repair tasks back to the code-generation agent.

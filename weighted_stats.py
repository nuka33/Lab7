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
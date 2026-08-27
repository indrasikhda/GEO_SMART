import numpy as np

# Saaty's Random Index (RI) lookup table
RANDOM_INDEX = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
}

CRITERIA_LIST = [
    {"id": "geology", "name": "Geology / Lithology"},
    {"id": "fault", "name": "Fault & Shear Traces"},
    {"id": "manifestation", "name": "Geothermal Manifestations"},
    {"id": "lineament", "name": "Lineament Density"},
    {"id": "lst", "name": "Land Surface Temp (LST)"},
    {"id": "ndvi", "name": "NDVI (Stress / Alteration)"},
    {"id": "seismicity", "name": "Micro-Seismicity"},
    {"id": "alteration", "name": "Hydrothermal Alteration"}
]

def calculate_fahp_weights(matrix):
    """
    Calculates normalized weights and Consistency Ratio (CR) from an NxN pairwise comparison matrix.
    Using Row Geometric Mean Method (Logarithmic Least Squares).
    """
    A = np.array(matrix, dtype=np.float64)
    n = A.shape[0]

    # Step 1: Geometric mean per row
    row_geo = np.prod(A, axis=1) ** (1.0 / n)

    # Step 2: Normalized Weights vector
    sum_geo = np.sum(row_geo)
    weights = row_geo / sum_geo

    # Step 3: Consistency Calculation
    # A * w
    Aw = np.dot(A, weights)
    
    # Lambda Max
    lambda_max = float(np.mean(Aw / weights))

    # Consistency Index (CI)
    CI = (lambda_max - n) / (n - 1) if n > 1 else 0.0

    # Consistency Ratio (CR)
    RI = RANDOM_INDEX.get(n, 1.41)
    CR = CI / RI if RI > 0 else 0.0
    is_consistent = CR < 0.10

    return {
        "weights": weights.tolist(),
        "lambda_max": round(lambda_max, 4),
        "CI": round(CI, 4),
        "CR": round(CR, 4),
        "is_consistent": is_consistent,
        "status": "Acceptable (CR < 0.10)" if is_consistent else "Inconsistent Matrix (CR >= 0.10)"
    }

def get_default_pairwise_matrix():
    """
    Returns initial default 8x8 pairwise comparison matrix
    """
    # Default relative preference ratios
    prefs = [0.18, 0.22, 0.25, 0.10, 0.12, 0.05, 0.04, 0.04]
    n = len(prefs)
    matrix = np.ones((n, n), dtype=np.float64)
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i, j] = prefs[i] / prefs[j]
    return matrix.tolist()

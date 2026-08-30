import numpy as np


# ============================================================
# SAATY RANDOM INDEX
# ============================================================

RANDOM_INDEX = {
    1: 0.00,
    2: 0.00,
    3: 0.58,
    4: 0.90,
    5: 1.12,
    6: 1.24,
    7: 1.32,
    8: 1.41,
    9: 1.45,
    10: 1.49,
}


# ============================================================
# 5 CURRENT DECISION CRITERIA
# Literature-informed from Şener & Şener (2021)
# ============================================================

CRITERIA_LIST = [
    {
        "id": "manifestation",
        "name": "Geothermal Manifestation",
        "lit_weight": 0.447,
        "role": "Surface thermal manifestations & hot springs",
    },
    {
        "id": "geology",
        "name": "Geology / Lithology",
        "lit_weight": 0.273,
        "role": "Volcanic lithological & reservoir formation",
    },
    {
        "id": "alteration",
        "name": "Hydrothermal Alteration",
        "lit_weight": 0.149,
        "role": "Hydrothermal mineral alteration",
    },
    {
        "id": "lineament",
        "name": "Fault & Lineament Density",
        "lit_weight": 0.079,
        "role": "Structural fluid pathways & fault density",
    },
    {
        "id": "lst",
        "name": "Land Surface Temperature (LST)",
        "lit_weight": 0.052,
        "role": "Satellite thermal anomaly detection",
    },
]


# ============================================================
# LITERATURE FUZZY PAIRWISE COMPARISON MATRIX
#
# Based on Table 2:
# "Comparison matrix and crisp weights of using criteria"
#
# Each comparison is represented as a Triangular Fuzzy Number:
# (lower, middle, upper)
#
# Example:
# (1, 3, 4) = criterion i is approximately 3-4 times
#             more important than criterion j.
# ============================================================

FUZZY_PAIRWISE_MATRIX = [
    # Geothermal Manifestation
    [
        (1, 1, 1),
        (1, 3, 4),
        (3, 4, 5),
        (3, 4, 6),
        (4, 5, 6),
    ],

    # Geology / Lithology
    [
        (1 / 4, 1 / 3, 1),
        (1, 1, 1),
        (2, 3, 4),
        (3, 4, 6),
        (4, 5, 7),
    ],

    # Hydrothermal Alteration
    [
        (1 / 5, 1 / 4, 1 / 3),
        (1 / 4, 1 / 3, 1 / 2),
        (1, 1, 1),
        (1, 3, 4),
        (3, 4, 5),
    ],

    # Fault & Lineament
    [
        (1 / 6, 1 / 4, 1 / 3),
        (1 / 6, 1 / 4, 1 / 3),
        (1 / 4, 1 / 3, 1 / 2),
        (1, 1, 1),
        (1, 2, 3),
    ],

    # Land Surface Temperature
    [
        (1 / 6, 1 / 5, 1 / 4),
        (1 / 7, 1 / 5, 1 / 4),
        (1 / 5, 1 / 4, 1 / 3),
        (1 / 3, 1 / 2, 1),
        (1, 1, 1),
    ],
]


# ============================================================
# FUZZY MATRIX VALIDATION
# ============================================================

def _validate_fuzzy_matrix(matrix):
    """
    Validate that the fuzzy pairwise matrix is a square NxN
    matrix containing triangular fuzzy numbers (l, m, u).
    """

    if not matrix:
        raise ValueError("Pairwise matrix cannot be empty.")

    n = len(matrix)

    if any(len(row) != n for row in matrix):
        raise ValueError("Pairwise matrix must be square.")

    for i in range(n):
        for j in range(n):
            value = matrix[i][j]

            if not isinstance(value, (tuple, list)) or len(value) != 3:
                raise ValueError(
                    f"Matrix[{i}][{j}] must contain "
                    "(lower, middle, upper)."
                )

            l, m, u = map(float, value)

            if l <= 0 or m <= 0 or u <= 0:
                raise ValueError(
                    f"Matrix[{i}][{j}] contains non-positive values."
                )

            if not (l <= m <= u):
                raise ValueError(
                    f"Matrix[{i}][{j}] must satisfy lower <= middle <= upper."
                )


# ============================================================
# DEFUZZIFICATION
# ============================================================

def _defuzzify_fuzzy_number(fuzzy_number):
    """
    Centroid / arithmetic mean defuzzification.

    TFN (l, m, u) -> (l + m + u) / 3
    """

    l, m, u = fuzzy_number
    return (float(l) + float(m) + float(u)) / 3.0


def defuzzify_matrix(fuzzy_matrix):
    """
    Convert a triangular fuzzy pairwise matrix into
    a crisp pairwise comparison matrix.
    """

    _validate_fuzzy_matrix(fuzzy_matrix)

    return np.array(
        [
            [
                _defuzzify_fuzzy_number(fuzzy_matrix[i][j])
                for j in range(len(fuzzy_matrix))
            ]
            for i in range(len(fuzzy_matrix))
        ],
        dtype=np.float64,
    )


# ============================================================
# CRISP AHP CONSISTENCY CHECK
# ============================================================

def _calculate_consistency(matrix, weights):
    """
    Calculate Lambda Max, CI and CR from the defuzzified
    pairwise comparison matrix.

    This is used as a consistency diagnostic for the
    literature-informed fuzzy comparison matrix.
    """

    A = np.asarray(matrix, dtype=np.float64)
    weights = np.asarray(weights, dtype=np.float64)

    n = A.shape[0]

    if n <= 1:
        return {
            "lambda_max": 1.0,
            "CI": 0.0,
            "CR": 0.0,
            "is_consistent": True,
            "status": "Acceptable (CR < 0.10)",
        }

    if np.any(weights <= 0):
        return {
            "lambda_max": float(n),
            "CI": 0.0,
            "CR": 0.0,
            "is_consistent": False,
            "status": "Invalid weights",
        }

    Aw = np.dot(A, weights)

    lambda_values = Aw / weights
    lambda_max = float(np.mean(lambda_values))

    CI = (lambda_max - n) / (n - 1)

    RI = RANDOM_INDEX.get(n, 1.12)

    CR = CI / RI if RI > 0 else 0.0

    is_consistent = CR < 0.10

    return {
        "lambda_max": round(lambda_max, 4),
        "CI": round(CI, 4),
        "CR": round(CR, 4),
        "is_consistent": is_consistent,
        "status": (
            "Acceptable (CR < 0.10)"
            if is_consistent
            else "Inconsistent Matrix (CR >= 0.10)"
        ),
    }


# ============================================================
# FUZZY AHP WEIGHT CALCULATION
# ============================================================

def _calculate_fuzzy_weights(matrix):
    """
    Calculate preliminary FAHP weights from a triangular
    fuzzy pairwise comparison matrix.

    Method:
        1. Calculate fuzzy geometric mean for each row.
        2. Calculate fuzzy total.
        3. Normalize fuzzy row geometric means.
        4. Defuzzify the resulting fuzzy weights.
        5. Normalize the crisp weights so their sum = 1.

    This keeps the calculation transparent and reproducible.
    """

    _validate_fuzzy_matrix(matrix)

    n = len(matrix)

    fuzzy_geometric_means = []

    for i in range(n):

        product_l = 1.0
        product_m = 1.0
        product_u = 1.0

        for j in range(n):
            l, m, u = matrix[i][j]

            product_l *= float(l)
            product_m *= float(m)
            product_u *= float(u)

        fuzzy_geometric_means.append(
            (
                product_l ** (1.0 / n),
                product_m ** (1.0 / n),
                product_u ** (1.0 / n),
            )
        )

    # Sum of fuzzy geometric means
    total_l = sum(x[0] for x in fuzzy_geometric_means)
    total_m = sum(x[1] for x in fuzzy_geometric_means)
    total_u = sum(x[2] for x in fuzzy_geometric_means)

    # Fuzzy normalization
    fuzzy_weights = []

    for l, m, u in fuzzy_geometric_means:

        normalized = (
            l / total_u,
            m / total_m,
            u / total_l,
        )

        fuzzy_weights.append(normalized)

    # Defuzzification
    crisp_weights = np.array(
        [
            _defuzzify_fuzzy_number(weight)
            for weight in fuzzy_weights
        ],
        dtype=np.float64,
    )

    # Final normalization
    weight_sum = float(np.sum(crisp_weights))

    if weight_sum > 0:
        crisp_weights = crisp_weights / weight_sum
    else:
        crisp_weights = np.ones(n) / n

    return crisp_weights, fuzzy_geometric_means, fuzzy_weights


# ============================================================
# PUBLIC FAHP FUNCTION
# ============================================================

def calculate_fahp_weights(matrix=None):
    """
    Calculate literature-informed FAHP weights.

    Parameters
    ----------
    matrix : optional
        Triangular fuzzy pairwise comparison matrix.

        If omitted, the literature-informed matrix from
        Şener & Şener (2021) is used.

    Returns
    -------
    dict
        Contains:
        - weights
        - lambda_max
        - CI
        - CR
        - consistency status
        - method
        - source
        - criteria
    """

    if matrix is None:
        matrix = FUZZY_PAIRWISE_MATRIX

    _validate_fuzzy_matrix(matrix)

    # --------------------------------------------------------
    # Step 1 — Defuzzify matrix for consistency diagnostics
    # --------------------------------------------------------

    crisp_matrix = defuzzify_matrix(matrix)

    # --------------------------------------------------------
    # Step 2 — Calculate FAHP weights
    # --------------------------------------------------------

    weights, fuzzy_geometric_means, fuzzy_weights = (
        _calculate_fuzzy_weights(matrix)
    )

    # --------------------------------------------------------
    # Step 3 — Consistency diagnostic
    # --------------------------------------------------------

    consistency = _calculate_consistency(
        crisp_matrix,
        weights,
    )

    return {
        "weights": [
            round(float(w), 4)
            for w in weights
        ],

        "weights_percent": [
            round(float(w * 100), 2)
            for w in weights
        ],

        "lambda_max": consistency["lambda_max"],

        "CI": consistency["CI"],

        "CR": consistency["CR"],

        "is_consistent": consistency["is_consistent"],

        "status": consistency["status"],

        "method": (
            "Literature-informed Fuzzy AHP "
            "using triangular fuzzy pairwise comparisons"
        ),

        "source": "Şener & Şener (2021)",

        "criteria": [
            criterion["name"]
            for criterion in CRITERIA_LIST
        ],

        "fuzzy_geometric_means": [
            [
                round(float(value), 6)
                for value in fuzzy_number
            ]
            for fuzzy_number in fuzzy_geometric_means
        ],

        "fuzzy_weights": [
            [
                round(float(value), 6)
                for value in fuzzy_number
            ]
            for fuzzy_number in fuzzy_weights
        ],

        "crisp_matrix": [
            [
                round(float(value), 4)
                for value in row
            ]
            for row in crisp_matrix
        ],
    }


# ============================================================
# DEFAULT LITERATURE-INFORMED MATRIX
# ============================================================

def get_default_pairwise_matrix():
    """
    Returns the literature-informed 5x5 triangular fuzzy
    pairwise comparison matrix from Şener & Şener (2021).

    Criteria order:

    1. Geothermal Manifestation
    2. Geology / Lithology
    3. Hydrothermal Alteration
    4. Fault & Lineament Density
    5. Land Surface Temperature (LST)
    """

    return [
        [
            tuple(round(float(x), 6) for x in value)
            for value in row
        ]
        for row in FUZZY_PAIRWISE_MATRIX
    ]


# ============================================================
# LITERATURE REFERENCE WEIGHTS
# ============================================================

def get_literature_weights():
    """
    Returns the crisp criterion weights reported in the
    literature source.

    These values are kept separately from calculated FAHP
    weights so the dashboard can distinguish between:

        1. Literature-reported benchmark
        2. System-calculated FAHP result
    """

    return [
        round(float(criterion["lit_weight"]), 4)
        for criterion in CRITERIA_LIST
    ]
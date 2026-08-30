import numpy as np


# ============================================================
# GPI — GEOTHERMAL PROSPECTIVITY INDEX
# ============================================================

CRITERIA_IDS = [
    "manifestation",
    "geology",
    "alteration",
    "lineament",
    "lst",
]


CRITERIA_NAMES = [
    "Geothermal Manifestation",
    "Geology / Lithology",
    "Hydrothermal Alteration",
    "Fault & Lineament Density",
    "Land Surface Temperature (LST)",
]


# ============================================================
# GPI CLASSIFICATION
# ============================================================

def classify_gpi(score):
    """
    Classify the normalized GPI score.

    GPI range:
        0.00 – 1.00

    Classification:
        >= 0.70 : High Prospect
        >= 0.50 : Moderate Prospect
        <  0.50 : Low Prospect
    """

    score = float(score)

    if score >= 0.70:
        return "High Prospect"

    elif score >= 0.50:
        return "Moderate Prospect"

    return "Low Prospect"


# ============================================================
# INPUT VALIDATION
# ============================================================

def _validate_inputs(weights, evidence_scores):
    """
    Validate weights and standardized evidence scores.
    """

    w = np.asarray(weights, dtype=np.float64)
    s = np.asarray(evidence_scores, dtype=np.float64)

    if len(w) != len(CRITERIA_IDS):
        raise ValueError(
            f"Expected {len(CRITERIA_IDS)} criterion weights, "
            f"received {len(w)}."
        )

    if len(s) != len(CRITERIA_IDS):
        raise ValueError(
            f"Expected {len(CRITERIA_IDS)} evidence scores, "
            f"received {len(s)}."
        )

    if np.any(~np.isfinite(w)):
        raise ValueError("Weights contain invalid numeric values.")

    if np.any(~np.isfinite(s)):
        raise ValueError(
            "Evidence scores contain invalid numeric values."
        )

    if np.any(s < 0) or np.any(s > 1):
        raise ValueError(
            "Standardized evidence scores must be between 0.0 and 1.0."
        )

    if np.sum(w) <= 0:
        raise ValueError(
            "The sum of weights must be greater than zero."
        )

    return w, s


# ============================================================
# WEIGHTED OVERLAY
# ============================================================

def compute_gpi_score(weights, evidence_scores):
    """
    Computes the Geothermal Prospectivity Index (GPI)
    using standardized multi-source evidence.

    Formula:

        GPI(x,y) = Σ [w_i × S_i(x,y)]

    where:

        w_i = FAHP criterion weight
        S_i = standardized evidence score (0–1)

    Current criteria:

        1. Geothermal Manifestation
        2. Geology / Lithology
        3. Hydrothermal Alteration
        4. Fault & Lineament Density
        5. Land Surface Temperature (LST)

    IMPORTANT:
        Evidence scores must come from the standardized
        evidence layers. No synthetic evidence values are
        generated inside this function.
    """

    w, s = _validate_inputs(
        weights,
        evidence_scores,
    )

    # --------------------------------------------------------
    # Normalize weights
    # --------------------------------------------------------

    weight_sum = np.sum(w)

    w = w / weight_sum

    # --------------------------------------------------------
    # Calculate contribution of each criterion
    # --------------------------------------------------------

    contributions = w * s

    # --------------------------------------------------------
    # Weighted overlay
    # --------------------------------------------------------

    gpi_val = float(np.sum(contributions))

    # Keep numerical result inside [0, 1]
    gpi_val = float(
        np.clip(gpi_val, 0.0, 1.0)
    )

    # --------------------------------------------------------
    # Classification
    # --------------------------------------------------------

    prospect_class = classify_gpi(gpi_val)

    # --------------------------------------------------------
    # Return structured result
    # --------------------------------------------------------

    return {
        "gpi_score": round(gpi_val, 4),

        "gpi_percent": round(
            gpi_val * 100,
            2,
        ),

        "class": prospect_class,

        "confidence": (
            "Preliminary — "
            "Literature-Informed Prototype"
        ),

        "criteria": [
            {
                "id": CRITERIA_IDS[i],
                "name": CRITERIA_NAMES[i],
                "weight": round(
                    float(w[i]),
                    4,
                ),
                "weight_percent": round(
                    float(w[i] * 100),
                    2,
                ),
                "standardized_score": round(
                    float(s[i]),
                    4,
                ),
                "contribution": round(
                    float(contributions[i]),
                    4,
                ),
            }
            for i in range(len(CRITERIA_IDS))
        ],
    }


# ============================================================
# SPATIAL GPI
# ============================================================

def compute_gpi_raster(weights, evidence_rasters):
    """
    Computes pixel-wise GPI from standardized raster layers.

    Parameters
    ----------
    weights : array-like
        Five FAHP criterion weights.

    evidence_rasters : list
        Five standardized raster arrays.
        Each raster must contain values in [0, 1].

    Returns
    -------
    numpy.ndarray
        GPI raster with values in [0, 1].

    Formula:

        GPI(x,y) =
            w1*S1(x,y) +
            w2*S2(x,y) +
            ...
            w5*S5(x,y)

    This is the spatial implementation of the
    weighted-overlay stage.
    """

    if len(evidence_rasters) != len(CRITERIA_IDS):
        raise ValueError(
            f"Expected {len(CRITERIA_IDS)} evidence rasters, "
            f"received {len(evidence_rasters)}."
        )

    w = np.asarray(
        weights,
        dtype=np.float64,
    )

    if len(w) != len(CRITERIA_IDS):
        raise ValueError(
            f"Expected {len(CRITERIA_IDS)} weights, "
            f"received {len(w)}."
        )

    if np.sum(w) <= 0:
        raise ValueError(
            "The sum of weights must be greater than zero."
        )

    # Normalize FAHP weights
    w = w / np.sum(w)

    # Convert raster layers
    rasters = [
        np.asarray(
            raster,
            dtype=np.float64,
        )
        for raster in evidence_rasters
    ]

    # Ensure all raster dimensions are identical
    reference_shape = rasters[0].shape

    for i, raster in enumerate(rasters):

        if raster.shape != reference_shape:
            raise ValueError(
                f"Evidence raster {i} has shape "
                f"{raster.shape}, expected "
                f"{reference_shape}."
            )

        if np.any(~np.isfinite(raster)):
            raise ValueError(
                f"Evidence raster {i} contains "
                "invalid numeric values."
            )

        if np.any(raster < 0) or np.any(raster > 1):
            raise ValueError(
                f"Evidence raster {i} contains values "
                "outside the standardized range [0, 1]."
            )

    # --------------------------------------------------------
    # Weighted overlay
    # --------------------------------------------------------

    gpi_raster = np.zeros(
        reference_shape,
        dtype=np.float64,
    )

    for i in range(len(CRITERIA_IDS)):
        gpi_raster += (
            w[i] * rasters[i]
        )

    # Ensure numerical range
    gpi_raster = np.clip(
        gpi_raster,
        0.0,
        1.0,
    )

    return gpi_raster


# ============================================================
# GPI ZONE CLASSIFICATION
# ============================================================

def classify_gpi_raster(gpi_raster):
    """
    Convert a continuous GPI raster into three
    prospectivity classes.

    Returns
    -------
    numpy.ndarray
        Integer classification:

            1 = Low Prospect
            2 = Moderate Prospect
            3 = High Prospect
    """

    gpi = np.asarray(
        gpi_raster,
        dtype=np.float64,
    )

    classes = np.zeros(
        gpi.shape,
        dtype=np.uint8,
    )

    classes[
        (gpi >= 0.0) &
        (gpi < 0.50)
    ] = 1

    classes[
        (gpi >= 0.50) &
        (gpi < 0.70)
    ] = 2

    classes[
        gpi >= 0.70
    ] = 3

    return classes
import numpy as np

def compute_gpi_score(weights):
    """
    Computes weighted composite GPI score using normalized FAHP weights.
    GPI = sum(w_i * S_i)
    """
    # Sample baseline evidence scores for criteria
    evidence_scores = np.array([0.85, 0.92, 0.95, 0.70, 0.78, 0.65, 0.60, 0.65])
    w = np.array(weights)
    
    # Normalize weights if sum != 1
    if np.sum(w) > 0:
        w = w / np.sum(w)
        
    gpi_val = float(np.sum(w * evidence_scores))
    
    if gpi_val >= 0.70:
        prospect_class = "High Prospect"
    elif gpi_val >= 0.50:
        prospect_class = "Moderate Prospect"
    else:
        prospect_class = "Low Prospect"
        
    return {
        "gpi_score": round(gpi_val, 2),
        "class": prospect_class
    }

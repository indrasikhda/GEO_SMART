import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import streamlit as st

LST_PATH = r"d:\SEMESTER 5\PROJEK\Bahan\LST_BARU.tif"
NDVI_PATH = r"d:\SEMESTER 5\PROJEK\Bahan\GEO_SMART_NDVI_2025.tif"

# ════════════════════════════════════════════════════════════
# DISTINCT HIGH-CONTRAST COLOR RAMPS
# ════════════════════════════════════════════════════════════

# NDVI: Brown/Yellow (Bare Soil/Low) ➔ Light Green ➔ Deep Lush Forest Green (High)
NDVI_COLORS = [
    (0.00, "#92400E"),   # Deep Amber/Brown (Low / Non-veg)
    (0.20, "#D97706"),   # Ochre / Bare Soil
    (0.40, "#FACC15"),   # Pale Yellow / Sparse Veg
    (0.60, "#4ADE80"),   # Bright Green / Moderate
    (0.80, "#16A34A"),   # Emerald Green / Healthy
    (1.00, "#064E3B"),   # Deep Forest Green / Dense Canopy
]
CMAP_NDVI = LinearSegmentedColormap.from_list("geosmart_ndvi", [(pos, col) for pos, col in NDVI_COLORS])

# LST: Cool Ocean Blue (Low) ➔ Cyan ➔ Yellow ➔ Warm Orange ➔ Hotspot Crimson/Ruby (High)
LST_COLORS = [
    (0.00, "#0369A1"),   # Deep Blue (Coolest)
    (0.20, "#0284C7"),   # Sky Blue
    (0.40, "#38BDF8"),   # Light Cyan
    (0.55, "#FEF08A"),   # Soft Yellow / Ambient
    (0.70, "#F59E0B"),   # Warm Orange
    (0.85, "#DC2626"),   # Crimson Red (Thermal Hotspot)
    (1.00, "#7F1D1D"),   # Deep Ruby (Maximum Thermal Anomaly)
]
CMAP_LST = LinearSegmentedColormap.from_list("geosmart_lst", [(pos, col) for pos, col in LST_COLORS])


@st.cache_data(show_spinner=False)
def get_raster_stats_and_overlay(layer_type="lst", out_dir=r"d:\SEMESTER 5\PROJEK\geo_smart_streamlit\static"):
    os.makedirs(out_dir, exist_ok=True)
    file_path = LST_PATH if layer_type == "lst" else NDVI_PATH

    if not os.path.exists(file_path):
        return {
            "error": f"File not found: {file_path}",
            "min": 0.0, "max": 0.0, "mean": 0.0,
            "bounds": [[0.27, 123.10], [5.56, 127.14]],
            "png_path": None
        }

    with rasterio.open(file_path) as src:
        bounds = src.bounds
        bounds_wgs84 = [[bounds.bottom, bounds.left], [bounds.top, bounds.right]]

        # Read downsampled data for fast interactive rendering (800x800)
        data = src.read(1, out_shape=(800, 800))

        if layer_type == "lst":
            valid_mask = (data > -20) & (data < 70) & (~np.isnan(data))
            cmap = CMAP_LST
        else:
            valid_mask = (data >= -1.0) & (data <= 1.0) & (~np.isnan(data))
            cmap = CMAP_NDVI

        valid_vals = data[valid_mask]
        min_v = float(np.min(valid_vals)) if len(valid_vals) > 0 else 0.0
        max_v = float(np.max(valid_vals)) if len(valid_vals) > 0 else 1.0
        mean_v = float(np.mean(valid_vals)) if len(valid_vals) > 0 else 0.5

        # Normalize raster to 0.0 - 1.0 range
        norm_data = np.zeros_like(data, dtype=np.float32)
        if max_v > min_v:
            norm_data[valid_mask] = np.clip((data[valid_mask] - min_v) / (max_v - min_v), 0, 1)

        rgba = cmap(norm_data)
        rgba[~valid_mask] = [0, 0, 0, 0]  # Fully transparent background for nodata

        png_filename = f"{layer_type}_overlay.png"
        png_path = os.path.join(out_dir, png_filename)
        plt.imsave(png_path, rgba)

        return {
            "min": round(min_v, 2),
            "max": round(max_v, 2),
            "mean": round(mean_v, 2),
            "bounds": bounds_wgs84,
            "png_path": png_path,
            "filename": os.path.basename(file_path),
            "valid_array": valid_vals
        }


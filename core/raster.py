import os
import base64
from pathlib import Path
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import streamlit as st

# ════════════════════════════════════════════════════════════
# PATH RELATIF & CROSS-PLATFORM (Bisa di lokal Windows & Cloud Linux)
# ════════════════════════════════════════════════════════════
BASE_DIR = Path(__file__).resolve().parent.parent

# Masukkan file GeoTIFF ke dalam folder 'data/' di root repository GitHub Anda
LST_PATH = BASE_DIR / "data" / "LST_BARU.tif"
NDVI_PATH = BASE_DIR / "data" / "GEO_SMART_NDVI_2025.tif"

# ════════════════════════════════════════════════════════════
# COLOR RAMPS
# ════════════════════════════════════════════════════════════
NDVI_COLORS = [
    (0.00, "#92400E"),   # Low / Non-veg
    (0.20, "#D97706"),   # Bare Soil
    (0.40, "#FACC15"),   # Pale Yellow
    (0.60, "#4ADE80"),   # Bright Green
    (0.80, "#16A34A"),   # Emerald Green
    (1.00, "#064E3B"),   # Deep Forest Green
]
CMAP_NDVI = LinearSegmentedColormap.from_list("geosmart_ndvi", [(pos, col) for pos, col in NDVI_COLORS])

LST_COLORS = [
    (0.00, "#0369A1"),   # Deep Blue
    (0.20, "#0284C7"),   # Sky Blue
    (0.40, "#38BDF8"),   # Light Cyan
    (0.55, "#FEF08A"),   # Soft Yellow
    (0.70, "#F59E0B"),   # Warm Orange
    (0.85, "#DC2626"),   # Crimson Red
    (1.00, "#7F1D1D"),   # Deep Ruby
]
CMAP_LST = LinearSegmentedColormap.from_list("geosmart_lst", [(pos, col) for pos, col in LST_COLORS])


@st.cache_data(show_spinner=False)
def get_raster_stats_and_overlay(layer_type="lst"):
    file_path = LST_PATH if layer_type == "lst" else NDVI_PATH

    if not file_path.exists():
        # Fallback jika file GeoTIFF belum ada / tidak ter-upload
        return {
            "error": f"File not found: {file_path}",
            "min": 0.0, "max": 0.0, "mean": 0.0,
            "bounds": [[1.0, 124.0], [1.7, 125.2]],
            "png_path": None,
            "filename": file_path.name,
            "valid_array": np.array([])
        }

    with rasterio.open(file_path) as src:
        bounds = src.bounds
        bounds_wgs84 = [[bounds.bottom, bounds.left], [bounds.top, bounds.right]]

        # Downsample raster 800x800 untuk rendering cepat
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

        # Normalisasi ke skala 0.0 - 1.0
        norm_data = np.zeros_like(data, dtype=np.float32)
        if max_v > min_v:
            norm_data[valid_mask] = np.clip((data[valid_mask] - min_v) / (max_v - min_v), 0, 1)

        rgba = cmap(norm_data)
        rgba[~valid_mask] = [0, 0, 0, 0]  # Transparan untuk NoData

        # Simpan sementara di memori dan ubah langsung ke Base64 Data URI
        import io
        buf = io.BytesIO()
        plt.imsave(buf, rgba, format="png")
        buf.seek(0)
        base64_png = base64.b64encode(buf.read()).decode("utf-8")
        data_uri = f"data:image/png;base64,{base64_png}"

        return {
            "min": round(min_v, 2),
            "max": round(max_v, 2),
            "mean": round(mean_v, 2),
            "bounds": bounds_wgs84,
            "png_path": data_uri,  # Mengembalikan Data URI yang siap dirender Folium ImageOverlay
            "filename": file_path.name,
            "valid_array": valid_vals
        }
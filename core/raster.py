import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt

LST_PATH = r"d:\SEMESTER 5\PROJEK\Bahan\LST_BARU.tif"
NDVI_PATH = r"d:\SEMESTER 5\PROJEK\Bahan\GEO_SMART_NDVI_2025.tif"

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
            cmap = plt.cm.inferno
        else:
            valid_mask = (data >= -1.0) & (data <= 1.0) & (~np.isnan(data))
            cmap = plt.cm.YlGn

        valid_vals = data[valid_mask]
        min_v = float(np.min(valid_vals)) if len(valid_vals) > 0 else 0.0
        max_v = float(np.max(valid_vals)) if len(valid_vals) > 0 else 1.0
        mean_v = float(np.mean(valid_vals)) if len(valid_vals) > 0 else 0.5

        # Normalize raster
        norm_data = np.zeros_like(data, dtype=np.float32)
        if max_v > min_v:
            norm_data[valid_mask] = np.clip((data[valid_mask] - min_v) / (max_v - min_v), 0, 1)

        rgba = cmap(norm_data)
        rgba[~valid_mask] = [0, 0, 0, 0]  # Transparent background

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

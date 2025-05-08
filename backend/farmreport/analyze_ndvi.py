import rasterio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

with rasterio.open("../farm_ndvi.tiff") as src:
    ndvi = src.read(1)

ndvi = np.clip(ndvi, -1, 1)

poor_mask = ndvi < 0.2
moderate_mask = (ndvi >= 0.2) & (ndvi <= 0.5)
good_mask = ndvi > 0.5

ndvi_classified = np.zeros((ndvi.shape[0], ndvi.shape[1], 3), dtype=np.uint8)
ndvi_classified[poor_mask] = [255, 0, 0]       
ndvi_classified[moderate_mask] = [255, 255, 0] 
ndvi_classified[good_mask] = [0, 255, 0]       

plt.figure(figsize=(8, 6))
plt.imshow(ndvi_classified)
plt.title("NDVI Classified Plot Health Status")
plt.axis('off')


total_pixels = ndvi.size
poor_pct = round((np.sum(poor_mask) / total_pixels) * 100, 2)
moderate_pct = round((np.sum(moderate_mask) / total_pixels) * 100, 2)
good_pct = round((np.sum(good_mask) / total_pixels) * 100, 2)

red_patch = mpatches.Patch(color='red', label=f'Poor (< 0.2): {poor_pct}%')
yellow_patch = mpatches.Patch(color='yellow', label=f'Moderate (0.2–0.5): {moderate_pct}%')
green_patch = mpatches.Patch(color='green', label=f'Good (> 0.5): {good_pct}%')

plt.legend(handles=[red_patch, yellow_patch, green_patch], loc='lower right')

plt.tight_layout()



print("\n NDVI Plot Health Classification Report:")
print(f"🟥 Poor (< 0.2):       {poor_pct}%")
print(f"🟨 Moderate (0.2–0.5): {moderate_pct}%")
print(f"🟩 Good (> 0.5):        {good_pct}%")


plt.show()

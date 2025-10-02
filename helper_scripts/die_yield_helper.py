import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

def die_yield_centered_reticle(die_w, die_h, kerf, reticle_cols, reticle_rows, plot=False, heatmap=False):
    """
    Compute usable die yield on a wafer with tiling starting from central 4 reticle shots.
    
    Parameters:
        die_w, die_h: die dimensions in mm
        kerf: saw kerf in mm
        reticle_cols, reticle_rows: dies per reticle
        plot: plot wafer + dies + reticle locations
        heatmap: plot reticle yield heatmap
    
    Returns:
        total dies, die centers, reticle yield counts
    """
    
    wafer_size = 200  # wafer size in mm
    wafer_r = wafer_size / 2.0
    hx, hy = die_w / 2.0, die_h / 2.0
    px = die_w + kerf
    py = die_h + kerf

    # Reticle dimensions
    ret_w = reticle_cols * px - kerf
    ret_h = reticle_rows * py - kerf

    # Determine number of reticles to tile in each direction
    n_rx = int(math.ceil((wafer_r + ret_w/2) / ret_w))
    n_ry = int(math.ceil((wafer_r + ret_h/2) / ret_h))

    # Compute reticle origin positions (tile from center)
    origins = []
    for ix in range(-n_rx, n_rx):
        for iy in range(-n_ry, n_ry):
            ox = ix * ret_w
            oy = iy * ret_h
            origins.append((ox, oy))

    centers = []
    counts = np.zeros((reticle_rows, reticle_cols), dtype=int)
    total = 0

    # Scan dies within each reticle
    for ox, oy in origins:
        for c in range(reticle_cols):
            for r in range(reticle_rows):
                cx = ox + c * px + hx
                cy = oy + r * py + hy
                corners = [(cx - hx, cy - hy), (cx + hx, cy - hy),
                           (cx + hx, cy + hy), (cx - hx, cy + hy)]
                inside = all(x*x + y*y <= wafer_r**2 for x, y in corners)
                if inside:
                    centers.append((cx, cy))
                    total += 1
                    # determine die position within reticle
                    counts[r, c] += 1

    # Plot wafer + dies + reticles
    if plot:
        fig, ax = plt.subplots(figsize=(8,8))
        wafer = Circle((0,0), wafer_r, edgecolor='black', facecolor='none', lw=2)
        ax.add_patch(wafer)

        for cx, cy in centers:
            rect = Rectangle((cx-hx, cy-hy), die_w, die_h, edgecolor='green', facecolor='none', lw=0.5)
            ax.add_patch(rect)

        for ox, oy in origins:
            rect = Rectangle((ox, oy), ret_w, ret_h, edgecolor='blue', facecolor='none', lw=1, linestyle='--')
            ax.add_patch(rect)

        ax.set_aspect('equal')
        ax.set_xlim(-wafer_r-5, wafer_r+5)
        ax.set_ylim(-wafer_r-5, wafer_r+5)
        ax.set_title(f"200mm Wafer Map: {total} full dies (green) + reticles (blue dashed)")
        plt.show()

    # Reticle yield heatmap
    if heatmap:
        fig, ax = plt.subplots(figsize=(6,5))
        im = ax.imshow(counts, cmap="viridis", origin="lower")
        for r in range(counts.shape[0]):
            for c in range(counts.shape[1]):
                ax.text(c, r, str(counts[r,c]), ha="center", va="center", color='white', fontsize=8)
        ax.set_title("Reticle Position Yield (usable dies)")
        ax.set_xlabel("Column index")
        ax.set_ylabel("Row index")
        fig.colorbar(im, ax=ax, label="Usable dies")
        plt.show()

    return total, centers, counts

if __name__ == "__main__":
    total, centers, counts = die_yield_centered_reticle(
        3.88, 5.08, 0.035, reticle_cols=8, reticle_rows=5, plot=True, heatmap=True
    )
    print(f"Total usable dies: {total}")
    print("Reticle-position yield table (rows 0=bottom..N-1=top):")
    print(counts)

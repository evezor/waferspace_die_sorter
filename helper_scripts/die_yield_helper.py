import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from typing import List, Tuple

# --- New Die Slicing Scheme ---
# Units are in mm. columns correspond to die widths, rows to die heights.
DIE_WIDTHS: List[float] = [1, 3.88, 3.88, 3.88, 3.88, 3.88, 3.88, 3.88, 1.94, 1]
DIE_HEIGHTS: List[float] = list(reversed([1, 2.535, 5.070, 5.070, 5.070, 5.070, 1]))
KERF: float = 0.035 # Saw kerf in mm
WAFER_SIZE: float = 200 # Wafer size in mm
EXLUSION_ZONE: float = 3.0 # Exclusion zone from wafer edge in mm

def die_yield_centered_reticle_flexible(
    die_widths: List[float],
    die_heights: List[float],
    kerf: float,
    wafer_size: float = 200,
    exclusion_zone: float = 3.0,
    plot: bool = False,
    heatmap: bool = False
) -> Tuple[int, List[Tuple[float, float]], np.ndarray]:
    """
    Compute usable die yield on a wafer with tiling starting from central 4 reticle shots.
    This version supports dies of different widths (columns) and heights (rows) within the reticle.
    
    Parameters:
        die_widths: List of die widths (column-wise) in mm.
        die_heights: List of die heights (row-wise) in mm.
        kerf: Saw kerf in mm.
        wafer_size: Wafer diameter in mm.
        plot: Plot wafer + dies + reticle locations.
        heatmap: Plot reticle yield heatmap.
    
    Returns:
        total_dies: Total number of full dies found on the wafer.
        die_centers: List of (x, y) center coordinates for the usable dies.
        reticle_yield_counts: 2D numpy array of yield counts for each die position within the reticle.
    """
    
    wafer_r: float = (wafer_size / 2.0) - exclusion_zone # Effective wafer radius after exclusion zone
    reticle_cols: int = len(die_widths)
    reticle_rows: int = len(die_heights)

    # Calculate horizontal and vertical pitch lists (die_dim + kerf)
    px_list: List[float] = [dw + kerf for dw in die_widths]
    py_list: List[float] = [dh + kerf for dh in die_heights]
    
    # Reticle dimensions are the sum of all pitches, minus one kerf
    ret_w: float = sum(px_list) - kerf
    ret_h: float = sum(py_list) - kerf

    # Determine number of reticles to tile in each direction
    # This logic assumes the reticle centers tile from (0,0) and tries to cover the wafer.
    n_rx: int = int(math.ceil((wafer_r + ret_w/2) / ret_w))
    n_ry: int = int(math.ceil((wafer_r + ret_h/2) / ret_h))

    # Compute reticle origin positions (tile from center)
    origins: List[Tuple[float, float]] = []
    for ix in range(-n_rx, n_rx):
        for iy in range(-n_ry, n_ry):
            ox: float = ix * ret_w
            oy: float = iy * ret_h
            origins.append((ox, oy))

    centers: List[Tuple[float, float]] = []
    reticle_yield_counts: np.ndarray = np.zeros((reticle_rows, reticle_cols), dtype=int)
    total_dies: int = 0

    # Scan dies within each reticle
    for ox, oy in origins:
        for c in range(reticle_cols):
            # The accumulated distance up to the start of column c
            # This is the sum of pitches for all columns *before* c.
            # Start position in X relative to reticle origin
            x_start_rel: float = sum(px_list[:c])
            die_w: float = die_widths[c]
            hx: float = die_w / 2.0
            
            for r in range(reticle_rows):
                # The accumulated distance up to the start of row r
                # This is the sum of pitches for all rows *before* r.
                # Start position in Y relative to reticle origin
                y_start_rel: float = sum(py_list[:r])
                die_h: float = die_heights[r]
                hy: float = die_h / 2.0

                # Center of the die
                # Die center = Reticle Origin + Relative Start + Half Die Dimension
                cx: float = ox + x_start_rel + hx
                cy: float = oy + y_start_rel + hy
                
                # Check the four corners for being inside the wafer
                corners: List[Tuple[float, float]] = [
                    (cx - hx, cy - hy), (cx + hx, cy - hy),
                    (cx + hx, cy + hy), (cx - hx, cy + hy)
                ]
                
                # A die is usable if *all* four corners are within the wafer radius
                inside: bool = all(x*x + y*y <= wafer_r**2 for x, y in corners)
                
                if inside:
                    centers.append((cx, cy))
                    total_dies += 1
                    # determine die position within reticle (r, c)
                    reticle_yield_counts[r, c] += 1

    # Plot wafer + dies + reticles
    if plot:
        fig, ax = plt.subplots(figsize=(8,8))
        wafer = Circle((0,0), wafer_size / 2.0, edgecolor='black', facecolor='none', lw=2)
        ax.add_patch(wafer)

        # Plot all usable dies
        # We need to iterate over the centers and re-calculate the die dimensions
        # to ensure the correct rectangle is drawn.
        for ox, oy in origins:
            for c in range(reticle_cols):
                x_start_rel: float = sum(px_list[:c])
                die_w: float = die_widths[c]
                
                for r in range(reticle_rows):
                    y_start_rel: float = sum(py_list[:r])
                    die_h: float = die_heights[r]

                    # Lower-left corner of the die
                    llx: float = ox + x_start_rel
                    lly: float = oy + y_start_rel
                    
                    if reticle_yield_counts[r, c] > 0:
                        # Re-check the die is inside for this specific reticle shot
                        # This is necessary because `reticle_yield_counts` accumulates across all shots,
                        # but we only want to plot the dies that were marked as usable.
                        # Since the check is already done above, we can simplify this block:
                        
                        # Find the center for this die in this specific reticle
                        cx = llx + die_w / 2.0
                        cy = lly + die_h / 2.0
                        
                        if (cx, cy) in centers: # Simple check to see if it was a counted die
                            rect = Rectangle(
                                (llx, lly), die_w, die_h, 
                                edgecolor='green', facecolor='none', lw=0.5
                            )
                            ax.add_patch(rect)
                        
            # Plot reticle boundaries (blue dashed)
            rect = Rectangle((ox, oy), ret_w, ret_h, edgecolor='blue', facecolor='none', lw=1, linestyle='--')
            ax.add_patch(rect)

        ax.set_aspect('equal')
        ax.set_xlim(-wafer_r-5, wafer_r+5)
        ax.set_ylim(-wafer_r-5, wafer_r+5)
        ax.set_title(f"{wafer_size}mm Wafer Map: {total_dies} full dies (green) + reticles (blue dashed)")
        plt.savefig('wafer_map.png', dpi=150, bbox_inches='tight')
        plt.show()
        

        # x_start_rel: float = sum(px_list[:c])
        # die_w: float = die_widths[c]
        
        # for r in range(reticle_rows):
        #     y_start_rel: float = sum(py_list[:r])
        #     die_h: float = die_heights[r]

        #     # Lower-left corner of the die
        #     llx: float = ox + x_start_rel
        #     lly: float = oy + y_start_rel
            
        #     if reticle_yield_counts[r, c] > 0:
        #         # Re-check the die is inside for this specific reticle shot
        #         # This is necessary because `reticle_yield_counts` accumulates across all shots,
        #         # but we only want to plot the dies that were marked as usable.
        #         # Since the check is already done above, we can simplify this block:
                
        #         # Find the center for this die in this specific reticle
        #         cx = llx + die_w / 2.0
        #         cy = lly + die_h / 2.0
                
        #         if (cx, cy) in centers: # Simple check to see if it was a counted die
        #             rect = Rectangle(
        #                 (llx, lly), die_w, die_h, 
        #                 edgecolor='green', facecolor='none', lw=0.5
        #             )
        #             ax.add_patch(rect)
                        
        #     # Plot reticle boundaries (blue dashed)
        #     rect = Rectangle((ox, oy), ret_w, ret_h, edgecolor='blue', facecolor='none', lw=1, linestyle='--')
        #     ax.add_patch(rect)

        # ax.set_aspect('equal')
        # ax.set_xlim(-wafer_r-5, wafer_r+5)
        # ax.set_ylim(-wafer_r-5, wafer_r+5)
        # ax.set_title(f"{wafer_size}mm Wafer Map: {total_dies} full dies (green) + reticles (blue dashed)")
        # plt.show()
        


    # Reticle yield heatmap
    if heatmap:
        fig, ax = plt.subplots(figsize=(6,5))
        im = ax.imshow(reticle_yield_counts, cmap="viridis", origin="lower")
        for r in range(reticle_yield_counts.shape[0]):
            for c in range(reticle_yield_counts.shape[1]):
                ax.text(c, r, str(reticle_yield_counts[r,c]), ha="center", va="center", color='white', fontsize=8)
        ax.set_title("Reticle Position Yield (usable dies)")
        ax.set_xlabel("Column index")
        ax.set_ylabel("Row index")
        fig.colorbar(im, ax=ax, label="Usable dies")
        plt.show()
        

    return total_dies, centers, reticle_yield_counts

if __name__ == "__main__":
    # Use the new lists defined at the top
    total, centers, counts = die_yield_centered_reticle_flexible(
        DIE_WIDTHS, DIE_HEIGHTS, KERF, WAFER_SIZE, EXLUSION_ZONE, plot=True, heatmap=True
    )
    print(f"Total usable dies: {total}")
    print("Reticle-position yield table (rows 0=bottom..N-1=top):")
    print(counts)
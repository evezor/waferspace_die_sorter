# die_yield_helper.py

A utility script for analyzing and processing wafer die yield data.

## Overview

`die_yield_helper.py` provides functions to calculate yield metrics and generate pick maps for wafer die sorting operations. 

## Example Output

```
Total usable dies: 1951,
Die count array shape: (6, 9),
[[33 35 36 37 37 36 35 35 34]
 [36 36 37 37 37 37 36 36 37]
 [38 36 36 36 36 36 36 38 40]
 [36 36 37 37 37 37 36 36 37]
 [34 35 36 37 37 36 35 35 36]
 [33 36 36 38 38 36 36 35 34]]
```

csv export:
```csv
X ,Y ,RETICLE_SHOT, COL|ROW
-94.276,-12.092,S-4_-1,C8R2
-94.276,-6.998,S-4_-1,C8R3
-94.276,-3.171,S-4_-1,C8R4
-94.276,-0.94,S-4_-1,C8R5
-94.276,2.535,S-4_0,C8R0
-94.276,7.629,S-4_0,C8R1
-94.276,12.723,S-4_0,C8R2
```

![](waferspace_run1_test.svg)
![](waferspace_run1_test_heatmap.svg)

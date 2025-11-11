# jitcdde_Wrapper

A **wrapper** for [`jitcdde`](https://github.com/neurophysics/jitcdde) that enables **output of intermediate helper variables** alongside the main state.

The wrapper replaces the default C code template with a custom one, allowing access to helper expressions during integration.

---

## Files

- **`custom_template.c`**  
  Dynamic C template for optimized code generation (replaces the original `jitcdde` template).

- **`customjitcdde.py`**  
  Python wrapper exposing a `customjitcdde` class with enhanced functionality.

---

## Usage

```python
from CustomJiTCDDE import customjitcdde
from jitcdde import y, t
import numpy as np

# Define your equations and helper symbols
equations = [...]  # your DDE system
helpers  = [...]   # symbolic helper expressions

# Initialize the custom DDE
DDE = customjitcdde(equations, helpers=helpers)

# Configure as with regular jitcdde (anchors, constants, etc.)
# ...

# Integration (point-by-point)
timepoints = np.linspace(0, 10, 1000)

for i, t in enumerate(timepoints):
    state, helper_values = DDE.integrate(t)
    
    # state: main system state (numpy array)
    # helper_values: values of helper variables (numpy array)

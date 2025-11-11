# jitcdde_Wrapper
A wrapper to be able to run jitcdde, while also outputting the intermediate helper variable values.
---------------------------------------------------------------------------------------------------

The .c file contains the dynamic template for the c-optimized code that substitutes the original template. The .py file contains the wrapper
that enables users to call jitcdde with the new template.

The wrapper can be used as following:

DDE = customjitcdde(equations, helpers = helpers)

The DDE object can then be modified similarly to jitcdde.

Results can be accessed by:

for itimepoint, timepoint in enumerate(timepoints):
    state, helpers = DDE.integrate(timepoint)

where state and helpers are numpy arrays. 

!!!For now the wrapper only handles the non-lambdified version, and timepoint by timepoint integration as illustrated!!!

from inspect import stack
from jinja2 import Environment, FileSystemLoader
from jitcdde import jitcdde
from os import path
from pathlib import Path
from warnings import warn


class customjitcdde(jitcdde):
    """
    A wrapper around JiTCDDE that:
    - Uses a custom C template from file
    - Provides a safer/custom integrate() method
    """
    def __init__(self, *args, helpers = None, **kwargs):
        # Load the template as string
        self.template_source = self._load_template_source()
        # Number of helpers
        if helpers == None:
            self.Nhelpers = 0
        else:
            self.Nhelpers = len(helpers)
        # Initialize parent
        super().__init__(*args, helpers = helpers, **kwargs)

    @property
    def helperNames(self):
        """Goal:
            Return the names of the newly ordered helper functions.
        -------------------------------------------------------------"""
        names = [str(helper[0]) for helper in self.helpers]
        return names[:self.Nhelpers]
    
    def _load_template_source(self):
        """Goal:
            Load the custom template as string.
        --------------------------------------------------------------------"""
        parent_dir = Path(__file__).resolve().parent
        custom_template_path = path.join(parent_dir, "jitced_adapted_template.c")
        if not path.exists(custom_template_path):
            raise FileNotFoundError(
                f"Custom template not found: {custom_template_path}"
                )
        with open(custom_template_path, "r", encoding="utf-8") as f:
            return f.read()
        
    def _render_template(self,**kwargs):
        """
        use Jinja2 to render a template for the module
        """
        kwargs["module_name"] = self._modulename
        folder = path.dirname( stack()[1][1] )
        env = Environment(loader=FileSystemLoader(folder))

        # Create a template from the string
        template = env.from_string(self.template_source)
        # Write
        with open(self.sourcefile, "w") as codefile:
            codefile.write(template.render(kwargs))
        return template
    
    def integrate(self, target_time):
        """
        Tries to evolve the dynamics.
        
        Parameters
        ----------
        
        target_time : float
            time until which the dynamics is evolved
        
        Returns
        -------
        state : NumPy array
            the computed state of the system at `target_time`.
        """
        self._initiate()
        
        if self.DDE.get_t() > target_time:
            warn("The target time is smaller than the current time. No integration step will happen. The returned state will be extrapolated from the interpolating Hermite polynomial for the last integration step. You may see this because you try to integrate backwards in time, in which case you did something wrong. You may see this just because your sampling step is small, in which case there is no need to worry (though you should think about increasing your sampling time).", stacklevel=2)
        
        if not self.initial_discontinuities_handled:
            warn("You did not explicitly handle initial discontinuities. Proceed only if you know what you are doing. This is only fine if you somehow chose your initial past such that the derivative of the last anchor complies with the DDE. In this case, you can set the attribute `initial_discontinuities_handled` to `True` to suppress this warning. See https://jitcdde.rtfd.io/#discontinuities for details.", stacklevel=2)
        
        while self.DDE.get_t() < target_time:
            if self.try_single_step(self.dt):
                self.DDE.accept_step()
        
        result = self.DDE.get_recent_state(target_time)
        self.DDE.forget(self.max_delay)

        return result, self.DDE.get_helpers()[:self.Nhelpers]
    

    
    
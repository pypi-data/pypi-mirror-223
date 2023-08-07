
__version__ = "0.0.1"


from seisfwi.plot import Plot
from seisfwi.problem import ElasticProblem
from seisfwi.propagator import ElasticPropagator, AnalyticalPropagator, source_ricker
from seisfwi.solver import Solver
from seisfwi.workflow import forward, inversion, timelapse

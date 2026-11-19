"""Euler-Bernoulli cantilever beam benchmark and mesh convergence."""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Beam:
    length: float = 1.0
    width: float = 0.02
    height: float = 0.04
    young_modulus: float = 210e9
    end_load: float = 1000.0

    def __post_init__(self):
        if min(self.length, self.width, self.height, self.young_modulus) <= 0:
            raise ValueError('Geometry and Young modulus must be positive')

    @property
    def inertia(self) -> float:
        return self.width * self.height**3 / 12

    def exact_tip_deflection(self) -> float:
        return self.end_load * self.length**3 / (3 * self.young_modulus * self.inertia)


def solve_tip_deflection(beam: Beam, elements: int) -> float:
    """Approximate the tip deflection by numerical quadrature.

    Integrate curvature y''(x)=M(x)/(EI) with a composite trapezoidal
    approximation of y(L)=integral_0^L (L-x)*M(x)/(EI) dx.
    This is a discretized beam benchmark, NOT a 3D finite-element solver.
    """
    if elements < 1:
        raise ValueError('elements must be >= 1')
    dx = beam.length / elements
    def integrand(x):
        moment = beam.end_load * (beam.length - x)
        return (beam.length - x) * moment / (beam.young_modulus * beam.inertia)
    total = (integrand(0.0) + integrand(beam.length)) / 2
    total += sum(integrand(i * dx) for i in range(1, elements))
    return total * dx


def convergence_study(beam: Beam, sizes=(4, 8, 16, 32, 64)):
    exact = beam.exact_tip_deflection()
    rows = []
    for n in sizes:
        numerical = solve_tip_deflection(beam, n)
        rows.append({'elements': n, 'tip_deflection_m': numerical,
                     'relative_error': abs(numerical-exact)/abs(exact) if exact else 0.0})
    return {'analytical_tip_deflection_m': exact, 'results': rows}

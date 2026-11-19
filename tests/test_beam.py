import unittest
from atlas.beam import Beam, solve_tip_deflection, convergence_study

class BeamTests(unittest.TestCase):
    def test_exact_solution(self):
        beam = Beam()
        expected = 1000 * 1**3 / (3 * 210e9 * (0.02 * 0.04**3 / 12))
        self.assertAlmostEqual(beam.exact_tip_deflection(), expected)

    def test_convergence(self):
        study = convergence_study(Beam())
        errors = [r['relative_error'] for r in study['results']]
        self.assertTrue(all(a > b for a, b in zip(errors, errors[1:])))
        self.assertLess(errors[-1], 0.001)

    def test_invalid_mesh(self):
        with self.assertRaises(ValueError):
            solve_tip_deflection(Beam(), 0)

    def test_invalid_geometry(self):
        with self.assertRaises(ValueError):
            Beam(height=0)

    def test_load_linearity(self):
        a = solve_tip_deflection(Beam(end_load=100), 16)
        b = solve_tip_deflection(Beam(end_load=200), 16)
        self.assertAlmostEqual(b, 2*a)

if __name__ == '__main__':
    unittest.main()

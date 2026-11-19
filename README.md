# Project ATLAS

**Autonomous Tools for Lightweight Analysis and Simulation**

ATLAS is an early-stage, open-source computational engineering project aiming to connect parametric CAD, meshing, numerical solvers, and reproducible verification workflows. The current repository contains a **working 1D Euler–Bernoulli cantilever beam benchmark** and automated convergence tests. It does **not** yet implement 3D FEA, CadQuery, Gmsh, CalculiX, or AI orchestration.

## Working prototype

The current prototype models a prismatic cantilever beam under an end load. It computes the analytical tip displacement and approximates the beam's curvature integral on progressively refined grids, producing machine-readable error metrics. The numerical method is composite trapezoidal quadrature, **not finite element analysis**. This intentionally small benchmark provides an initial reproducible validation target for later solver integrations.

### Run

Requires Python 3.10+; no third-party packages.

```bash
python -m atlas.cli
python -m atlas.cli --load 500 --length 0.8 --output benchmark.json
python -m unittest discover -s tests -v
```

The CLI prints JSON containing the analytical displacement, numerical results, and relative errors for five grid resolutions. GitHub Actions runs the test suite on every push and pull request.

## Planned architecture

```text
atlas/
  beam.py          # implemented: analytical + numerical beam benchmark
  cli.py           # implemented: JSON benchmark CLI
  geometry/        # planned: CadQuery parametric geometry
  meshing/         # planned: Gmsh integration
  solvers/         # planned: CalculiX adapters
  verification/    # planned: mesh convergence and result validation
  optimization/    # planned: constrained design optimization
```

Future orchestration: FastAPI, asynchronous workers, isolated solver execution, and artifact provenance. These are **planned**, not implemented.

## Milestones

- [x] Analytical cantilever beam reference solution
- [x] Grid-refinement convergence benchmark
- [x] Automated tests and GitHub Actions workflow
- [ ] Parametric CAD prototype with CadQuery
- [ ] Gmsh mesh-generation adapter
- [ ] CalculiX finite-element benchmark with boundary-condition validation
- [ ] Mesh-convergence verification on non-singular quantities of interest
- [ ] Automated constrained structural optimization
- [ ] Devin Bots integration for implementation and maintenance

## Engineering reliability

Numerical results should be independently validated. Planned checks include dimensional consistency, equilibrium, boundary-condition verification, solver-log inspection, grid-convergence checks, and reproducible simulation artifacts. AI agents may write code but must not unilaterally declare a simulation physically valid.

## License

MIT. See LICENSE.

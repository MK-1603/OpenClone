# Blueprint 14: Research & Scientific Software

**Project Family:** `research_and_scientific_computing`  
**Primary Project Type:** `computational_model`  
**Maturity Status:** `SPECIFIED`  
**Complexity Level:** `MEDIUM` to `RESEARCH_EXPERIMENTAL`  
**Default Delivery Targets:** `linux`, `containers_cloud`

---

## 1. Goals & Scope
- Computational modeling, numerical simulations, bioinformatics data pipelines, differential equation solvers, and reproducible scientific workflows.
- Enforces strict numerical precision validation, deterministic random number generation, scientific dataset citation, and open-access reproducibility.

## 2. Classification Rules
- Matched when the software is developed for peer-reviewed scientific discovery, mathematical modeling, bioinformatics, or physical simulation.

## 3. Intake Questions & Required Information
1. Scientific domain: physics simulation, bioinformatics, geospatial GIS, or financial mathematics.
2. Numerical accuracy: single vs. double precision floating-point tolerances, convergence criteria.
3. Compute acceleration: CPU SIMD vectorization, OpenMP, MPI, or CUDA/OpenCL.
4. Data format: HDF5, NetCDF, CSV, Parquet, FASTA/FASTQ.

## 4. Domain & Capability Mapping
- **Mandatory Domains:** `01-SPECIFICATION`, `03-DATA-INTEGRITY`, `10-TESTING-AND-QA`, `14-PERFORMANCE-ENGINEERING`.
- **Mandatory Engines:** `E-001`, `E-003`, `E-010`, `E-014`.

## 5. Specialist Workforce
- `research-software-engineer`: Numerical algorithms, scientific libraries, and containerized reproducibility.
- `scientific-computing-specialist`: Parallelization, memory alignment, and precision checks.
- `statistician`: Uncertainty quantification and sensitivity analysis.

## 6. Verification & Delivery Artifacts
- Analytical ground-truth verification comparing numerical output to closed-form solutions.
- Docker environment file freezing BLAS/LAPACK and compiler versions.
- Data availability statement and parameter specification document.

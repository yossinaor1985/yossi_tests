 Here is Claude's plan:
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
 Quantum Computing Learning Repository - Implementation Plan
                                                                            
 Context                                                

 Build a comprehensive quantum computing learning repository covering
 optimization algorithms (with emphasis on QML), error correction, and
 error mitigation. Each topic gets physicist-level docs, kid-level docs,
 and Python implementations (both local-simulator and
 IBM-production-ready). All code uses Qiskit 2.4.1 (latest stable, April
 2026).

 Required Packages

 pip install qiskit==2.4.1 qiskit-aer qiskit-ibm-runtime qiskit-algorithms
 qiskit-optimization==0.7.0 qiskit-machine-learning==0.9.0 matplotlib numpy
  scipy pylatexenc

 ---
 SUBJECT 1: OPTIMIZATION ALGORITHMS (18 topics, simple → sophisticated)

 Part A: Core Quantum Optimization (8 topics)

 #: 1
 Algorithm: VQE (Variational Quantum Eigensolver)
 Difficulty: Beginner
 Folder Name: 01_VQE
 ────────────────────────────────────────
 #: 2
 Algorithm: QAOA (Quantum Approximate Optimization Algorithm)
 Difficulty: Beginner
 Folder Name: 02_QAOA
 ────────────────────────────────────────
 #: 3
 Algorithm: Grover Adaptive Search (GroverOptimizer)
 Difficulty: Intermediate
 Folder Name: 03_grover_adaptive_search
 ────────────────────────────────────────
 #: 4
 Algorithm: Warm-Start QAOA
 Difficulty: Intermediate
 Folder Name: 04_warm_start_qaoa
 ────────────────────────────────────────
 #: 5
 Algorithm: CVaR-VQE / CVaR-QAOA (Conditional Value at Risk)
 Difficulty: Intermediate
 Folder Name: 05_cvar_optimization
 ────────────────────────────────────────
 #: 6
 Algorithm: FALQON (Feedback-based ALgorithm for Quantum OptimizatioN)
 Difficulty: Advanced
 Folder Name: 06_FALQON
 ────────────────────────────────────────
 #: 7
 Algorithm: ADMM (Alternating Direction Method of Multipliers)
 Difficulty: Advanced
 Folder Name: 07_ADMM
 ────────────────────────────────────────
 #: 8
 Algorithm: Quantum Annealing (simulated on gate-based)
 Difficulty: Advanced
 Folder Name: 08_quantum_annealing_sim

 Part B: Quantum Machine Learning for Optimization (10 topics)

 ┌─────┬──────────────────────────┬──────────────┬──────────────────────┐
 │  #  │        Algorithm         │  Difficulty  │     Folder Name      │
 ├─────┼──────────────────────────┼──────────────┼──────────────────────┤
 │ 9   │ Parameterized Quantum    │ Beginner     │ 09_PQC_ansatz_design │
 │     │ Circuits & Ansatz Design │              │                      │
 ├─────┼──────────────────────────┼──────────────┼──────────────────────┤
 │ 10  │ Quantum Kernel Methods   │ Intermediate │ 10_quantum_kernels   │
 │     │ (FidelityQuantumKernel)  │              │                      │
 ├─────┼──────────────────────────┼──────────────┼──────────────────────┤
 │ 11  │ QSVC (Quantum Support    │ Intermediate │ 11_QSVC              │
 │     │ Vector Classifier)       │              │                      │
 ├─────┼──────────────────────────┼──────────────┼──────────────────────┤
 │ 12  │ VQC (Variational Quantum │ Intermediate │ 12_VQC               │
 │     │  Classifier)             │              │                      │
 ├─────┼──────────────────────────┼──────────────┼──────────────────────┤
 │     │ Quantum Neural Networks  │              │                      │
 │ 13  │ (EstimatorQNN,           │ Intermediate │ 13_QNN               │
 │     │ SamplerQNN)              │              │                      │
 ├─────┼──────────────────────────┼──────────────┼──────────────────────┤
 │ 14  │ VQR (Variational Quantum │ Advanced     │ 14_VQR               │
 │     │  Regressor)              │              │                      │
 ├─────┼──────────────────────────┼──────────────┼──────────────────────┤
 │ 15  │ Hybrid Quantum-Classical │ Advanced     │ 15_hybrid_torch_qnn  │
 │     │  NNs (TorchConnector)    │              │                      │
 ├─────┼──────────────────────────┼──────────────┼──────────────────────┤
 │ 16  │ Quantum Boltzmann        │ Expert       │ 16_quantum_boltzmann │
 │     │ Machines                 │              │                      │
 ├─────┼──────────────────────────┼──────────────┼──────────────────────┤
 │ 17  │ QGAN (Quantum Generative │ Expert       │ 17_QGAN              │
 │     │  Adversarial Networks)   │              │                      │
 ├─────┼──────────────────────────┼──────────────┼──────────────────────┤
 │ 18  │ Quantum Reservoir        │ Expert       │ 18_quantum_reservoir │
 │     │ Computing                │              │                      │
 └─────┴──────────────────────────┴──────────────┴──────────────────────┘

 ---
 SUBJECT 2: ERROR CORRECTION (11 topics, simple → sophisticated)

 ┌─────┬────────────────────────┬─────────────┬───────────────────────┐
 │  #  │      Code/Method       │ Difficulty  │      Folder Name      │
 ├─────┼────────────────────────┼─────────────┼───────────────────────┤
 │ 1   │ Bit-Flip Code          │ Beginner    │ 01_bit_flip_code      │
 │     │ (3-qubit)              │             │                       │
 ├─────┼────────────────────────┼─────────────┼───────────────────────┤
 │ 2   │ Phase-Flip Code        │ Beginner    │ 02_phase_flip_code    │
 │     │ (3-qubit)              │             │                       │
 ├─────┼────────────────────────┼─────────────┼───────────────────────┤
 │ 3   │ Bit-Phase Flip Code    │ Intermediat │ 03_shor_code          │
 │     │ (Shor 9-qubit)         │ e           │                       │
 ├─────┼────────────────────────┼─────────────┼───────────────────────┤
 │ 4   │ Steane Code (7-qubit)  │ Intermediat │ 04_steane_code        │
 │     │                        │ e           │                       │
 ├─────┼────────────────────────┼─────────────┼───────────────────────┤
 │ 5   │ CSS Codes (Calderbank- │ Intermediat │ 05_CSS_codes          │
 │     │ Shor-Steane)           │ e           │                       │
 ├─────┼────────────────────────┼─────────────┼───────────────────────┤
 │ 6   │ Stabilizer Formalism   │ Intermediat │ 06_stabilizer_formali │
 │     │                        │ e           │ sm                    │
 ├─────┼────────────────────────┼─────────────┼───────────────────────┤
 │ 7   │ Repetition Codes       │ Intermediat │ 07_repetition_codes   │
 │     │                        │ e           │                       │
 ├─────┼────────────────────────┼─────────────┼───────────────────────┤
 │ 8   │ Surface Codes          │ Advanced    │ 08_surface_codes      │
 ├─────┼────────────────────────┼─────────────┼───────────────────────┤
 │ 9   │ Color Codes            │ Advanced    │ 09_color_codes        │
 ├─────┼────────────────────────┼─────────────┼───────────────────────┤
 │ 10  │ Toric Codes            │ Advanced    │ 10_toric_codes        │
 ├─────┼────────────────────────┼─────────────┼───────────────────────┤
 │ 11  │ Bacon-Shor Code        │ Expert      │ 11_bacon_shor_code    │
 └─────┴────────────────────────┴─────────────┴───────────────────────┘

 ---
 SUBJECT 3: ERROR MITIGATION (8 topics, simple → sophisticated)

 ┌─────┬───────────────┬──────────────┬─────────────────────────────────┐
 │  #  │   Technique   │  Difficulty  │           Folder Name           │
 ├─────┼───────────────┼──────────────┼─────────────────────────────────┤
 │     │ Measurement   │              │                                 │
 │ 1   │ Error         │ Beginner     │ 01_measurement_error_mitigation │
 │     │ Mitigation    │              │                                 │
 │     │ (M3)          │              │                                 │
 ├─────┼───────────────┼──────────────┼─────────────────────────────────┤
 │     │ TREX (Twirled │              │                                 │
 │ 2   │  Readout      │ Beginner     │ 02_TREX                         │
 │     │ Error         │              │                                 │
 │     │ eXtinction)   │              │                                 │
 ├─────┼───────────────┼──────────────┼─────────────────────────────────┤
 │ 3   │ Dynamical     │ Intermediate │ 03_dynamical_decoupling         │
 │     │ Decoupling    │              │                                 │
 ├─────┼───────────────┼──────────────┼─────────────────────────────────┤
 │ 4   │ Pauli         │ Intermediate │ 04_pauli_twirling               │
 │     │ Twirling      │              │                                 │
 ├─────┼───────────────┼──────────────┼─────────────────────────────────┤
 │     │ Zero-Noise    │              │                                 │
 │ 5   │ Extrapolation │ Advanced     │ 05_ZNE                          │
 │     │  (ZNE)        │              │                                 │
 ├─────┼───────────────┼──────────────┼─────────────────────────────────┤
 │     │ Probabilistic │              │                                 │
 │ 6   │  Error        │ Advanced     │ 06_PEA                          │
 │     │ Amplification │              │                                 │
 │     │  (PEA)        │              │                                 │
 ├─────┼───────────────┼──────────────┼─────────────────────────────────┤
 │     │ Probabilistic │              │                                 │
 │ 7   │  Error        │ Expert       │ 07_PEC                          │
 │     │ Cancellation  │              │                                 │
 │     │ (PEC)         │              │                                 │
 ├─────┼───────────────┼──────────────┼─────────────────────────────────┤
 │     │ Clifford Data │              │                                 │
 │ 8   │  Regression   │ Expert       │ 08_CDR                          │
 │     │ (CDR)         │              │                                 │
 └─────┴───────────────┴──────────────┴─────────────────────────────────┘

 ---
 Directory Structure

 quantum/
 ├── progress_log.md                    # Updated after each subtask
 ├── algorithms/
 │   ├── 01_VQE/
 │   │   ├── explanation_physicist.md   # Deep math, derivations, examples
 │   │   ├── explanation_simple.md      # ELI5
 │   │   ├── vqe_local.py              # Local simulator code
 │   │   └── vqe_ibm_production.py     # IBM backend-ready code
 │   ├── 02_QAOA/
 │   │   ├── explanation_physicist.md
 │   │   ├── explanation_simple.md
 │   │   ├── qaoa_local.py
 │   │   └── qaoa_ibm_production.py
 │   └── ... (18 total)
 ├── error_correction/
 │   ├── 01_bit_flip_code/
 │   │   ├── explanation_physicist.md
 │   │   ├── explanation_simple.md
 │   │   ├── bit_flip_local.py
 │   │   └── bit_flip_ibm_production.py
 │   └── ... (11 total)
 └── mitigation/
     ├── 01_measurement_error_mitigation/
     │   ├── explanation_physicist.md
     │   ├── explanation_simple.md
     │   ├── m3_mitigation_local.py
     │   └── m3_mitigation_ibm_production.py
     └── ... (8 total)

 Per-Topic Deliverables (4 files each)

 1. explanation_physicist.md

 - Rigorous mathematical framework with full derivations
 - Hamiltonian formulations, operator algebra
 - Complexity analysis, convergence proofs where applicable
 - Circuit diagrams described in detail
 - Concrete worked examples with numbers
 - References to literature

 2. explanation_simple.md

 - ELI5 analogies and metaphors
 - No equations, pure intuition
 - Visual/story-based explanations

 3. *_local.py (Local Simulator)

 - Uses qiskit_aer AerSimulator
 - Fully executable locally with python script.py
 - Extensive inline comments referencing physicist.md concepts
 - Visualization of results (matplotlib)
 - Step-by-step print outputs explaining what's happening

 4. *_ibm_production.py (IBM Production-Ready)

 - Uses qiskit_ibm_runtime with QiskitRuntimeService
 - Proper session management, error handling
 - Transpilation for real backend topology
 - Production patterns: retry logic, result saving
 - NOT actually deployed (uses least_busy backend selection, commented
 instructions)

 Execution Order

 1. Algorithms (topics 1-18) - one at a time, log after each
 2. Error Correction (topics 1-11) - one at a time, log after each
 3. Error Mitigation (topics 1-8) - one at a time, log after each

 Total: 37 topics x 4 files = 148 files + progress log + folder structure

 Verification

 - Each Python file must be syntactically valid (check with python -c
 "import ast; ast.parse(open('file.py').read())")
 - Imports must reference correct Qiskit 2.4.1 module paths
 - Progress log updated after each completed topic
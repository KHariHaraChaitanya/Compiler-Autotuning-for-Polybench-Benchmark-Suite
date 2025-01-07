# Compiler-Autotuning-for-Polybench-Benchmark-Suite
Autotuning tool to optimize C programs for performance using OpenMP and PAPI (Performance API) counters

This project focuses on autotuning and optimizing the performance of the Correlation kernel from the Polybench benchmark suite. The goal is to apply loop transformations, parallelization (OpenMP), and SIMD vectorization to enhance performance and reduce execution time. Performance is measured using PAPI (Performance Application Programming Interface) counters to evaluate CPU cycles, cache misses, and vector operations.

The project was implemented as part of the CS 553: Algorithmic Language Compilers course, and experiments were conducted on an HP-Z440-XeonE5-1650v4 CPU system.

Key Features
Autotuning Script: Automates the compilation, execution, and performance profiling of Polybench kernels.
OpenMP Parallelization: Enables multi-threaded execution with dynamic thread count exploration.
PAPI Integration: Collects performance metrics (L1/L2 cache misses, stalled cycles, vector instructions) to identify bottlenecks and calculate metrics like IPC (Instructions Per Cycle).
Loop Transformations: Improves cache performance by applying loop interchange and fission.
Environment Control: Dynamically adjusts environment variables (e.g., OMP_NUM_THREADS) to explore performance under different parallel configurations.
Project Goals
Optimize Performance: Reduce execution time for large datasets by applying compiler optimizations and parallelization techniques.
Analyze Hardware Performance: Use PAPI counters to gain insights into cache behavior, CPU cycles, and instruction execution.
Scalable Tuning: Automate testing across different problem sizes and thread counts, enabling robust performance exploration.

Requirements:

Polybench 4.2.1
GCC (with OpenMP support)
PAPI (Performance API), PAPI compatible CPU (Eg. Intel XeonE5 CPU) 
Python 3.x
Linux 

Usage:

Clone the Repository:
git clone https://github.com/username/autotuning-polybench.git
cd autotuning-polybench

Set Up the Environment:
export OMP_NUM_THREADS=8

Compile and Execute:
python3 autotuning.py --explore-threads --command "./kernel"

Run with PAPI Profiling:
python3 autotuning.py --profile-papi --command "./kernel"

Generate Machine Info:
python3 autotuning.py --machine-info

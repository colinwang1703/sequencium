# Building the C++ Search Engine

This document explains how to build the C++ optimized search engine for Sequencium.

## Prerequisites

- Python 3.6 or later
- C++ compiler (g++ or clang++)
- pybind11 library

## Installation Steps

### 1. Install pybind11

```bash
pip install pybind11
```

### 2. Build the C++ Extension

```bash
python3 setup.py build_ext --inplace
```

This will:
- Compile `search_engine.cpp` with optimizations (`-O3 -march=native -ffast-math`)
- Create a shared library (`.so` file on Linux/macOS, `.pyd` on Windows)
- Place it in the current directory

### 3. Verify Installation

```bash
python3 -c "import search_engine; print('C++ engine loaded successfully!')"
```

### 4. Run Tests

```bash
# Run basic game tests
python3 test_sequencium.py

# Run C++ engine tests
python3 test_cpp_engine.py

# Run performance benchmark
python3 benchmark.py
```

## Troubleshooting

### Build Errors

If you get compiler errors:

1. Make sure you have a C++17-compatible compiler:
   ```bash
   g++ --version  # Should be 7.0 or later
   ```

2. **Portability note**: The default build uses `-march=native` which optimizes for your CPU but may not work on other machines. If you need to distribute the compiled library, edit `setup.py` and change:
   ```python
   extra_compile_args=['-std=c++17', '-O3', '-march=native', '-ffast-math'],
   ```
   to:
   ```python
   extra_compile_args=['-std=c++17', '-O3'],
   ```

3. Check pybind11 installation:
   ```bash
   python3 -c "import pybind11; print(pybind11.get_include())"
   ```

### Import Errors

If Python can't find the module:

1. Make sure the `.so` file is in the same directory as `sequencium.py`
2. Check the file permissions:
   ```bash
   ls -l *.so
   chmod +x *.so  # If needed
   ```

### Running Without C++

The code automatically falls back to pure Python if the C++ engine is not available. You can force Python-only mode:

```python
ai = SequenciumAI(max_depth=4, use_cpp=False)
```

## Performance Notes

The C++ implementation provides:
- **100-600x faster** execution
- **50-85% fewer nodes** evaluated (thanks to transposition table)
- Better scaling with deeper search depths

For best performance:
- Use depth 4-6 with the C++ engine
- Limit to depth 3-4 with Python-only mode

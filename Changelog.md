# Changelog

**Version:** v1.0.0  
**Release Date:** November 6, 2025

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-11-06

### 🎉 Initial Release

### ✅ Added
- **Main CLI Entry Point** (`main.py`)
  - Command-line interface for running all test scripts
  - Default behavior: runs all critical tests
  - Support for individual test commands
  - Comprehensive help system

- **Version Management**
  - `version.py` with version information and release date
  - Version labels added to all documentation files
  - Version comments added to key Python files

- **Documentation Structure**
  - `docs/` directory for all documentation files
  - `codes/README.md` with brief descriptions of each code file
  - `tools/README.md` for development tools documentation

- **Tools Directory**
  - `tools/` directory for development tools
  - Separated development tools from production code

### 🔄 Changed
- **Project Reorganization**
  - Reorganized root directory with cleaner structure
  - Moved all code files to `codes/` directory
  - Moved all documentation to `docs/` directory
  - Created `tools/` directory for development tools

- **File Consolidation**
  - Consolidated `test_performance_counters_qualcomm.py` and `qualcomm_performance_counters_test.py` into single comprehensive file
  - Combined functionality from both files into `qualcomm_performance_counters_test.py`

### 🗑️ Removed
- **Duplicate Files**
  - Removed `test_performance_counters_qualcomm.py` (consolidated into `qualcomm_performance_counters_test.py`)

- **Development Tools from Production Code**
  - Moved `gpu_monitor_working.py` from `codes/` to `tools/` directory

### 📝 Updated
- **Documentation**
  - Updated `README.md` with new file structure
  - Updated `codes/README.md` with consolidated file descriptions
  - Updated `main.py` descriptions for Qualcomm test
  - All documentation files now include version v1.0.0 and release date

### 🔧 Fixed
- **Code Organization**
  - Removed duplicate code
  - Better separation of concerns
  - Cleaner directory structure

### 📊 Statistics
- **Before:** 18 Python files in codes/, 1 duplicate, 1 development tool mixed in
- **After:** 16 Python files in codes/, 1 development tool in tools/, no duplicates

### 📁 Final Structure
```
amdperftest/
├── 📖 README.md                            # Main documentation
├── 🚀 main.py                              # CLI entry point
├── 📄 version.py                           # Version information
├── 📄 requirements.txt                     # Python dependencies
│
├── 📚 docs/                                # Documentation directory
│   ├── AMD_GPU_NPU_Monitoring_Guide.md
│   ├── Windows_Performance_Counters_vs_WMI_Guide.md
│   └── CPU_Performance_Analysis_Report.md
│
├── 🔧 tools/                                # Development tools
│   ├── README.md
│   └── gpu_monitor_working.py
│
└── 💻 codes/                                # Production code
    ├── README.md
    └── [16 Python files + 1 PowerShell + 1 HTML]
```

---

## Format

This changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.

### Categories
- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security improvements


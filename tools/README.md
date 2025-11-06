# Tools Directory

**Version:** v1.0.0  
**Release Date:** November 6, 2025

This directory contains development tools and utility scripts that are not part of the main production code.

## 🔧 Development Tools

### `gpu_monitor_working.py`
**Purpose:** Development tool for exploring GPU monitoring methods and generating production scripts  
**Description:** This script was used during development to:
- Test various GPU monitoring methods
- Explore working solutions
- Generate the production `amd_gpu_monitor.py` script

**Status:** Development tool - kept for reference  
**Note:** This script contains code that generates `codes/amd_gpu_monitor.py`. It's kept here for reference but is not part of the main production codebase.

**Usage:**
```bash
python tools/gpu_monitor_working.py
```

This will:
1. Test various GPU monitoring methods
2. Display working solutions
3. Generate `amd_gpu_monitor.py` in the current directory

## 📝 Notes

- These tools are for development and reference purposes
- They may not be maintained as actively as production code
- Use production scripts in `codes/` directory for actual monitoring tasks


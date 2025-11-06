# Code Files Overview

**Version:** v1.0.0  
**Release Date:** November 6, 2025

This directory contains all the code files for the AMD GPU & NPU Monitoring Toolkit. Below is a brief description of each file.

## 🎮 GPU Monitoring Scripts

### `amd_gpu_monitor.py`
**Purpose:** Practical GPU monitoring solution for AMD GPUs  
**Description:** Provides real-time GPU monitoring using Windows Performance Counters. Displays GPU engine utilization and memory usage with simple, clean output.  
**Usage:** `python amd_gpu_monitor.py`

### `enhanced_gpu_monitor.py`
**Purpose:** Advanced real-time GPU monitoring with continuous updates  
**Description:** Enhanced version with continuous monitoring, multiple GPU engine tracking, and detailed memory usage reporting. Includes interactive menu for different monitoring modes.  
**Usage:** `python enhanced_gpu_monitor.py`


### `gpu_monitoring_test.py`
**Purpose:** GPU monitoring testing and validation  
**Description:** Test script for validating GPU monitoring capabilities. Tests Windows Performance Counters, WMI, and other monitoring methods.  
**Usage:** `python gpu_monitoring_test.py`

## 🧪 Testing and Load Generation

### `comprehensive_gpu_test.py`
**Purpose:** Comprehensive GPU load testing and monitoring  
**Description:** Combines GPU load generation with real-time monitoring. Allows testing GPU utilization under various load conditions.  
**Usage:** `python comprehensive_gpu_test.py`

### `simple_gpu_test.py`
**Purpose:** Simple GPU load test  
**Description:** Basic GPU load generation using CPU-intensive and memory-intensive tasks. Useful for quick GPU utilization testing.  
**Usage:** `python simple_gpu_test.py`

### `gpu_load_generator.py`
**Purpose:** GPU workload generation tool  
**Description:** Advanced GPU load generator with multiple workload types, configurable intensity, and real-time monitoring integration.  
**Usage:** `python gpu_load_generator.py`

### `gpu_load.ps1`
**Purpose:** PowerShell GPU load generator  
**Description:** PowerShell script for generating GPU load using Windows Performance Counters. Can be run independently or integrated with Python scripts.  
**Usage:** `powershell -ExecutionPolicy Bypass -File gpu_load.ps1`

### `gpu_webgl_test.html`
**Purpose:** WebGL GPU test  
**Description:** HTML file with WebGL-based GPU stress test. Open in a web browser to generate GPU load for testing purposes.  
**Usage:** Open `gpu_webgl_test.html` in a web browser

## 🧠 NPU Monitoring

### `test_amd_npu_xrt_smi.py`
**Purpose:** AMD NPU monitoring via xrt-smi  
**Description:** Tests and monitors AMD Phoenix NPU using xrt-smi tool in WSL environment. Detects NPU devices and retrieves device information.  
**Usage:** `python test_amd_npu_xrt_smi.py` (requires WSL and xrt-smi)

## 🔍 Exploration and Analysis

### `test_wmi_gpu_cpu.py`
**Purpose:** WMI GPU/CPU information retrieval  
**Description:** Tests WMI capabilities for retrieving GPU and CPU hardware information. Displays device names, memory, drivers, and basic specifications.  
**Usage:** `python test_wmi_gpu_cpu.py`

### `wmi_gpu_detailed.py`
**Purpose:** Detailed WMI GPU exploration  
**Description:** Comprehensive WMI exploration script that retrieves detailed GPU information from multiple WMI classes. Includes error handling for missing data.  
**Usage:** `python wmi_gpu_detailed.py`

### `wmi_gpu_explorer.py`
**Purpose:** WMI class exploration tool  
**Description:** Interactive tool for exploring WMI classes related to GPU and system hardware. Useful for discovering available WMI properties and methods.  
**Usage:** `python wmi_gpu_explorer.py`

### `psutil_gpu_test.py`
**Purpose:** psutil GPU data test  
**Description:** Tests what GPU information is available through the psutil library. Explores psutil's capabilities for GPU monitoring on Windows.  
**Usage:** `python psutil_gpu_test.py`

## 💻 CPU and Platform-Specific Tests

### `cpu_performance_efficiency_test.py`
**Purpose:** CPU performance and efficiency testing  
**Description:** Comprehensive CPU monitoring test comparing Windows Performance Counters vs WMI. Measures response times, accuracy, and data quality for CPU utilization.  
**Usage:** `python cpu_performance_efficiency_test.py`

### `cpu_monitoring_comparison.py`
**Purpose:** CPU monitoring comparison tool  
**Description:** Compares different methods for CPU utilization monitoring (Performance Counters, WMI, psutil). Useful for understanding method differences.  
**Usage:** `python cpu_monitoring_comparison.py`

### `qualcomm_performance_counters_test.py`
**Purpose:** Comprehensive Qualcomm platform performance counters test  
**Description:** Complete test for Windows Performance Counters on Qualcomm Snapdragon and Adreno GPUs. Includes platform detection, CPU/GPU counters, WMI data, Qualcomm-specific counters, and continuous monitoring. This is the consolidated version combining functionality from previous separate test files.  
**Usage:** `python qualcomm_performance_counters_test.py`

## 📝 Notes

- All Python scripts require Python 3.7 or higher
- Windows scripts require Windows 10/11
- NPU monitoring scripts require WSL2 with AMD XRT tools installed
- Some scripts require additional dependencies (see `requirements.txt` in root directory)
- PowerShell scripts may require execution policy changes: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## 🔧 Dependencies

Core dependencies (see `requirements.txt`):
- `wmi>=1.5.1` - Windows Management Instrumentation
- `psutil>=5.8.0` - System and process utilities

Optional dependencies:
- `numpy>=1.21.0` - For advanced calculations
- `matplotlib>=3.5.0` - For data visualization


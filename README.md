# AMD GPU & NPU Monitoring Toolkit

## 🎯 Project Overview

This comprehensive toolkit provides working solutions for monitoring AMD GPUs in Windows and AMD NPUs in WSL environments. Based on extensive testing and research, we've identified and implemented the most effective methods for real-time GPU utilization and performance monitoring on AMD platforms.

## 📋 Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Environment Requirements](#environment-requirements)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [File Structure](#file-structure)
- [Key Findings](#key-findings)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## ✨ Features

### **🎮 GPU Monitoring (Windows)**
- ✅ **Real-time GPU utilization** - 3D, Copy, Compute engines
- ✅ **GPU memory usage** - Dedicated and shared memory tracking
- ✅ **Process-level monitoring** - Per-application GPU usage
- ✅ **High-frequency sampling** - Configurable update intervals
- ✅ **Multiple GPU support** - Works with RX 7600M XT, 780M, and other AMD GPUs

### **🧠 NPU Monitoring (WSL)**
- ✅ **AMD Phoenix NPU detection** via xrt-smi
- ✅ **Device information** and status monitoring
- ✅ **Workload tracking** and performance metrics
- ✅ **Cross-platform support** - Windows + WSL environments

### **📊 Monitoring Capabilities**
- **Real-time data** with high precision
- **Low overhead** monitoring
- **Programmatic access** via Python and PowerShell
- **Comprehensive documentation** and code examples
- **Load generation tools** for testing utilization

## 🚀 Quick Start

### **1. Basic GPU Monitoring**
```bash
# Run the enhanced GPU monitor
python enhanced_gpu_monitor.py

# Or use the simple monitor
python amd_gpu_monitor.py
```

### **2. GPU Load Testing**
```bash
# Generate GPU load and monitor simultaneously
python comprehensive_gpu_test.py

# Or run a simple load test
python simple_gpu_test.py
```

### **3. NPU Monitoring (WSL)**
```bash
# Monitor AMD Phoenix NPU
python test_amd_npu_xrt_smi.py

# Or use xrt-smi directly
xrt-smi --list
xrt-smi --info
```

## 🔧 Environment Requirements

### **Windows Requirements**
- **Operating System**: Windows 10/11
- **Python**: 3.7 or higher
- **AMD GPU**: Any AMD GPU with recent drivers
- **AMD Software**: Already installed (for temperature monitoring)

### **Python Dependencies**
```bash
# Install all dependencies from requirements.txt
pip install -r requirements.txt

# Core dependencies included:
# - wmi>=1.5.1 (Windows Management Instrumentation)
# - psutil>=5.8.0 (System and process utilities)

# Optional dependencies (uncomment in requirements.txt if needed):
# - numpy>=1.21.0 (For advanced calculations)
# - matplotlib>=3.5.0 (For plotting and visualization)
```

### **WSL Requirements (for NPU monitoring)**
- **WSL2**: Ubuntu/Debian Linux
- **AMD XRT Tools**: xrt-smi for NPU monitoring
- **Linux Tools**: lshw, hwinfo, lm-sensors

### **System Requirements**
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 100MB for scripts and documentation
- **Permissions**: Standard user permissions (no admin required)

## 📦 Installation

### **1. Clone or Download**
```bash
# If using git
git clone <repository-url>
cd amdperftest

# Or download and extract the files
```

### **2. Install Python Dependencies**
```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/WSL

# Install dependencies from requirements.txt
pip install -r requirements.txt
```

### **3. Verify Installation**
```bash
# Test basic functionality
python test_wmi_gpu_cpu.py

# Test GPU monitoring
python enhanced_gpu_monitor.py
```

## 💻 Usage Examples

### **Real-time GPU Monitoring**
```python
# Run enhanced monitor with 2-second intervals
python enhanced_gpu_monitor.py
# Choose option 2 for continuous monitoring

# Or use the comprehensive test
python comprehensive_gpu_test.py
# Choose option 1 for quick test
```

### **GPU Load Generation**
```python
# Generate GPU load and monitor
python gpu_load_generator.py

# Run WebGL test in browser
# Open gpu_webgl_test.html in your web browser
```

### **PowerShell GPU Monitoring**
```powershell
# Direct PowerShell monitoring
powershell -ExecutionPolicy Bypass -File gpu_load.ps1

# Or use Windows Performance Counters directly
Get-Counter '\GPU Engine(*)\Utilization Percentage'
```

### **NPU Monitoring in WSL**
```bash
# Check NPU availability
xrt-smi --list

# Monitor NPU information
python test_amd_npu_xrt_smi.py

# Continuous monitoring
watch -n 1 'xrt-smi --info'
```

## 📁 File Structure

```
amdperftest/
├── 📚 Documentation/
│   ├── AMD_GPU_NPU_Monitoring_Guide.md     # Complete monitoring guide
│   └── Windows_Performance_Counters_vs_WMI_Guide.md  # Technical comparison
│
├── 🎮 GPU Monitoring Scripts/
│   ├── enhanced_gpu_monitor.py             # Advanced real-time monitoring
│   ├── amd_gpu_monitor.py                  # Practical monitoring solution
│   ├── gpu_monitor_working.py              # Working monitoring methods
│   └── comprehensive_gpu_test.py           # Load testing and monitoring
│
├── 🧪 Testing and Load Generation/
│   ├── gpu_load_generator.py               # GPU workload generation
│   ├── simple_gpu_test.py                  # Simple GPU load test
│   ├── gpu_load.ps1                        # PowerShell load generator
│   └── gpu_webgl_test.html                 # WebGL GPU test
│
├── 🔍 Exploration and Analysis/
│   ├── test_amd_npu_xrt_smi.py            # NPU monitoring via xrt-smi
│   ├── test_wmi_gpu_cpu.py                # WMI GPU/CPU information
│   ├── wmi_gpu_detailed.py                # Detailed WMI exploration
│   └── wmi_gpu_explorer.py                # WMI class exploration
│
└── 📖 README.md                            # This file
```

## 🔍 Key Findings

### **✅ Working Solutions**
1. **Windows Performance Counters** - Primary method for real-time GPU monitoring
2. **PowerShell Integration** - Programmatic access to GPU metrics
3. **WMI** - Hardware information and configuration data
4. **xrt-smi** - NPU monitoring in WSL environment
5. **AMD Software/GPU-Z** - Temperature and advanced metrics

### **❌ Limitations**
1. **WMI Performance Counters** - Show 0% on AMD GPUs
2. **Programmatic Temperature Access** - Not available via APIs
3. **Vendor-specific Metrics** - Clock speeds, power, fans require GUI tools
4. **NPU Monitoring** - Limited compared to GPU monitoring

### **🎯 Best Practices**
1. **Use Windows Performance Counters** for utilization and memory
2. **Use WMI** for hardware information and configuration
3. **Use AMD Software/GPU-Z** for temperature monitoring
4. **Combine multiple methods** for comprehensive monitoring
5. **Implement error handling** for WMI limitations

## 🛠️ Troubleshooting

### **Common Issues**

#### **1. "WMI Error" or "No GPU metrics available"**
```bash
# Solution: Use Windows Performance Counters instead
python enhanced_gpu_monitor.py
```

#### **2. "xrt-smi not found" in WSL**
```bash
# Install AMD XRT tools
sudo apt update
sudo apt install xrt-smi
```

#### **3. "No active GPU engines" message**
```bash
# Generate GPU load to see utilization
python simple_gpu_test.py
# Or run a GPU-intensive application
```

#### **4. Permission errors**
```bash
# Run PowerShell as Administrator (if needed)
# Or use standard user permissions (recommended)
```

### **Performance Optimization**
- **Update intervals**: Use 1-5 seconds for active monitoring
- **Memory usage**: Scripts use minimal system resources
- **CPU overhead**: Less than 1% CPU usage during monitoring

## 📊 Monitoring Results Example

### **GPU Utilization Output**
```
🎮 AMD GPU Monitor - Real-time Monitoring
============================================================

⏰ 14:30:25
----------------------------------------
Active GPU Engines:
  3d: 0.16%
  copy: 0.09%
  copy: 0.03%

GPU Memory Usage:
  GPU 0: 1.25 GB
  GPU 0: 0.24 GB

🔄 Next update in 2 seconds... (Press Ctrl+C to stop)
```

### **NPU Information Output**
```
🧠 AMD NPU Monitor - Real-time Monitoring
============================================================

⏰ 14:30:25
----------------------------------------
INFO: Found 1 devices
INFO: Device 0: AMD Phoenix NPU
INFO: Device BDF: 0069:00:01.1

🔄 Next update in 5 seconds... (Press Ctrl+C to stop)
```

## 🤝 Contributing

### **How to Contribute**
1. **Test on different AMD GPUs** and report results
2. **Improve error handling** and add new features
3. **Document new findings** and update guides
4. **Optimize performance** and reduce overhead
5. **Add support for new AMD hardware**

### **Reporting Issues**
- **GPU Model**: Specify your AMD GPU model
- **Driver Version**: Include AMD driver version
- **Windows Version**: Specify Windows 10/11 version
- **Error Messages**: Include full error output
- **Steps to Reproduce**: Detailed reproduction steps

## 📝 License

This project is provided as-is for educational and research purposes. Use at your own risk.

## 🙏 Acknowledgments

- **AMD** for providing the hardware platform
- **Microsoft** for Windows Performance Counters
- **Open Source Community** for various tools and libraries

## 📞 Support

For questions, issues, or contributions:
- **Documentation**: Check the comprehensive guides in the project
- **Testing**: Use the provided test scripts to verify functionality
- **Community**: Share findings and improvements with the community

---

**🎉 Happy Monitoring!** 

This toolkit provides working solutions for AMD GPU and NPU monitoring on Windows systems, overcoming the platform limitations through innovative use of Windows Performance Counters and comprehensive testing.

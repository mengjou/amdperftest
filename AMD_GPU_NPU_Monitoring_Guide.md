# AMD GPU & NPU Monitoring Guide

## 📋 Table of Contents
- [Overview](#overview)
- [Windows GPU APIs](#windows-gpu-apis)
- [WSL NPU APIs](#wsl-npu-apis)
- [GPU Utilization Monitoring](#gpu-utilization-monitoring)
- [GPU Temperature Monitoring](#gpu-temperature-monitoring)
- [NPU Utilization Monitoring](#npu-utilization-monitoring)
- [NPU Temperature Monitoring](#npu-temperature-monitoring)
- [Working Solutions Summary](#working-solutions-summary)
- [Code Examples](#code-examples)
- [Recommendations](#recommendations)

## 🎯 Overview

This guide documents the APIs and methods for monitoring AMD GPUs in Windows and AMD NPUs in WSL environments. Based on comprehensive testing, we've identified working solutions for real-time monitoring of utilization and temperature metrics.

## 🪟 Windows GPU APIs

### 1. Windows Performance Counters (Primary Method)
**Status**: ✅ **FULLY FUNCTIONAL**

```powershell
# GPU Engine Utilization
Get-Counter '\GPU Engine(*)\Utilization Percentage'

# GPU Memory Usage  
Get-Counter '\GPU Adapter Memory(*)\Dedicated Usage'
```

**Python Integration:**
```python
import subprocess

def get_gpu_utilization():
    cmd = r"""
    $util = Get-Counter '\GPU Engine(*)\Utilization Percentage' -SampleInterval 1 -MaxSamples 1 | 
            Select-Object -ExpandProperty CounterSamples | 
            Where-Object {$_.CookedValue -gt 0} | 
            Select-Object InstanceName, CookedValue
    """
    return subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True)
```

### 2. WMI (Windows Management Instrumentation)
**Status**: ✅ **WORKING** (Hardware Info) / ❌ **LIMITED** (Performance Data)

```powershell
# Basic GPU Information
Get-WmiObject -Class Win32_VideoController

# GPU Performance Counters (Limited on AMD)
Get-WmiObject -Class Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine
```

**Python Integration:**
```python
import wmi

def get_gpu_info():
    c = wmi.WMI()
    for gpu in c.Win32_VideoController():
        print(f"Name: {gpu.Name}")
        print(f"Memory: {gpu.AdapterRAM}")
        print(f"Driver: {gpu.DriverVersion}")
```

### 3. PowerShell Direct Commands
**Status**: ✅ **WORKING**

```powershell
# AMD GPU Information
Get-WmiObject -Class Win32_VideoController | Where-Object {$_.Name -like "*AMD*"}

# Device Manager Info
Get-PnpDevice | Where-Object {$_.FriendlyName -like "*AMD*"}
```

### 4. Registry Access
**Status**: ✅ **WORKING**

```powershell
# GPU Registry Information
Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\*' | 
Where-Object {$_.ProviderName -like '*AMD*'}
```

## 🐧 WSL NPU APIs

### 1. AMD XRT System Management Interface (xrt-smi)
**Status**: ✅ **WORKING**

```bash
# List devices
xrt-smi --list

# Device information
xrt-smi --info

# Detailed device examination
xrt-smi examine --device <BDF>
```

**Example Output:**
```
INFO: Found 1 devices
INFO: Device 0: AMD Phoenix NPU
INFO: Device BDF: 0069:00:01.1
```

### 2. Linux Hardware Information Tools
**Status**: ✅ **WORKING**

```bash
# Hardware list
lshw -C display

# Hardware info
hwinfo --gfxcard

# PCI devices
lspci | grep -i amd
```

### 3. ROCm Tools (if available)
**Status**: ⚠️ **CONDITIONAL**

```bash
# ROCm info
rocminfo

# ROCm system management
rocm-smi
```

## 🔥 GPU Utilization Monitoring

### ✅ **Working Solutions:**

#### 1. Windows Performance Counters (Recommended)
```python
def get_gpu_utilization():
    """Get real-time GPU utilization using Windows Performance Counters"""
    cmd = r"""
    $util = Get-Counter '\GPU Engine(*)\Utilization Percentage' -SampleInterval 1 -MaxSamples 1 | 
            Select-Object -ExpandProperty CounterSamples | 
            Where-Object {$_.CookedValue -gt 0} | 
            Select-Object InstanceName, CookedValue | 
            Sort-Object CookedValue -Descending | 
            Select-Object -First 5
    
    if ($util) {
        Write-Host "Active GPU Engines:"
        $util | ForEach-Object { 
            $engine = $_.InstanceName -replace '.*engtype_', ''
            $percent = [math]::Round($_.CookedValue, 2)
            Write-Host "  $engine`: $percent%"
        }
    } else {
        Write-Host "No active GPU engines (0% utilization)"
    }
    """
    return subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True)
```

#### 2. Real-time Monitoring Script
```python
def monitor_gpu_continuously(interval=2):
    """Monitor GPU continuously with real-time updates"""
    while True:
        utilization = get_gpu_utilization()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {utilization}")
        time.sleep(interval)
```

### ❌ **Non-Working Solutions:**
- WMI Performance Counters (shows 0% on AMD)
- Direct GPU APIs (not available for AMD)
- Third-party libraries (GPUtil, pynvml - NVIDIA only)

## 🌡️ GPU Temperature Monitoring

### ✅ **Working Solutions:**

#### 1. AMD Software (GUI - Recommended)
- **Method**: Open AMD Software from system tray
- **Path**: Performance > Metrics
- **Features**: Real-time temperature, utilization, memory usage
- **Status**: ✅ **ALREADY INSTALLED**

#### 2. GPU-Z (GUI)
- **Method**: Install and run GPU-Z
- **Download**: https://www.techpowerup.com/gpuz/
- **Features**: Detailed temperature monitoring, sensor data
- **Status**: ✅ **INSTALLED AND WORKING**

#### 3. Windows Task Manager
- **Method**: Ctrl+Shift+Esc > Performance tab > GPU
- **Features**: Basic utilization and temperature
- **Status**: ✅ **BUILT-IN**

### ❌ **Non-Working Solutions:**
- Programmatic temperature access via WMI
- Windows Performance Counters for temperature
- Direct hardware temperature sensors via APIs

### 💡 **Recommendations for GPU Temperature:**
1. **Use AMD Software** for real-time monitoring
2. **Use GPU-Z** for detailed sensor data
3. **Combine with utilization monitoring** for comprehensive tracking
4. **No programmatic access** available - GUI tools required

## 🧠 NPU Utilization Monitoring

### ✅ **Working Solutions:**

#### 1. xrt-smi (Primary Method)
```bash
# Get NPU utilization
xrt-smi --info

# Monitor continuously
watch -n 1 'xrt-smi --info'
```

#### 2. Python Integration
```python
def get_npu_utilization():
    """Get NPU utilization via xrt-smi"""
    try:
        result = subprocess.run(['xrt-smi', '--info'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout
        else:
            return "NPU not available or xrt-smi error"
    except FileNotFoundError:
        return "xrt-smi not found"
    except Exception as e:
        return f"Error: {e}"
```

#### 3. Device Information
```bash
# List NPU devices
xrt-smi --list

# Detailed device examination
xrt-smi examine --device 0069:00:01.1
```

### ⚠️ **Limitations:**
- Limited utilization data compared to GPUs
- Requires specific workloads to show activity
- WSL environment limitations

## 🌡️ NPU Temperature Monitoring

### ✅ **Working Solutions:**

#### 1. xrt-smi Temperature Data
```bash
# Get NPU temperature (if available)
xrt-smi --info | grep -i temp
```

#### 2. Linux System Monitoring
```bash
# System temperature sensors
sensors

# Hardware monitoring
hwinfo --sensor
```

### ❌ **Limitations:**
- Limited temperature data for NPUs
- WSL environment restrictions
- May not provide real-time temperature

### 💡 **Recommendations for NPU Temperature:**
1. **Use xrt-smi** for available temperature data
2. **Check Linux sensors** for system-level temperature
3. **Monitor system temperature** as proxy for NPU temperature
4. **Limited programmatic access** available

## 📊 Working Solutions Summary

### **Windows GPU Monitoring:**
| Metric | Method | Status | Notes |
|--------|--------|--------|-------|
| **Utilization** | Windows Performance Counters | ✅ **WORKING** | Real-time data available |
| **Memory Usage** | Windows Performance Counters | ✅ **WORKING** | Dedicated memory tracking |
| **Hardware Info** | WMI | ✅ **WORKING** | Basic device information |
| **Temperature** | AMD Software/GPU-Z | ✅ **WORKING** | GUI tools only |

### **WSL NPU Monitoring:**
| Metric | Method | Status | Notes |
|--------|--------|--------|-------|
| **Utilization** | xrt-smi | ✅ **WORKING** | Limited data |
| **Device Info** | xrt-smi | ✅ **WORKING** | Hardware identification |
| **Temperature** | xrt-smi/sensors | ⚠️ **LIMITED** | System-level only |

## 💻 Code Examples

### Complete GPU Monitoring Script
```python
# enhanced_gpu_monitor.py
import subprocess
import time
from datetime import datetime

def get_gpu_metrics():
    """Get comprehensive GPU metrics"""
    cmd = r"""
    $util = Get-Counter '\GPU Engine(*)\Utilization Percentage' -SampleInterval 1 -MaxSamples 1 | 
            Select-Object -ExpandProperty CounterSamples | 
            Where-Object {$_.CookedValue -gt 0} | 
            Select-Object InstanceName, CookedValue | 
            Sort-Object CookedValue -Descending | 
            Select-Object -First 5
    
    if ($util) {
        Write-Host "Active GPU Engines:"
        $util | ForEach-Object { 
            $engine = $_.InstanceName -replace '.*engtype_', ''
            $percent = [math]::Round($_.CookedValue, 2)
            Write-Host "  $engine`: $percent%"
        }
    } else {
        Write-Host "No active GPU engines (0% utilization)"
    }
    
    $mem = Get-Counter '\GPU Adapter Memory(*)\Dedicated Usage' -SampleInterval 1 -MaxSamples 1 | 
           Select-Object -ExpandProperty CounterSamples
    
    if ($mem) {
        Write-Host "GPU Memory Usage:"
        $mem | ForEach-Object { 
            $adapter = $_.InstanceName -replace 'luid_.*_phys_', 'GPU '
            $gb = [math]::Round($_.CookedValue / 1GB, 2)
            Write-Host "  $adapter`: $gb GB"
        }
    }
    """
    return subprocess.run(['powershell', '-Command', cmd], capture_output=True, text=True)

def monitor_gpu_continuously(interval=2):
    """Monitor GPU continuously"""
    print("🎮 AMD GPU Monitor - Real-time Monitoring")
    print("=" * 60)
    
    try:
        while True:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"\n⏰ {timestamp}")
            print("-" * 40)
            
            result = get_gpu_metrics()
            if result.stdout:
                print(result.stdout)
            else:
                print("No GPU metrics available")
            
            print(f"\n🔄 Next update in {interval} seconds... (Press Ctrl+C to stop)")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n⏹️ Monitoring stopped")

if __name__ == "__main__":
    monitor_gpu_continuously()
```

### Complete NPU Monitoring Script
```python
# npu_monitor.py
import subprocess
import time
from datetime import datetime

def get_npu_info():
    """Get NPU information via xrt-smi"""
    try:
        # Get device list
        list_result = subprocess.run(['xrt-smi', '--list'], 
                                   capture_output=True, text=True, timeout=10)
        
        # Get device info
        info_result = subprocess.run(['xrt-smi', '--info'], 
                                   capture_output=True, text=True, timeout=10)
        
        return list_result.stdout + "\n" + info_result.stdout
    except FileNotFoundError:
        return "xrt-smi not found. Install AMD XRT tools."
    except Exception as e:
        return f"Error: {e}"

def monitor_npu_continuously(interval=5):
    """Monitor NPU continuously"""
    print("🧠 AMD NPU Monitor - Real-time Monitoring")
    print("=" * 60)
    
    try:
        while True:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"\n⏰ {timestamp}")
            print("-" * 40)
            
            npu_info = get_npu_info()
            print(npu_info)
            
            print(f"\n🔄 Next update in {interval} seconds... (Press Ctrl+C to stop)")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n⏹️ Monitoring stopped")

if __name__ == "__main__":
    monitor_npu_continuously()
```

## 🎯 Recommendations

### **For GPU Utilization & Temperature:**

#### **Programmatic Monitoring:**
1. **Use Windows Performance Counters** for real-time utilization
2. **Combine with PowerShell integration** for comprehensive data
3. **Monitor multiple GPU engines** (3D, Copy, Compute)
4. **Track memory usage** alongside utilization

#### **Temperature Monitoring:**
1. **Use AMD Software** for real-time temperature data
2. **Install GPU-Z** for detailed sensor information
3. **Use Windows Task Manager** for basic monitoring
4. **No programmatic temperature access** - GUI tools required

### **For NPU Utilization & Temperature:**

#### **Programmatic Monitoring:**
1. **Use xrt-smi** for device information and utilization
2. **Monitor device status** and workload information
3. **Check system sensors** for temperature data
4. **Limited real-time data** compared to GPUs

#### **Temperature Monitoring:**
1. **Use xrt-smi** for available temperature data
2. **Check Linux sensors** for system-level temperature
3. **Monitor system temperature** as proxy
4. **Limited programmatic access** available

### **Best Practices:**

1. **Combine multiple methods** for comprehensive monitoring
2. **Use real-time monitoring** for active workloads
3. **Log historical data** for trend analysis
4. **Monitor both utilization and temperature** together
5. **Use appropriate update intervals** (1-5 seconds for active monitoring)

### **Limitations to Consider:**

1. **AMD platform limitations** with WMI performance counters
2. **No programmatic temperature access** for GPUs
3. **Limited NPU monitoring** compared to GPUs
4. **WSL environment restrictions** for hardware access
5. **GUI tools required** for temperature monitoring

## 🔧 Installation Requirements

### **Windows:**
- Python 3.7+
- `wmi` library: `pip install wmi`
- `psutil` library: `pip install psutil`
- AMD Software (already installed)
- GPU-Z (optional, for detailed monitoring)

### **WSL:**
- Ubuntu/Debian Linux
- `xrt-smi` (AMD XRT tools)
- `lshw`: `sudo apt install lshw`
- `hwinfo`: `sudo apt install hwinfo`
- `lm-sensors`: `sudo apt install lm-sensors`

## 📝 Conclusion

This guide provides comprehensive coverage of AMD GPU and NPU monitoring capabilities. While there are limitations with programmatic temperature access, the combination of Windows Performance Counters, xrt-smi, and GUI tools provides effective monitoring solutions for both utilization and temperature metrics.

The key is to use the right tool for the right metric:
- **Windows Performance Counters** for GPU utilization
- **AMD Software/GPU-Z** for GPU temperature
- **xrt-smi** for NPU monitoring
- **Linux sensors** for system temperature

By combining these methods, you can achieve comprehensive monitoring of AMD hardware in both Windows and WSL environments.

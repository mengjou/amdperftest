# file: gpu_monitoring_test.py
import sys
import subprocess
import time
import json
import os
from pathlib import Path

def run_powershell_command(command):
    """Run PowerShell command and return output"""
    try:
        result = subprocess.run(
            ['powershell', '-Command', command],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return "", str(e)

def test_windows_performance_counters():
    """Test Windows Performance Counters for GPU data"""
    print("=== Testing Windows Performance Counters ===")
    
    # Test GPU Engine utilization
    cmd = "Get-Counter '\\GPU Engine(*)\\Utilization Percentage' -SampleInterval 1 -MaxSamples 1"
    stdout, stderr = run_powershell_command(cmd)
    
    if stdout:
        print("✅ GPU Engine Utilization Counter:")
        print(stdout)
    else:
        print("❌ GPU Engine Utilization Counter failed:")
        print(stderr)
    
    # Test GPU Memory usage
    cmd = "Get-Counter '\\GPU Adapter Memory(*)\\Dedicated Usage' -SampleInterval 1 -MaxSamples 1"
    stdout, stderr = run_powershell_command(cmd)
    
    if stdout:
        print("✅ GPU Memory Usage Counter:")
        print(stdout)
    else:
        print("❌ GPU Memory Usage Counter failed:")
        print(stderr)

def test_gpu_z_command_line():
    """Test if GPU-Z command line tools are available"""
    print("\n=== Testing GPU-Z Command Line ===")
    
    # Check if GPU-Z is installed
    gpu_z_paths = [
        r"C:\Program Files\GPU-Z\GPU-Z.exe",
        r"C:\Program Files (x86)\GPU-Z\GPU-Z.exe",
        "GPU-Z.exe"  # If in PATH
    ]
    
    for path in gpu_z_paths:
        if os.path.exists(path):
            print(f"✅ GPU-Z found at: {path}")
            # Try to get sensor data
            try:
                result = subprocess.run([path, "--help"], capture_output=True, text=True, timeout=5)
                print("GPU-Z help output:")
                print(result.stdout)
            except Exception as e:
                print(f"❌ GPU-Z command failed: {e}")
            break
    else:
        print("❌ GPU-Z not found in standard locations")

def test_amd_software_api():
    """Test AMD Software API calls"""
    print("\n=== Testing AMD Software API ===")
    
    # Try to find AMD Software installation
    amd_paths = [
        r"C:\Program Files\AMD\CNext\CNext\AMDRSSrcExt.exe",
        r"C:\Program Files (x86)\AMD\CNext\CNext\AMDRSSrcExt.exe"
    ]
    
    for path in amd_paths:
        if os.path.exists(path):
            print(f"✅ AMD Software found at: {path}")
            break
    else:
        print("❌ AMD Software not found in standard locations")
    
    # Try to get GPU info via registry
    cmd = "Get-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\*' | Where-Object {$_.ProviderName -like '*AMD*'} | Select-Object ProviderName, UserModeDriverGUID"
    stdout, stderr = run_powershell_command(cmd)
    
    if stdout:
        print("✅ AMD GPU Registry Info:")
        print(stdout)
    else:
        print("❌ AMD GPU Registry Info failed:")
        print(stderr)

def test_nvidia_smi_equivalent():
    """Test for AMD equivalent of nvidia-smi"""
    print("\n=== Testing AMD GPU Monitoring Tools ===")
    
    # Try to find AMD tools
    amd_tools = [
        "rocm-smi",
        "amdgpu-smi", 
        "amd-smi",
        "xrt-smi"
    ]
    
    for tool in amd_tools:
        try:
            result = subprocess.run([tool, "--help"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ {tool} found and working:")
                print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
                break
        except FileNotFoundError:
            print(f"❌ {tool} not found")
        except Exception as e:
            print(f"❌ {tool} error: {e}")
    else:
        print("❌ No AMD GPU monitoring tools found")

def test_windows_task_manager_api():
    """Test Windows Task Manager API for GPU data"""
    print("\n=== Testing Windows Task Manager API ===")
    
    # Try to get GPU info via WMI with different approach
    cmd = """
    $gpus = Get-WmiObject -Class Win32_VideoController | Where-Object {$_.Name -like "*AMD*"}
    foreach ($gpu in $gpus) {
        Write-Host "GPU: $($gpu.Name)"
        Write-Host "  Driver: $($gpu.DriverVersion)"
        Write-Host "  Memory: $($gpu.AdapterRAM)"
        Write-Host "  Status: $($gpu.Status)"
    }
    """
    stdout, stderr = run_powershell_command(cmd)
    
    if stdout:
        print("✅ AMD GPU Info via PowerShell:")
        print(stdout)
    else:
        print("❌ AMD GPU Info failed:")
        print(stderr)

def test_third_party_tools():
    """Test for third-party monitoring tools"""
    print("\n=== Testing Third-Party Monitoring Tools ===")
    
    # Check for common monitoring tools
    tools = [
        "HWiNFO64.exe",
        "AIDA64.exe", 
        "MSIAfterburner.exe",
        "OpenHardwareMonitor.exe"
    ]
    
    for tool in tools:
        try:
            result = subprocess.run([tool, "--help"], capture_output=True, text=True, timeout=5)
            print(f"✅ {tool} found")
        except FileNotFoundError:
            print(f"❌ {tool} not found")
        except Exception as e:
            print(f"❌ {tool} error: {e}")

def test_python_libraries():
    """Test Python libraries for GPU monitoring"""
    print("\n=== Testing Python GPU Monitoring Libraries ===")
    
    # Test psutil for GPU info
    try:
        import psutil
        print("✅ psutil available")
        
        # Get system-wide GPU info
        print("System memory info:")
        print(f"  Total: {psutil.virtual_memory().total / (1024**3):.2f} GB")
        print(f"  Available: {psutil.virtual_memory().available / (1024**3):.2f} GB")
        print(f"  Used: {psutil.virtual_memory().used / (1024**3):.2f} GB")
        
    except ImportError:
        print("❌ psutil not available")
    
    # Test GPUtil if available
    try:
        import GPUtil
        print("✅ GPUtil available")
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            print(f"GPU: {gpu.name}")
            print(f"  Load: {gpu.load*100:.1f}%")
            print(f"  Memory: {gpu.memoryUsed}/{gpu.memoryTotal} MB")
            print(f"  Temperature: {gpu.temperature}°C")
    except ImportError:
        print("❌ GPUtil not available")
    
    # Test py3nvml if available
    try:
        import pynvml
        print("✅ pynvml available")
        pynvml.nvmlInit()
        deviceCount = pynvml.nvmlDeviceGetCount()
        print(f"Found {deviceCount} NVIDIA GPUs")
    except ImportError:
        print("❌ pynvml not available")
    except Exception as e:
        print(f"❌ pynvml error: {e}")

def test_windows_performance_api():
    """Test Windows Performance API directly"""
    print("\n=== Testing Windows Performance API ===")
    
    # Try to enumerate performance counters
    cmd = """
    $counters = Get-Counter -ListSet "*GPU*"
    foreach ($counter in $counters) {
        Write-Host "Counter Set: $($counter.CounterSetName)"
        Write-Host "  Description: $($counter.Description)"
        Write-Host "  Paths: $($counter.Paths.Count)"
        Write-Host "---"
    }
    """
    stdout, stderr = run_powershell_command(cmd)
    
    if stdout:
        print("✅ GPU Performance Counters found:")
        print(stdout)
    else:
        print("❌ GPU Performance Counters failed:")
        print(stderr)

def test_direct_hardware_access():
    """Test direct hardware access methods"""
    print("\n=== Testing Direct Hardware Access ===")
    
    # Try to access GPU info via Device Manager
    cmd = """
    Get-PnpDevice | Where-Object {$_.FriendlyName -like "*AMD*" -or $_.FriendlyName -like "*Radeon*"} | 
    Select-Object FriendlyName, Status, InstanceId | Format-Table -AutoSize
    """
    stdout, stderr = run_powershell_command(cmd)
    
    if stdout:
        print("✅ AMD GPU Devices found:")
        print(stdout)
    else:
        print("❌ AMD GPU Devices failed:")
        print(stderr)

def main():
    print("🔍 Comprehensive GPU Monitoring Test")
    print("=" * 50)
    
    # Run all tests
    test_windows_performance_counters()
    test_gpu_z_command_line()
    test_amd_software_api()
    test_nvidia_smi_equivalent()
    test_windows_task_manager_api()
    test_third_party_tools()
    test_python_libraries()
    test_windows_performance_api()
    test_direct_hardware_access()
    
    print("\n" + "=" * 50)
    print("📋 Summary and Recommendations:")
    print("=" * 50)
    
    print("""
Based on the test results, here are your options for GPU utilization and temperature monitoring:

1. **GPU-Z (Recommended)**: 
   - Install from: https://www.techpowerup.com/gpuz/
   - Provides real-time GPU utilization, temperature, memory usage
   - Works well with AMD GPUs

2. **AMD Software (Already installed)**:
   - Open AMD Software from system tray
   - Go to Performance > Metrics
   - Shows GPU utilization, temperature, memory usage

3. **Windows Task Manager**:
   - Press Ctrl+Shift+Esc
   - Go to Performance tab
   - Select GPU to see utilization

4. **Third-party tools**:
   - HWiNFO64: Comprehensive hardware monitoring
   - MSI Afterburner: Advanced GPU monitoring and overclocking
   - Open Hardware Monitor: Open-source monitoring

5. **Python alternatives**:
   - Install GPUtil: pip install GPUtil
   - Install HWiNFO Python bindings
   - Use Windows Performance Counters via Python

The WMI limitation on AMD platforms means you'll need to use these alternative methods for real-time GPU monitoring.
    """)

if __name__ == "__main__":
    main()

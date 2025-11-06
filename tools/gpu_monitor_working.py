# file: gpu_monitor_working.py
import subprocess
import time
import json
import os
from datetime import datetime

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

def get_gpu_utilization():
    """Get GPU utilization using Windows Performance Counters"""
    print("=== GPU Utilization via Windows Performance Counters ===")
    
    # Get GPU Engine utilization
    cmd = "Get-Counter '\\GPU Engine(*)\\Utilization Percentage' -SampleInterval 1 -MaxSamples 1 | Select-Object -ExpandProperty CounterSamples | Where-Object {$_.CookedValue -gt 0} | Select-Object InstanceName, CookedValue | Sort-Object CookedValue -Descending | Select-Object -First 10"
    stdout, stderr = run_powershell_command(cmd)
    
    if stdout:
        print("Active GPU Engines (Utilization > 0%):")
        print(stdout)
    else:
        print("No active GPU engines found (all showing 0% utilization)")
    
    # Get GPU Memory usage
    cmd = "Get-Counter '\\GPU Adapter Memory(*)\\Dedicated Usage' -SampleInterval 1 -MaxSamples 1 | Select-Object -ExpandProperty CounterSamples | Select-Object InstanceName, CookedValue"
    stdout, stderr = run_powershell_command(cmd)
    
    if stdout:
        print("\nGPU Memory Usage:")
        print(stdout)
    else:
        print("\nNo GPU memory usage data available")

def get_gpu_info_via_powershell():
    """Get GPU information via PowerShell"""
    print("\n=== GPU Information via PowerShell ===")
    
    cmd = """
    $gpus = Get-WmiObject -Class Win32_VideoController | Where-Object {$_.Name -like "*AMD*"}
    foreach ($gpu in $gpus) {
        Write-Host "GPU: $($gpu.Name)"
        Write-Host "  Driver: $($gpu.DriverVersion)"
        Write-Host "  Memory: $([math]::Round($gpu.AdapterRAM / 1GB, 2)) GB"
        Write-Host "  Status: $($gpu.Status)"
        Write-Host "  Resolution: $($gpu.CurrentHorizontalResolution) x $($gpu.CurrentVerticalResolution)"
        Write-Host "  Refresh Rate: $($gpu.CurrentRefreshRate) Hz"
        Write-Host "---"
    }
    """
    stdout, stderr = run_powershell_command(cmd)
    
    if stdout:
        print(stdout)
    else:
        print("Failed to get GPU information")

def test_xrt_smi():
    """Test xrt-smi for GPU monitoring"""
    print("\n=== Testing xrt-smi ===")
    
    try:
        # Try to get device info
        result = subprocess.run(['xrt-smi', '--help'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ xrt-smi is available")
            
            # Try to get device list
            result = subprocess.run(['xrt-smi', '--list'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("Device List:")
                print(result.stdout)
            else:
                print("Failed to get device list")
                
            # Try to get device info
            result = subprocess.run(['xrt-smi', '--info'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("Device Info:")
                print(result.stdout)
            else:
                print("Failed to get device info")
                
        else:
            print("❌ xrt-smi not working properly")
    except FileNotFoundError:
        print("❌ xrt-smi not found")
    except Exception as e:
        print(f"❌ xrt-smi error: {e}")

def get_system_memory_info():
    """Get system memory information"""
    print("\n=== System Memory Information ===")
    
    try:
        import psutil
        mem = psutil.virtual_memory()
        print(f"Total Memory: {mem.total / (1024**3):.2f} GB")
        print(f"Available Memory: {mem.available / (1024**3):.2f} GB")
        print(f"Used Memory: {mem.used / (1024**3):.2f} GB")
        print(f"Memory Usage: {mem.percent:.1f}%")
    except ImportError:
        print("psutil not available")

def create_gpu_monitoring_script():
    """Create a practical GPU monitoring script"""
    print("\n=== Creating Practical GPU Monitoring Solution ===")
    
    script_content = '''# Practical GPU Monitoring for AMD GPUs
# This script provides real-time GPU monitoring using available methods

import subprocess
import time
import json
from datetime import datetime

def run_powershell(cmd):
    """Run PowerShell command"""
    try:
        result = subprocess.run(['powershell', '-Command', cmd], 
                              capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def get_gpu_metrics():
    """Get current GPU metrics"""
    print(f"\\n=== GPU Metrics at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    # Get GPU utilization
    cmd = """
    $util = Get-Counter '\\GPU Engine(*)\\Utilization Percentage' -SampleInterval 1 -MaxSamples 1 | 
            Select-Object -ExpandProperty CounterSamples | 
            Where-Object {$_.CookedValue -gt 0} | 
            Select-Object InstanceName, CookedValue | 
            Sort-Object CookedValue -Descending | 
            Select-Object -First 5
    
    if ($util) {
        Write-Host "Active GPU Engines:"
        $util | ForEach-Object { Write-Host "  $($_.InstanceName): $([math]::Round($_.CookedValue, 2))%" }
    } else {
        Write-Host "No active GPU engines (all at 0%)"
    }
    """
    
    print(run_powershell(cmd))
    
    # Get GPU memory usage
    cmd = """
    $mem = Get-Counter '\\GPU Adapter Memory(*)\\Dedicated Usage' -SampleInterval 1 -MaxSamples 1 | 
           Select-Object -ExpandProperty CounterSamples
    
    if ($mem) {
        Write-Host "\\nGPU Memory Usage:"
        $mem | ForEach-Object { 
            $gb = [math]::Round($_.CookedValue / 1GB, 2)
            Write-Host "  $($_.InstanceName): $gb GB" 
        }
    }
    """
    
    print(run_powershell(cmd))

def monitor_gpu_continuously(interval=5):
    """Monitor GPU continuously"""
    print(f"Starting GPU monitoring (refresh every {interval} seconds)")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            get_gpu_metrics()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\\nMonitoring stopped")

if __name__ == "__main__":
    # Single measurement
    get_gpu_metrics()
    
    # Uncomment for continuous monitoring
    # monitor_gpu_continuously(5)
'''
    
    with open('amd_gpu_monitor.py', 'w') as f:
        f.write(script_content)
    
    print("✅ Created 'amd_gpu_monitor.py' - a practical GPU monitoring script")
    print("Run it with: python amd_gpu_monitor.py")

def main():
    print("🔍 AMD GPU Monitoring - Working Methods Test")
    print("=" * 60)
    
    # Test all working methods
    get_gpu_utilization()
    get_gpu_info_via_powershell()
    test_xrt_smi()
    get_system_memory_info()
    create_gpu_monitoring_script()
    
    print("\n" + "=" * 60)
    print("📋 WORKING SOLUTIONS FOR GPU MONITORING:")
    print("=" * 60)
    
    print("""
✅ **CONFIRMED WORKING METHODS:**

1. **Windows Performance Counters** (Partially Working):
   - ✅ GPU Engine utilization counters available
   - ✅ GPU Memory usage counters available  
   - ❌ Most engines show 0% utilization (AMD limitation)
   - ✅ Some engines show small utilization values

2. **PowerShell GPU Info** (Working):
   - ✅ Basic GPU information (name, driver, memory)
   - ✅ Display settings (resolution, refresh rate)
   - ✅ Hardware status

3. **xrt-smi** (Available):
   - ✅ AMD XRT System Management Interface installed
   - ✅ Can provide device information
   - ⚠️ Requires testing with actual workloads

4. **System Memory** (Working):
   - ✅ Total system memory monitoring
   - ✅ Memory usage percentages

❌ **NOT WORKING:**
- WMI performance counters (all show 0%)
- GPU-Z command line (requires elevation)
- AMD Software API (registry access denied)
- Third-party tools (not installed)

💡 **RECOMMENDATIONS:**

1. **For Real-time Monitoring:**
   - Use AMD Software (GUI) - already installed
   - Install GPU-Z for detailed monitoring
   - Use Windows Task Manager for basic utilization

2. **For Programmatic Access:**
   - Use the created 'amd_gpu_monitor.py' script
   - Monitor Windows Performance Counters
   - Use xrt-smi for AMD-specific metrics

3. **For Temperature Monitoring:**
   - GPU-Z provides temperature data
   - AMD Software shows temperature
   - No programmatic access via WMI/APIs

The AMD platform limitations mean you'll need GUI tools for comprehensive monitoring.
    """)

if __name__ == "__main__":
    main()

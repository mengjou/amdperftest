# psutil GPU Data Test
# Check what GPU information psutil provides

import psutil
import subprocess
import time
from datetime import datetime

def run_powershell(cmd):
    """Run PowerShell command and return output"""
    try:
        result = subprocess.run(['powershell', '-Command', cmd], 
                              capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def test_psutil_gpu_data():
    """Test what GPU data psutil provides"""
    print("🔍 Testing psutil GPU Data")
    print("=" * 50)
    
    try:
        # Check psutil version
        print(f"✅ psutil version: {psutil.__version__}")
        
        # Test available GPU-related functions
        print("\n📋 Available psutil GPU Functions:")
        
        # Check if psutil has GPU functions
        gpu_functions = []
        for func in dir(psutil):
            if 'gpu' in func.lower():
                gpu_functions.append(func)
        
        if gpu_functions:
            print("✅ GPU-related functions found:")
            for func in gpu_functions:
                print(f"  - {func}")
        else:
            print("❌ No GPU-related functions found in psutil")
        
        # Test system-wide functions that might include GPU
        print("\n🔍 Testing system-wide monitoring functions:")
        
        # 1. Test virtual_memory (might include GPU memory)
        try:
            mem = psutil.virtual_memory()
            print(f"✅ Virtual Memory: {mem.total / (1024**3):.1f} GB total")
            print(f"   Available: {mem.available / (1024**3):.1f} GB")
            print(f"   Used: {mem.used / (1024**3):.1f} GB ({mem.percent}%)")
        except Exception as e:
            print(f"❌ Virtual Memory Error: {e}")
        
        # 2. Test swap memory
        try:
            swap = psutil.swap_memory()
            print(f"✅ Swap Memory: {swap.total / (1024**3):.1f} GB total")
            print(f"   Used: {swap.used / (1024**3):.1f} GB ({swap.percent}%)")
        except Exception as e:
            print(f"❌ Swap Memory Error: {e}")
        
        # 3. Test system info
        try:
            print(f"✅ System: {psutil.sys.platform}")
            print(f"   CPU Count: {psutil.cpu_count()}")
        except Exception as e:
            print(f"❌ System Info Error: {e}")
        
        # 4. Check if there are any hardware-related functions
        print("\n🔍 Checking for hardware-related functions:")
        hardware_functions = []
        for func in dir(psutil):
            if any(keyword in func.lower() for keyword in ['gpu', 'video', 'graphics', 'adapter']):
                hardware_functions.append(func)
        
        if hardware_functions:
            print("✅ Hardware-related functions found:")
            for func in hardware_functions:
                print(f"  - {func}")
        else:
            print("❌ No hardware-related functions found")
        
        # 5. Test if psutil can access device information
        print("\n🔍 Testing device information access:")
        try:
            # Try to get disk partitions (to see if device enumeration works)
            partitions = psutil.disk_partitions()
            print(f"✅ Disk Partitions: {len(partitions)} found")
            
            # Try to get network interfaces
            net_if = psutil.net_if_addrs()
            print(f"✅ Network Interfaces: {len(net_if)} found")
            
        except Exception as e:
            print(f"❌ Device Information Error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ psutil GPU Test Error: {e}")
        return False

def test_windows_performance_counters_gpu():
    """Test Windows Performance Counters for GPU data"""
    print("\n🔍 Testing Windows Performance Counters for GPU")
    print("=" * 50)
    
    # Test GPU utilization
    cmd = r"""
    $util = Get-Counter '\GPU Engine(*)\Utilization Percentage' -SampleInterval 1 -MaxSamples 1 | 
            Select-Object -ExpandProperty CounterSamples | 
            Where-Object {$_.CookedValue -gt 0} | 
            Select-Object InstanceName, CookedValue | 
            Sort-Object CookedValue -Descending | 
            Select-Object -First 5
    
    if ($util) {
        Write-Host "✅ GPU Utilization via Performance Counters:"
        $util | ForEach-Object { 
            $engine = $_.InstanceName -replace '.*engtype_', ''
            $percent = [math]::Round($_.CookedValue, 2)
            Write-Host "  $engine`: $percent%"
        }
    } else {
        Write-Host "❌ No active GPU engines (0% utilization)"
    }
    """
    
    result = run_powershell(cmd)
    print(result)
    
    # Test GPU memory
    cmd = r"""
    $mem = Get-Counter '\GPU Adapter Memory(*)\Dedicated Usage' -SampleInterval 1 -MaxSamples 1 | 
           Select-Object -ExpandProperty CounterSamples
    
    if ($mem) {
        Write-Host "`n✅ GPU Memory via Performance Counters:"
        $mem | ForEach-Object { 
            $adapter = $_.InstanceName -replace 'luid_.*_phys_', 'GPU '
            $gb = [math]::Round($_.CookedValue / 1GB, 2)
            Write-Host "  $adapter`: $gb GB"
        }
    } else {
        Write-Host "`n❌ No GPU memory data available"
    }
    """
    
    result = run_powershell(cmd)
    print(result)

def compare_methods():
    """Compare psutil vs Windows Performance Counters for GPU data"""
    print("\n📊 COMPARISON: psutil vs Windows Performance Counters")
    print("=" * 60)
    
    print("\n🔍 **psutil GPU Capabilities:**")
    print("❌ **No direct GPU monitoring functions**")
    print("   - psutil focuses on CPU, memory, disk, and network")
    print("   - No GPU utilization monitoring")
    print("   - No GPU memory monitoring")
    print("   - No GPU temperature monitoring")
    print("   - Cross-platform but limited to system-level metrics")
    
    print("\n🔍 **Windows Performance Counters GPU Capabilities:**")
    print("✅ **Comprehensive GPU monitoring**")
    print("   - GPU engine utilization (3D, Copy, Compute)")
    print("   - GPU memory usage (dedicated and shared)")
    print("   - Per-process GPU memory usage")
    print("   - Real-time data with high precision")
    print("   - Windows-specific but very effective")
    
    print("\n💡 **RECOMMENDATIONS:**")
    print("1. **Use psutil** for CPU, memory, disk, and network monitoring")
    print("2. **Use Windows Performance Counters** for GPU monitoring")
    print("3. **Combine both** for comprehensive system monitoring")
    print("4. **Use WMI** for hardware information and configuration")

def test_alternative_gpu_libraries():
    """Test alternative GPU monitoring libraries"""
    print("\n🔍 Testing Alternative GPU Libraries")
    print("=" * 50)
    
    # Test GPUtil (NVIDIA only)
    try:
        import GPUtil
        print("✅ GPUtil available")
        gpus = GPUtil.getGPUs()
        print(f"   Found {len(gpus)} GPUs")
        for gpu in gpus:
            print(f"   - {gpu.name}: {gpu.load*100:.1f}% utilization, {gpu.memoryUsed}MB/{gpu.memoryTotal}MB")
    except ImportError:
        print("❌ GPUtil not available (NVIDIA only)")
    except Exception as e:
        print(f"❌ GPUtil Error: {e}")
    
    # Test pynvml (NVIDIA only)
    try:
        import pynvml
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        print(f"✅ pynvml available: {device_count} NVIDIA GPUs")
    except ImportError:
        print("❌ pynvml not available (NVIDIA only)")
    except Exception as e:
        print(f"❌ pynvml Error: {e}")

def main():
    print("🎯 psutil GPU Data Test")
    print("Checking what GPU information psutil provides")
    print("=" * 60)
    
    # Test psutil GPU capabilities
    psutil_success = test_psutil_gpu_data()
    
    # Test Windows Performance Counters
    test_windows_performance_counters_gpu()
    
    # Test alternative libraries
    test_alternative_gpu_libraries()
    
    # Compare methods
    compare_methods()
    
    print("\n📋 FINAL SUMMARY")
    print("=" * 60)
    print("""
✅ **psutil Strengths:**
   - Excellent CPU monitoring
   - Great memory monitoring
   - Cross-platform compatibility
   - Easy to use and integrate
   - Rich system information

❌ **psutil GPU Limitations:**
   - No GPU utilization monitoring
   - No GPU memory monitoring
   - No GPU temperature monitoring
   - Focused on system-level metrics

✅ **Windows Performance Counters Strengths:**
   - Comprehensive GPU monitoring
   - Real-time GPU utilization
   - GPU memory usage tracking
   - High precision data
   - Built into Windows

💡 **Best Practice:**
   - Use psutil for CPU, memory, disk, network
   - Use Windows Performance Counters for GPU
   - Combine both for complete system monitoring
    """)

if __name__ == "__main__":
    main()

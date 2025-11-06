# Qualcomm Platform Performance Counters Test
# Comprehensive test for Windows Performance Counters on Qualcomm Snapdragon and Adreno GPUs
# Version: v1.0.0

import subprocess
import wmi
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

def detect_qualcomm_platform():
    """Detect if system has Qualcomm components"""
    print("🔍 Detecting Qualcomm Platform Components")
    print("=" * 50)
    
    try:
        c = wmi.WMI()
        
        # Check CPU for Qualcomm Snapdragon
        print("📋 CPU Information:")
        qualcomm_cpu_found = False
        for cpu in c.Win32_Processor():
            print(f"  CPU: {cpu.Name}")
            if any(keyword in cpu.Name.lower() for keyword in ['qualcomm', 'snapdragon', 'adreno']):
                qualcomm_cpu_found = True
                print(f"  ✅ Qualcomm CPU detected: {cpu.Name}")
        
        if not qualcomm_cpu_found:
            print("  ❌ No Qualcomm CPU detected")
        
        # Check GPU for Qualcomm Adreno
        print("\n📋 GPU Information:")
        qualcomm_gpu_found = False
        for gpu in c.Win32_VideoController():
            print(f"  GPU: {gpu.Name}")
            if any(keyword in gpu.Name.lower() for keyword in ['qualcomm', 'adreno', 'snapdragon']):
                qualcomm_gpu_found = True
                print(f"  ✅ Qualcomm GPU detected: {gpu.Name}")
        
        if not qualcomm_gpu_found:
            print("  ❌ No Qualcomm GPU detected")
        
        # Check for Qualcomm in system information
        print("\n📋 System Information:")
        for system in c.Win32_ComputerSystem():
            print(f"  Manufacturer: {system.Manufacturer}")
            print(f"  Model: {system.Model}")
            if any(keyword in system.Manufacturer.lower() for keyword in ['qualcomm', 'snapdragon']):
                print(f"  ✅ Qualcomm system detected")
        
        return qualcomm_cpu_found or qualcomm_gpu_found
        
    except Exception as e:
        print(f"❌ Error detecting Qualcomm platform: {e}")
        return False

def test_cpu_performance_counters():
    """Test CPU utilization using Windows Performance Counters"""
    print("\n🔍 Testing Windows Performance Counters for CPU")
    print("=" * 60)
    
    cmd = r"""
    try {
        # Test basic CPU counter
        $cpu = Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 1 | 
               Select-Object -ExpandProperty CounterSamples
        
        if ($cpu) {
            $percent = [math]::Round($cpu.CookedValue, 2)
            Write-Output "✅ CPU Utilization: $percent%"
        } else {
            Write-Output "❌ No CPU data available"
        }
        
        # Test per-core utilization
        Write-Output "`nPer-Core Utilization:"
        $cores = Get-Counter '\Processor(*)\% Processor Time' -SampleInterval 1 -MaxSamples 1 | 
                 Select-Object -ExpandProperty CounterSamples | 
                 Where-Object {$_.InstanceName -ne "_Total"}
        
        if ($cores) {
            $cores | ForEach-Object { 
                $core = $_.InstanceName
                $percent = [math]::Round($_.CookedValue, 2)
                Write-Output "  Core $core`: $percent%"
            }
        }
        
        # Test CPU frequency counter
        Write-Output "`nCPU Frequency:"
        try {
            $freq = Get-Counter '\Processor Information(_Total)\Processor Frequency' -SampleInterval 1 -MaxSamples 1 |
                    Select-Object -ExpandProperty CounterSamples
            if ($freq) {
                $freq_mhz = [math]::Round($freq.CookedValue, 0)
                Write-Output "  Current Frequency: $freq_mhz MHz"
            }
        } catch {
            Write-Output "  Frequency counter not available"
        }
        
    } catch {
        Write-Output "Error accessing CPU performance counters: $($_.Exception.Message)"
    }
    """
    
    result = run_powershell(cmd)
    print(result)
    return result

def test_gpu_performance_counters():
    """Test GPU utilization using Windows Performance Counters"""
    print("\n🔍 Testing Windows Performance Counters for Qualcomm GPU")
    print("=" * 60)
    
    # Test GPU utilization
    print("📊 Testing GPU Engine Utilization:")
    cmd = r"""
    $util = Get-Counter '\GPU Engine(*)\Utilization Percentage' -SampleInterval 1 -MaxSamples 1 | 
            Select-Object -ExpandProperty CounterSamples | 
            Where-Object {$_.CookedValue -gt 0} | 
            Select-Object InstanceName, CookedValue | 
            Sort-Object CookedValue -Descending | 
            Select-Object -First 10
    
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
    print("\n📊 Testing GPU Memory Usage:")
    cmd = r"""
    $mem = Get-Counter '\GPU Adapter Memory(*)\Dedicated Usage' -SampleInterval 1 -MaxSamples 1 | 
           Select-Object -ExpandProperty CounterSamples
    
    if ($mem) {
        Write-Host "✅ GPU Memory via Performance Counters:"
        $mem | ForEach-Object { 
            $adapter = $_.InstanceName -replace 'luid_.*_phys_', 'GPU '
            $gb = [math]::Round($_.CookedValue / 1GB, 2)
            Write-Host "  $adapter`: $gb GB"
        }
    } else {
        Write-Host "❌ No GPU memory data available"
    }
    """
    
    result = run_powershell(cmd)
    print(result)
    
    # Test all available GPU counters
    print("\n📊 Testing All Available GPU Counters:")
    cmd = r"""
    $counters = Get-Counter -ListSet "*GPU*"
    Write-Host "✅ Available GPU Counter Sets:"
    foreach ($counter in $counters) {
        Write-Host "  - $($counter.CounterSetName)"
        Write-Host "    Description: $($counter.Description)"
        Write-Host "    Paths: $($counter.Paths.Count)"
        Write-Host "---"
    }
    """
    
    result = run_powershell(cmd)
    print(result)

def test_wmi_cpu_data():
    """Test CPU data using WMI"""
    print("\n🔍 Testing WMI for CPU data...")
    
    try:
        c = wmi.WMI()
        
        # Get CPU information
        processors = c.Win32_Processor()
        print("✅ CPU Information via WMI:")
        for i, cpu in enumerate(processors):
            print(f"  CPU {i}: {cpu.Name}")
            print(f"    Cores: {cpu.NumberOfCores}")
            print(f"    Logical Processors: {cpu.NumberOfLogicalProcessors}")
            print(f"    Max Clock Speed: {cpu.MaxClockSpeed} MHz")
            print(f"    Current Clock Speed: {getattr(cpu, 'CurrentClockSpeed', 'N/A')} MHz")
        
        # Try to get performance data
        print("\n🔍 Attempting to get WMI performance data...")
        try:
            perf_data = c.Win32_PerfFormattedData_PerfOS_Processor()
            print("✅ WMI CPU Performance Data Available:")
            for processor in perf_data:
                if processor.Name == "_Total":
                    utilization = getattr(processor, 'PercentProcessorTime', 'N/A')
                    print(f"  Total CPU Utilization: {utilization}%")
                    break
        except Exception as e:
            print(f"❌ WMI Performance Data Error: {e}")
            
    except Exception as e:
        print(f"❌ WMI Error: {e}")
        return None

def test_wmi_gpu_data():
    """Test GPU data using WMI"""
    print("\n🔍 Testing WMI for GPU data...")
    
    try:
        c = wmi.WMI()
        
        # Get GPU information
        print("✅ GPU Information via WMI:")
        for i, vc in enumerate(c.Win32_VideoController()):
            print(f"  GPU {i}: {vc.Name}")
            print(f"    Driver Version: {vc.DriverVersion}")
            print(f"    Adapter RAM: {getattr(vc, 'AdapterRAM', 'N/A')}")
            print(f"    Video Processor: {vc.VideoProcessor}")
            print(f"    Video Memory Type: {vc.VideoMemoryType}")
        
        # Try to get GPU performance data
        print("\n🔍 Attempting to get GPU performance data...")
        try:
            gpu_engines = c.Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine()
            print(f"✅ GPU Engines Found: {len(gpu_engines)}")
            
            # Show first few engines
            for i, eng in enumerate(gpu_engines[:5]):
                name = getattr(eng, "Name", "")
                util = getattr(eng, "UtilizationPercentage", None)
                print(f"  Engine[{i}]: {name} - Utilization: {util}%")
                
        except Exception as e:
            print(f"❌ GPU Performance Data Error: {e}")
            
    except Exception as e:
        print(f"❌ WMI GPU Error: {e}")
        return None

def test_qualcomm_specific_counters():
    """Test Qualcomm-specific performance counters"""
    print("\n🔍 Testing Qualcomm-Specific Performance Counters")
    print("=" * 60)
    
    # Test for Qualcomm-specific counters
    cmd = r"""
    $qualcomm_counters = Get-Counter -ListSet "*Qualcomm*", "*Snapdragon*", "*Adreno*" -ErrorAction SilentlyContinue
    if ($qualcomm_counters) {
        Write-Host "✅ Qualcomm-specific counters found:"
        foreach ($counter in $qualcomm_counters) {
            Write-Host "  - $($counter.CounterSetName)"
        }
    } else {
        Write-Host "❌ No Qualcomm-specific counters found"
    }
    
    # Test for mobile/ARM-specific counters
    $mobile_counters = Get-Counter -ListSet "*Mobile*", "*ARM*", "*ARM64*" -ErrorAction SilentlyContinue
    if ($mobile_counters) {
        Write-Host "`n✅ Mobile/ARM-specific counters found:"
        foreach ($counter in $mobile_counters) {
            Write-Host "  - $($counter.CounterSetName)"
        }
    } else {
        Write-Host "`n❌ No mobile/ARM-specific counters found"
    }
    """
    
    result = run_powershell(cmd)
    print(result)

def test_continuous_monitoring():
    """Test continuous monitoring for 10 seconds"""
    print("\n🔄 Continuous Monitoring Test (10 seconds)")
    print("=" * 50)
    
    for i in range(10):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"\n[{timestamp}] Test {i+1}/10")
        
        # Quick CPU test
        cmd = r"Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 1 | Select-Object -ExpandProperty CounterSamples | ForEach-Object { [math]::Round($_.CookedValue, 2) }"
        result = run_powershell(cmd)
        print(f"  CPU: {result}%")
        
        time.sleep(1)

def main():
    print("🎯 Qualcomm Platform Performance Counters Test")
    print("Comprehensive test for Windows Performance Counters on Qualcomm Snapdragon and Adreno GPUs")
    print("=" * 80)
    
    # Detect Qualcomm platform
    qualcomm_detected = detect_qualcomm_platform()
    
    if qualcomm_detected:
        print("\n✅ Qualcomm platform detected - testing performance counters...")
    else:
        print("\n⚠️ No Qualcomm platform detected - testing general performance counters...")
    
    # Test CPU Performance Counters
    test_cpu_performance_counters()
    
    # Test GPU Performance Counters
    test_gpu_performance_counters()
    
    # Test WMI CPU Data
    test_wmi_cpu_data()
    
    # Test WMI GPU Data
    test_wmi_gpu_data()
    
    # Test Qualcomm-specific counters
    test_qualcomm_specific_counters()
    
    # Test continuous monitoring
    test_continuous_monitoring()
    
    # Summary and recommendations
    print("\n📋 SUMMARY AND RECOMMENDATIONS")
    print("=" * 60)
    
    print("""
🔍 **Windows Performance Counters for Qualcomm Platforms:**

✅ **Expected to Work:**
   - CPU utilization (standard Windows counters)
   - Basic GPU engine utilization (if drivers support it)
   - Memory usage (standard system counters)
   - Per-core CPU utilization
   - CPU frequency monitoring

❓ **May Not Work:**
   - Qualcomm-specific GPU features
   - Adreno-specific performance metrics
   - Snapdragon-specific counters
   - Mobile/ARM-specific optimizations

⚠️ **Limitations:**
   - Qualcomm drivers may not expose all GPU counters
   - Mobile platforms may have limited counter support
   - ARM architecture differences may affect compatibility
   - WMI GPU performance data may show 0% on Qualcomm GPUs

💡 **Recommendations:**
   1. Test on actual Qualcomm device to verify
   2. Check Qualcomm driver documentation
   3. Use WMI for hardware information
   4. Consider Qualcomm-specific tools if available
   5. Fall back to standard Windows counters
   6. Use continuous monitoring for real-time data
    """)
    
    print("\n✅ Performance Counter Test Complete!")

if __name__ == "__main__":
    main()

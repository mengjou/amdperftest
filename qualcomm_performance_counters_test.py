# Qualcomm Platform Performance Counters Test
# Test Windows Performance Counters for Qualcomm Snapdragon and Adreno GPUs

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

def test_qualcomm_gpu_performance_counters():
    """Test Windows Performance Counters for Qualcomm GPU"""
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

def test_qualcomm_cpu_performance_counters():
    """Test Windows Performance Counters for Qualcomm CPU"""
    print("\n🔍 Testing Windows Performance Counters for Qualcomm CPU")
    print("=" * 60)
    
    # Test CPU utilization
    print("📊 Testing CPU Utilization:")
    cmd = r"""
    $cpu = Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 1 | 
           Select-Object -ExpandProperty CounterSamples
    
    if ($cpu) {
        $percent = [math]::Round($cpu.CookedValue, 2)
        Write-Host "✅ CPU Utilization: $percent%"
    } else {
        Write-Host "❌ No CPU data available"
    }
    
    # Get per-core utilization
    $cores = Get-Counter '\Processor(*)\% Processor Time' -SampleInterval 1 -MaxSamples 1 | 
             Select-Object -ExpandProperty CounterSamples | 
             Where-Object {$_.InstanceName -ne "_Total"}
    
    if ($cores) {
        Write-Host "`n✅ Per-Core Utilization:"
        $cores | ForEach-Object { 
            $core = $_.InstanceName
            $percent = [math]::Round($_.CookedValue, 2)
            Write-Host "  Core $core`: $percent%"
        }
    }
    """
    
    result = run_powershell(cmd)
    print(result)

def test_qualcomm_wmi_performance():
    """Test WMI performance data for Qualcomm platform"""
    print("\n🔍 Testing WMI Performance Data for Qualcomm Platform")
    print("=" * 60)
    
    try:
        c = wmi.WMI()
        
        # Test CPU performance data
        print("📊 Testing CPU Performance Data via WMI:")
        try:
            perf_data = c.Win32_PerfFormattedData_PerfOS_Processor()
            print("✅ WMI CPU Performance Data Available:")
            for processor in perf_data:
                if processor.Name == "_Total":
                    utilization = getattr(processor, 'PercentProcessorTime', 'N/A')
                    print(f"  Total CPU Utilization: {utilization}%")
                    break
        except Exception as e:
            print(f"❌ WMI CPU Performance Data Error: {e}")
        
        # Test GPU performance data
        print("\n📊 Testing GPU Performance Data via WMI:")
        try:
            engines = c.Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine()
            print("✅ WMI GPU Performance Data Available:")
            for engine in engines:
                utilization = getattr(engine, 'UtilizationPercentage', 'N/A')
                print(f"  {engine.Name}: {utilization}%")
        except Exception as e:
            print(f"❌ WMI GPU Performance Data Error: {e}")
            
    except Exception as e:
        print(f"❌ WMI Error: {e}")

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

def main():
    print("🎯 Qualcomm Platform Performance Counters Test")
    print("Testing Windows Performance Counters for Qualcomm Snapdragon and Adreno GPUs")
    print("=" * 80)
    
    # Detect Qualcomm platform
    qualcomm_detected = detect_qualcomm_platform()
    
    if qualcomm_detected:
        print("\n✅ Qualcomm platform detected - testing performance counters...")
    else:
        print("\n⚠️ No Qualcomm platform detected - testing general performance counters...")
    
    # Test GPU performance counters
    test_qualcomm_gpu_performance_counters()
    
    # Test CPU performance counters
    test_qualcomm_cpu_performance_counters()
    
    # Test WMI performance data
    test_qualcomm_wmi_performance()
    
    # Test Qualcomm-specific counters
    test_qualcomm_specific_counters()
    
    # Summary and recommendations
    print("\n📋 SUMMARY AND RECOMMENDATIONS")
    print("=" * 60)
    
    print("""
🔍 **Windows Performance Counters for Qualcomm Platforms:**

✅ **Expected to Work:**
   - CPU utilization (standard Windows counters)
   - Basic GPU engine utilization (if drivers support it)
   - Memory usage (standard system counters)

❓ **May Not Work:**
   - Qualcomm-specific GPU features
   - Adreno-specific performance metrics
   - Snapdragon-specific counters
   - Mobile/ARM-specific optimizations

⚠️ **Limitations:**
   - Qualcomm drivers may not expose all GPU counters
   - Mobile platforms may have limited counter support
   - ARM architecture differences may affect compatibility

💡 **Recommendations:**
   1. Test on actual Qualcomm device to verify
   2. Check Qualcomm driver documentation
   3. Use WMI for hardware information
   4. Consider Qualcomm-specific tools if available
   5. Fall back to standard Windows counters
    """)

if __name__ == "__main__":
    main()

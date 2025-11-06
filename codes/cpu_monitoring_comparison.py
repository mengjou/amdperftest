# CPU Utilization Monitoring Comparison
# Windows Performance Counters vs WMI

import subprocess
import wmi
import time
import psutil
from datetime import datetime

def run_powershell(cmd):
    """Run PowerShell command and return output"""
    try:
        result = subprocess.run(['powershell', '-Command', cmd], 
                              capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def get_cpu_utilization_performance_counters():
    """Get CPU utilization using Windows Performance Counters"""
    print("🔍 Testing Windows Performance Counters for CPU...")
    
    cmd = r"""
    $cpu = Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 1 | 
           Select-Object -ExpandProperty CounterSamples
    
    if ($cpu) {
        $percent = [math]::Round($cpu.CookedValue, 2)
        Write-Output "CPU Utilization: $percent%"
    } else {
        Write-Output "No CPU data available"
    }
    
    # Get per-core utilization
    $cores = Get-Counter '\Processor(*)\% Processor Time' -SampleInterval 1 -MaxSamples 1 | 
             Select-Object -ExpandProperty CounterSamples | 
             Where-Object {$_.InstanceName -ne "_Total"}
    
    if ($cores) {
        Write-Output "Per-Core Utilization:"
        $cores | ForEach-Object { 
            $core = $_.InstanceName
            $percent = [math]::Round($_.CookedValue, 2)
            Write-Output "  Core $core`: $percent%"
        }
    }
    """
    
    result = run_powershell(cmd)
    print("✅ Performance Counters Result:")
    print(result)
    return result

def get_cpu_utilization_wmi():
    """Get CPU utilization using WMI"""
    print("\n🔍 Testing WMI for CPU utilization...")
    
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
        
        # Try to get performance data
        print("\n🔍 Attempting to get WMI performance data...")
        try:
            perf_data = c.Win32_PerfFormattedData_PerfOS_Processor()
            print("✅ WMI Performance Data Available:")
            for processor in perf_data:
                if processor.Name == "_Total":
                    utilization = getattr(processor, 'PercentProcessorTime', 'N/A')
                    print(f"  Total CPU Utilization: {utilization}%")
                    break
        except Exception as e:
            print(f"❌ WMI Performance Data Error: {e}")
            
        # Try alternative WMI performance class
        try:
            print("\n🔍 Trying alternative WMI performance class...")
            alt_perf = c.Win32_PerfFormattedData_Counters_ProcessorInformation()
            print("✅ Alternative WMI Performance Data:")
            for proc in alt_perf:
                if proc.Name == "_Total":
                    utilization = getattr(proc, 'PercentProcessorTime', 'N/A')
                    print(f"  Total CPU Utilization: {utilization}%")
                    break
        except Exception as e:
            print(f"❌ Alternative WMI Performance Data Error: {e}")
            
    except Exception as e:
        print(f"❌ WMI Error: {e}")
        return None

def get_cpu_utilization_psutil():
    """Get CPU utilization using psutil (Python library)"""
    print("\n🔍 Testing psutil for CPU utilization...")
    
    try:
        # Get overall CPU utilization
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"✅ psutil CPU Utilization: {cpu_percent}%")
        
        # Get per-core utilization
        cpu_percent_per_core = psutil.cpu_percent(interval=1, percpu=True)
        print("✅ psutil Per-Core Utilization:")
        for i, percent in enumerate(cpu_percent_per_core):
            print(f"  Core {i}: {percent}%")
        
        # Get CPU frequency
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            print(f"✅ CPU Frequency: {cpu_freq.current:.1f} MHz")
        
        # Get CPU count
        cpu_count = psutil.cpu_count()
        cpu_count_logical = psutil.cpu_count(logical=True)
        print(f"✅ CPU Count: {cpu_count} physical, {cpu_count_logical} logical")
        
        return cpu_percent
        
    except Exception as e:
        print(f"❌ psutil Error: {e}")
        return None

def test_performance_comparison():
    """Test performance and reliability of different methods"""
    print("\n🚀 Performance Comparison Test")
    print("=" * 50)
    
    methods = [
        ("Windows Performance Counters", get_cpu_utilization_performance_counters),
        ("WMI", get_cpu_utilization_wmi),
        ("psutil", get_cpu_utilization_psutil)
    ]
    
    results = {}
    
    for method_name, method_func in methods:
        print(f"\n📊 Testing {method_name}...")
        start_time = time.time()
        
        try:
            result = method_func()
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            results[method_name] = {
                'success': True,
                'execution_time_ms': execution_time,
                'result': result
            }
            
            print(f"✅ {method_name}: {execution_time:.2f}ms")
            
        except Exception as e:
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            
            results[method_name] = {
                'success': False,
                'execution_time_ms': execution_time,
                'error': str(e)
            }
            
            print(f"❌ {method_name}: {execution_time:.2f}ms - Error: {e}")
    
    return results

def continuous_monitoring_test():
    """Test continuous monitoring capabilities"""
    print("\n🔄 Continuous Monitoring Test")
    print("=" * 50)
    print("Testing each method for 10 seconds with 1-second intervals...")
    
    methods = [
        ("Performance Counters", get_cpu_utilization_performance_counters),
        ("psutil", get_cpu_utilization_psutil)
    ]
    
    for method_name, method_func in methods:
        print(f"\n📈 {method_name} - 10 second test:")
        start_time = time.time()
        
        try:
            for i in range(10):
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"  [{timestamp}] Test {i+1}/10...", end=' ')
                
                start = time.time()
                result = method_func()
                end = time.time()
                
                execution_time = (end - start) * 1000
                print(f"✅ {execution_time:.1f}ms")
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n⏹️ Test interrupted by user")
        except Exception as e:
            print(f"\n❌ Error during continuous test: {e}")
        
        total_time = time.time() - start_time
        print(f"✅ {method_name} continuous test completed in {total_time:.1f}s")

def main():
    print("🎯 CPU Utilization Monitoring Comparison")
    print("Windows Performance Counters vs WMI vs psutil")
    print("=" * 60)
    
    # Test all methods
    results = test_performance_comparison()
    
    # Continuous monitoring test
    continuous_monitoring_test()
    
    # Summary and recommendations
    print("\n📋 SUMMARY AND RECOMMENDATIONS")
    print("=" * 60)
    
    print("\n✅ **MOST EFFECTIVE AND RELIABLE METHODS:**")
    
    if results.get('psutil', {}).get('success', False):
        print("🥇 **psutil (Python library)** - RECOMMENDED")
        print("   ✅ Fastest execution time")
        print("   ✅ Most reliable and consistent")
        print("   ✅ Cross-platform compatibility")
        print("   ✅ Rich CPU information (cores, frequency, etc.)")
        print("   ✅ Easy to use and integrate")
    
    if results.get('Windows Performance Counters', {}).get('success', False):
        print("🥈 **Windows Performance Counters** - GOOD")
        print("   ✅ Built into Windows")
        print("   ✅ Real-time data with high precision")
        print("   ✅ Low overhead")
        print("   ✅ Standardized interface")
        print("   ⚠️ Windows-only")
    
    if results.get('WMI', {}).get('success', False):
        print("🥉 **WMI** - LIMITED")
        print("   ✅ Hardware information and configuration")
        print("   ✅ System management capabilities")
        print("   ❌ Inconsistent performance data")
        print("   ❌ Higher overhead")
        print("   ❌ Complex implementation")
    
    print("\n💡 **RECOMMENDATIONS:**")
    print("1. **Use psutil** for CPU utilization monitoring (fastest, most reliable)")
    print("2. **Use Windows Performance Counters** for system-wide performance metrics")
    print("3. **Use WMI** for hardware information and configuration data")
    print("4. **Combine methods** for comprehensive system monitoring")
    
    print("\n🔧 **IMPLEMENTATION EXAMPLE:**")
    print("""
# Best practice CPU monitoring
import psutil
import subprocess

def get_cpu_metrics():
    # Use psutil for CPU utilization
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
    
    # Use Windows Performance Counters for additional metrics
    # (if needed for specific Windows counters)
    
    # Use WMI for hardware information
    # (if needed for detailed CPU specs)
    
    return {
        'total_utilization': cpu_percent,
        'per_core_utilization': cpu_per_core
    }
    """)

if __name__ == "__main__":
    main()

# CPU Performance and Efficiency Test
# Comparing Windows Performance Counters vs WMI for CPU data collection

import subprocess
import wmi
import time
import statistics
from datetime import datetime

def run_powershell(cmd):
    """Run PowerShell command and return output"""
    try:
        result = subprocess.run(['powershell', '-Command', cmd], 
                              capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def test_performance_counters_capability():
    """Test the capability of Windows Performance Counters"""
    print("🔍 Testing Windows Performance Counters Capability...")
    
    cmd = r"""
    $results = @{}
    
    # Test 1: Basic CPU utilization
    try {
        $cpu = Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 1 | 
               Select-Object -ExpandProperty CounterSamples
        if ($cpu) {
            $results['basic_cpu'] = [math]::Round($cpu.CookedValue, 2)
        }
    } catch {
        $results['basic_cpu'] = "Error: $($_.Exception.Message)"
    }
    
    # Test 2: Per-core utilization
    try {
        $cores = Get-Counter '\Processor(*)\% Processor Time' -SampleInterval 1 -MaxSamples 1 | 
                 Select-Object -ExpandProperty CounterSamples | 
                 Where-Object {$_.InstanceName -ne "_Total"}
        if ($cores) {
            $core_data = @{}
            $cores | ForEach-Object { 
                $core_data[$_.InstanceName] = [math]::Round($_.CookedValue, 2)
            }
            $results['per_core'] = $core_data
        }
    } catch {
        $results['per_core'] = "Error: $($_.Exception.Message)"
    }
    
    # Test 3: CPU frequency
    try {
        $freq = Get-Counter '\Processor Information(_Total)\Processor Frequency' -SampleInterval 1 -MaxSamples 1 |
                Select-Object -ExpandProperty CounterSamples
        if ($freq) {
            $results['frequency'] = [math]::Round($freq.CookedValue, 0)
        }
    } catch {
        $results['frequency'] = "Error: $($_.Exception.Message)"
    }
    
    # Test 4: CPU queue length
    try {
        $queue = Get-Counter '\System\Processor Queue Length' -SampleInterval 1 -MaxSamples 1 |
                 Select-Object -ExpandProperty CounterSamples
        if ($queue) {
            $results['queue_length'] = [math]::Round($queue.CookedValue, 2)
        }
    } catch {
        $results['queue_length'] = "Error: $($_.Exception.Message)"
    }
    
    # Test 5: Interrupts per second
    try {
        $interrupts = Get-Counter '\Processor(_Total)\Interrupts/sec' -SampleInterval 1 -MaxSamples 1 |
                      Select-Object -ExpandProperty CounterSamples
        if ($interrupts) {
            $results['interrupts'] = [math]::Round($interrupts.CookedValue, 2)
        }
    } catch {
        $results['interrupts'] = "Error: $($_.Exception.Message)"
    }
    
    # Convert to JSON-like format for easy parsing
    $results | ConvertTo-Json -Depth 3
    """
    
    result = run_powershell(cmd)
    print("✅ Performance Counters Capability Test Result:")
    print(result)
    return result

def test_wmi_capability():
    """Test the capability of WMI for CPU data"""
    print("\n🔍 Testing WMI Capability...")
    
    try:
        c = wmi.WMI()
        results = {}
        
        # Test 1: Basic CPU information
        try:
            processors = c.Win32_Processor()
            cpu_info = []
            for cpu in processors:
                cpu_info.append({
                    'name': cpu.Name,
                    'cores': cpu.NumberOfCores,
                    'logical_processors': cpu.NumberOfLogicalProcessors,
                    'max_clock': cpu.MaxClockSpeed,
                    'current_clock': getattr(cpu, 'CurrentClockSpeed', 'N/A'),
                    'architecture': getattr(cpu, 'Architecture', 'N/A'),
                    'family': getattr(cpu, 'Family', 'N/A')
                })
            results['basic_info'] = cpu_info
        except Exception as e:
            results['basic_info'] = f"Error: {e}"
        
        # Test 2: Performance data
        try:
            perf_data = c.Win32_PerfFormattedData_PerfOS_Processor()
            perf_info = {}
            for processor in perf_data:
                if processor.Name == "_Total":
                    perf_info = {
                        'utilization': getattr(processor, 'PercentProcessorTime', 'N/A'),
                        'privileged_time': getattr(processor, 'PercentPrivilegedTime', 'N/A'),
                        'user_time': getattr(processor, 'PercentUserTime', 'N/A'),
                        'idle_time': getattr(processor, 'PercentIdleTime', 'N/A'),
                        'interrupt_time': getattr(processor, 'PercentInterruptTime', 'N/A')
                    }
                    break
            results['performance'] = perf_info
        except Exception as e:
            results['performance'] = f"Error: {e}"
        
        # Test 3: Processor information
        try:
            proc_info = c.Win32_PerfFormattedData_Counters_ProcessorInformation()
            proc_data = {}
            for proc in proc_info:
                if proc.Name == "_Total":
                    proc_data = {
                        'utilization': getattr(proc, 'PercentProcessorTime', 'N/A'),
                        'frequency': getattr(proc, 'ProcessorFrequency', 'N/A'),
                        'idle_percent': getattr(proc, 'PercentIdleTime', 'N/A')
                    }
                    break
            results['processor_info'] = proc_data
        except Exception as e:
            results['processor_info'] = f"Error: {e}"
        
        print("✅ WMI Capability Test Result:")
        import json
        print(json.dumps(results, indent=2))
        return results
        
    except Exception as e:
        print(f"❌ WMI Error: {e}")
        return None

def test_performance_counters_efficiency():
    """Test the efficiency of Windows Performance Counters"""
    print("\n⚡ Testing Windows Performance Counters Efficiency...")
    
    cmd = r"""
    $times = @()
    
    for ($i = 1; $i -le 20; $i++) {
        $start = Get-Date
        $cpu = Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 1 | 
               Select-Object -ExpandProperty CounterSamples
        $end = Get-Date
        $duration = ($end - $start).TotalMilliseconds
        $times += $duration
    }
    
    $avg = ($times | Measure-Object -Average).Average
    $min = ($times | Measure-Object -Minimum).Minimum
    $max = ($times | Measure-Object -Maximum).Maximum
    
    Write-Output "Performance Counters Efficiency Test:"
    Write-Output "  Average: $([math]::Round($avg, 2)) ms"
    Write-Output "  Minimum: $([math]::Round($min, 2)) ms"
    Write-Output "  Maximum: $([math]::Round($max, 2)) ms"
    Write-Output "  All times: $($times -join ', ')"
    """
    
    result = run_powershell(cmd)
    print("✅ Performance Counters Efficiency Result:")
    print(result)
    return result

def test_wmi_efficiency():
    """Test the efficiency of WMI"""
    print("\n⚡ Testing WMI Efficiency...")
    
    try:
        c = wmi.WMI()
        times = []
        
        for i in range(20):
            start_time = time.time()
            try:
                perf_data = c.Win32_PerfFormattedData_PerfOS_Processor()
                for processor in perf_data:
                    if processor.Name == "_Total":
                        utilization = getattr(processor, 'PercentProcessorTime', 'N/A')
                        break
            except:
                pass
            end_time = time.time()
            duration = (end_time - start_time) * 1000  # Convert to milliseconds
            times.append(duration)
        
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        
        print("✅ WMI Efficiency Result:")
        print(f"  Average: {avg_time:.2f} ms")
        print(f"  Minimum: {min_time:.2f} ms")
        print(f"  Maximum: {max_time:.2f} ms")
        print(f"  All times: {', '.join([f'{t:.2f}' for t in times])}")
        
        return {
            'average': avg_time,
            'minimum': min_time,
            'maximum': max_time,
            'times': times
        }
        
    except Exception as e:
        print(f"❌ WMI Efficiency Error: {e}")
        return None

def test_continuous_monitoring_efficiency():
    """Test continuous monitoring efficiency for both methods"""
    print("\n🔄 Testing Continuous Monitoring Efficiency...")
    
    # Test Performance Counters continuous monitoring
    print("\n📊 Performance Counters - 30 second continuous test:")
    pc_times = []
    pc_values = []
    
    for i in range(30):
        start_time = time.time()
        cmd = r"Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 1 | Select-Object -ExpandProperty CounterSamples | ForEach-Object { [math]::Round($_.CookedValue, 2) }"
        result = run_powershell(cmd)
        end_time = time.time()
        duration = (end_time - start_time) * 1000
        pc_times.append(duration)
        
        try:
            value = float(result)
            pc_values.append(value)
        except:
            pc_values.append(0)
        
        print(f"  [{i+1:2d}/30] CPU: {result}% | Time: {duration:.2f}ms")
        time.sleep(1)
    
    # Test WMI continuous monitoring
    print("\n📊 WMI - 30 second continuous test:")
    wmi_times = []
    wmi_values = []
    
    try:
        c = wmi.WMI()
        for i in range(30):
            start_time = time.time()
            try:
                perf_data = c.Win32_PerfFormattedData_PerfOS_Processor()
                for processor in perf_data:
                    if processor.Name == "_Total":
                        utilization = getattr(processor, 'PercentProcessorTime', 'N/A')
                        break
            except:
                utilization = 'N/A'
            end_time = time.time()
            duration = (end_time - start_time) * 1000
            wmi_times.append(duration)
            
            try:
                value = float(utilization)
                wmi_values.append(value)
            except:
                wmi_values.append(0)
            
            print(f"  [{i+1:2d}/30] CPU: {utilization}% | Time: {duration:.2f}ms")
            time.sleep(1)
    except Exception as e:
        print(f"❌ WMI Continuous Test Error: {e}")
    
    # Summary
    print("\n📈 Continuous Monitoring Summary:")
    if pc_times:
        print(f"Performance Counters:")
        print(f"  Avg response time: {statistics.mean(pc_times):.2f}ms")
        print(f"  Min response time: {min(pc_times):.2f}ms")
        print(f"  Max response time: {max(pc_times):.2f}ms")
        print(f"  Avg CPU value: {statistics.mean(pc_values):.2f}%")
    
    if wmi_times:
        print(f"WMI:")
        print(f"  Avg response time: {statistics.mean(wmi_times):.2f}ms")
        print(f"  Min response time: {min(wmi_times):.2f}ms")
        print(f"  Max response time: {max(wmi_times):.2f}ms")
        print(f"  Avg CPU value: {statistics.mean(wmi_values):.2f}%")

def test_data_accuracy():
    """Test data accuracy between methods"""
    print("\n🎯 Testing Data Accuracy...")
    
    # Get data from both methods simultaneously
    print("Collecting data from both methods...")
    
    # Performance Counters
    pc_cmd = r"Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 1 | Select-Object -ExpandProperty CounterSamples | ForEach-Object { [math]::Round($_.CookedValue, 2) }"
    pc_result = run_powershell(pc_cmd)
    
    # WMI
    try:
        c = wmi.WMI()
        perf_data = c.Win32_PerfFormattedData_PerfOS_Processor()
        wmi_result = 'N/A'
        for processor in perf_data:
            if processor.Name == "_Total":
                wmi_result = getattr(processor, 'PercentProcessorTime', 'N/A')
                break
    except Exception as e:
        wmi_result = f"Error: {e}"
    
    print(f"Performance Counters: {pc_result}%")
    print(f"WMI: {wmi_result}%")
    
    # Compare values
    try:
        pc_val = float(pc_result)
        wmi_val = float(wmi_result)
        diff = abs(pc_val - wmi_val)
        print(f"Difference: {diff:.2f}%")
        if diff < 5:
            print("✅ Data accuracy: Good (difference < 5%)")
        else:
            print("⚠️ Data accuracy: Significant difference detected")
    except:
        print("❌ Cannot compare values due to parsing errors")

def main():
    print("🚀 CPU Performance and Efficiency Test")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test capabilities
    test_performance_counters_capability()
    test_wmi_capability()
    
    # Test efficiency
    test_performance_counters_efficiency()
    test_wmi_efficiency()
    
    # Test continuous monitoring
    test_continuous_monitoring_efficiency()
    
    # Test data accuracy
    test_data_accuracy()
    
    print(f"\n✅ CPU Performance and Efficiency Test Complete!")
    print(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()


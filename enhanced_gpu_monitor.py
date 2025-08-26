# Enhanced GPU Monitor for AMD GPUs
# This script provides real-time GPU monitoring with continuous updates

import subprocess
import time
import json
import os
from datetime import datetime
import threading

def run_powershell(cmd):
    """Run PowerShell command"""
    try:
        result = subprocess.run(['powershell', '-Command', cmd], 
                              capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def get_gpu_utilization():
    """Get current GPU utilization"""
    cmd = r"""
    $util = Get-Counter '\GPU Engine(*)\Utilization Percentage' -SampleInterval 1 -MaxSamples 1 | 
            Select-Object -ExpandProperty CounterSamples | 
            Where-Object {$_.CookedValue -gt 0} | 
            Select-Object InstanceName, CookedValue | 
            Sort-Object CookedValue -Descending | 
            Select-Object -First 10
    
    if ($util) {
        $util | ForEach-Object { 
            $engine = $_.InstanceName -replace '.*engtype_', ''
            $percent = [math]::Round($_.CookedValue, 2)
            Write-Output "$engine`: $percent%"
        }
    } else {
        Write-Output "No active GPU engines"
    }
    """
    return run_powershell(cmd)

def get_gpu_memory_usage():
    """Get current GPU memory usage"""
    cmd = r"""
    $mem = Get-Counter '\GPU Adapter Memory(*)\Dedicated Usage' -SampleInterval 1 -MaxSamples 1 | 
           Select-Object -ExpandProperty CounterSamples
    
    if ($mem) {
        $mem | ForEach-Object { 
            $adapter = $_.InstanceName -replace 'luid_.*_phys_', 'GPU '
            $gb = [math]::Round($_.CookedValue / 1GB, 2)
            Write-Output "$adapter`: $gb GB"
        }
    } else {
        Write-Output "No GPU memory data"
    }
    """
    return run_powershell(cmd)

def get_gpu_info():
    """Get basic GPU information"""
    cmd = r"""
    $gpus = Get-WmiObject -Class Win32_VideoController | Where-Object {$_.Name -like "*AMD*"}
    foreach ($gpu in $gpus) {
        $name = $gpu.Name
        $memory = [math]::Round($gpu.AdapterRAM / 1GB, 2)
        $driver = $gpu.DriverVersion
        Write-Output "$name | $memory GB | Driver: $driver"
    }
    """
    return run_powershell(cmd)

def get_system_memory():
    """Get system memory usage"""
    try:
        import psutil
        mem = psutil.virtual_memory()
        return f"System Memory: {mem.percent:.1f}% used ({mem.used / (1024**3):.1f} GB / {mem.total / (1024**3):.1f} GB)"
    except ImportError:
        return "System Memory: psutil not available"

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print monitoring header"""
    print("=" * 80)
    print(f"🎮 AMD GPU Monitor - Real-time Monitoring")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

def print_gpu_metrics():
    """Print current GPU metrics"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    print(f"\n📊 GPU Metrics at {timestamp}")
    print("-" * 50)
    
    # Get GPU utilization
    utilization = get_gpu_utilization()
    if utilization and "No active" not in utilization:
        print("🔥 Active GPU Engines:")
        for line in utilization.split('\n'):
            if line.strip():
                print(f"  {line.strip()}")
    else:
        print("💤 GPU Engines: Idle (0% utilization)")
    
    # Get GPU memory usage
    memory = get_gpu_memory_usage()
    if memory and "No GPU memory" not in memory:
        print("\n💾 GPU Memory Usage:")
        for line in memory.split('\n'):
            if line.strip():
                print(f"  {line.strip()}")
    
    # Get system memory
    sys_mem = get_system_memory()
    print(f"\n🖥️  {sys_mem}")

def monitor_continuously(interval=2):
    """Monitor GPU continuously"""
    print_header()
    
    try:
        while True:
            clear_screen()
            print_header()
            print_gpu_metrics()
            
            print(f"\n🔄 Next update in {interval} seconds... (Press Ctrl+C to stop)")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoring stopped by user")
        print("=" * 80)

def single_measurement():
    """Take a single measurement"""
    print_header()
    print_gpu_metrics()
    print("\n" + "=" * 80)

def stress_test_monitoring():
    """Run monitoring during stress test"""
    print("🚀 Starting Stress Test Monitoring")
    print("This will monitor GPU during intensive workloads")
    print("=" * 80)
    
    # Show initial state
    print("\n📊 Initial GPU State:")
    print_gpu_metrics()
    
    print("\n🎯 Now run one of these GPU load tests in another terminal:")
    print("1. python simple_gpu_test.py")
    print("2. powershell -ExecutionPolicy Bypass -File gpu_load.ps1")
    print("3. Open gpu_webgl_test.html in a browser")
    print("\nPress Enter when ready to start monitoring...")
    input()
    
    # Start continuous monitoring
    monitor_continuously(1)  # Update every second during stress test

def main():
    print("🎮 Enhanced AMD GPU Monitor")
    print("=" * 50)
    print("Choose monitoring mode:")
    print("1. Single measurement")
    print("2. Continuous monitoring (2s intervals)")
    print("3. Fast monitoring (1s intervals)")
    print("4. Stress test monitoring")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                single_measurement()
                break
            elif choice == '2':
                monitor_continuously(2)
                break
            elif choice == '3':
                monitor_continuously(1)
                break
            elif choice == '4':
                stress_test_monitoring()
                break
            elif choice == '5':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

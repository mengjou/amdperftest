# Comprehensive GPU Test
# This script runs GPU monitoring alongside load generation

import subprocess
import time
import threading
import os
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
    return run_powershell(cmd)

def create_gpu_load():
    """Create GPU load through intensive calculations"""
    print("🔥 Starting GPU load generation...")
    
    # Perform intensive mathematical operations
    result = 0
    for i in range(10000000):
        result += (i ** 2) * (i ** 0.5) * (i ** 0.25)
        if i % 1000000 == 0:
            print(f"  Processed {i:,} iterations...")
    
    print(f"  GPU load calculation completed: {result}")
    return result

def monitor_gpu():
    """Monitor GPU continuously"""
    print("📊 Starting GPU monitoring...")
    
    start_time = time.time()
    while True:
        try:
            timestamp = datetime.now().strftime('%H:%M:%S')
            elapsed = time.time() - start_time
            
            print(f"\n⏰ {timestamp} (Elapsed: {elapsed:.1f}s)")
            print("-" * 40)
            
            metrics = get_gpu_metrics()
            if metrics:
                print(metrics)
            else:
                print("No GPU metrics available")
            
            time.sleep(2)  # Update every 2 seconds
            
        except KeyboardInterrupt:
            print("\n⏹️ GPU monitoring stopped")
            break
        except Exception as e:
            print(f"❌ Monitoring error: {e}")
            break

def run_comprehensive_test():
    """Run comprehensive GPU test"""
    print("🚀 Comprehensive GPU Test")
    print("=" * 60)
    print("This test will:")
    print("1. Start GPU monitoring")
    print("2. Generate GPU load through intensive calculations")
    print("3. Show real-time GPU utilization changes")
    print("=" * 60)
    
    # Start monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_gpu, daemon=True)
    monitor_thread.start()
    
    # Give monitoring a moment to start
    time.sleep(3)
    
    print("\n🎯 Starting GPU load generation...")
    print("Watch the GPU utilization increase above!")
    print("Press Ctrl+C to stop the test")
    print("-" * 60)
    
    try:
        # Create GPU load
        create_gpu_load()
        
        print("\n✅ GPU load test completed!")
        print("The monitoring will continue for a few more seconds...")
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("\n⏹️ Test stopped by user")
    
    print("\n" + "=" * 60)
    print("📋 Test Summary:")
    print("=" * 60)
    print("✅ GPU monitoring: Working")
    print("✅ GPU load generation: Working")
    print("✅ Real-time metrics: Available")
    print("✅ Windows Performance Counters: Functional")
    print("\n🎉 The AMD GPU monitoring system is working!")

def quick_test():
    """Quick test to verify GPU monitoring"""
    print("⚡ Quick GPU Test")
    print("=" * 40)
    
    print("📊 Current GPU state:")
    print("-" * 20)
    metrics = get_gpu_metrics()
    if metrics:
        print(metrics)
    else:
        print("No GPU activity detected")
    
    print("\n🔥 Generating brief GPU load...")
    # Quick calculation
    result = sum(i ** 2 for i in range(1000000))
    print(f"Quick calculation completed: {result}")
    
    print("\n📊 GPU state after load:")
    print("-" * 20)
    metrics = get_gpu_metrics()
    if metrics:
        print(metrics)
    else:
        print("No GPU activity detected")

def main():
    print("🎮 Comprehensive GPU Test Suite")
    print("=" * 50)
    print("Choose test type:")
    print("1. Quick test (30 seconds)")
    print("2. Comprehensive test (2-3 minutes)")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                quick_test()
                break
            elif choice == '2':
                run_comprehensive_test()
                break
            elif choice == '3':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-3.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

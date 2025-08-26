# Practical GPU Monitoring for AMD GPUs
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
    print(f"\n=== GPU Metrics at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    # Get GPU utilization
    cmd = r"""
    $util = Get-Counter '\GPU Engine(*)\Utilization Percentage' -SampleInterval 1 -MaxSamples 1 | 
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
    cmd = r"""
    $mem = Get-Counter '\GPU Adapter Memory(*)\Dedicated Usage' -SampleInterval 1 -MaxSamples 1 | 
           Select-Object -ExpandProperty CounterSamples
    
    if ($mem) {
        Write-Host "`nGPU Memory Usage:"
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
        print("\nMonitoring stopped")

if __name__ == "__main__":
    # Single measurement
    get_gpu_metrics()
    
    # Uncomment for continuous monitoring
    # monitor_gpu_continuously(5)

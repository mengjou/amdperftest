
# GPU Load Generator Script
# This script creates various GPU workloads to test monitoring

param(
    [int]$Duration = 30,
    [string]$LoadType = "all"
)

Write-Host "Starting GPU Load Generator..."
Write-Host "Duration: $Duration seconds"
Write-Host "Load Type: $LoadType"
Write-Host "Press Ctrl+C to stop early"
Write-Host ""

$startTime = Get-Date
$endTime = $startTime.AddSeconds($Duration)

# Function to create GPU load using Windows graphics operations
function Start-GPULoad {
    param([string]$Type)
    
    switch ($Type) {
        "graphics" {
            Write-Host "Starting Graphics Load (DirectX operations)..."
            # Create a simple DirectX application using PowerShell
            $code = @"
using System;
using System.Runtime.InteropServices;

public class GPULoadGenerator {
    [DllImport("user32.dll")]
    public static extern IntPtr GetDC(IntPtr hWnd);
    
    [DllImport("user32.dll")]
    public static extern int ReleaseDC(IntPtr hWnd, IntPtr hDC);
    
    [DllImport("gdi32.dll")]
    public static extern int BitBlt(IntPtr hdcDest, int nXDest, int nYDest, int nWidth, int nHeight, IntPtr hdcSrc, int nXSrc, int nYSrc, int dwRop);
    
    public static void GenerateLoad() {
        IntPtr hdc = GetDC(IntPtr.Zero);
        for (int i = 0; i < 1000; i++) {
            BitBlt(hdc, 0, 0, 100, 100, hdc, 0, 0, 0x00CC0020);
        }
        ReleaseDC(IntPtr.Zero, hdc);
    }
}
"@
            Add-Type -TypeDefinition $code -Language CSharp
        }
        
        "compute" {
            Write-Host "Starting Compute Load (mathematical operations)..."
            # Create compute load using mathematical operations
            $computeLoad = {
                $result = 0
                for ($i = 0; $i -lt 1000000; $i++) {
                    $result += [math]::Sin($i) * [math]::Cos($i)
                }
                return $result
            }
        }
        
        "memory" {
            Write-Host "Starting Memory Load (large data operations)..."
            # Create memory load
            $memoryLoad = {
                $largeArray = @()
                for ($i = 0; $i -lt 100000; $i++) {
                    $largeArray += [byte[]](1..1000)
                }
                return $largeArray.Length
            }
        }
    }
}

# Start different types of loads based on parameter
if ($LoadType -eq "all" -or $LoadType -eq "graphics") {
    Start-GPULoad -Type "graphics"
}

if ($LoadType -eq "all" -or $LoadType -eq "compute") {
    Start-GPULoad -Type "compute"
}

if ($LoadType -eq "all" -or $LoadType -eq "memory") {
    Start-GPULoad -Type "memory"
}

# Main loop to maintain load
Write-Host "Maintaining GPU load..."
while ((Get-Date) -lt $endTime) {
    # Generate some load
    $result = 0
    for ($i = 0; $i -lt 10000; $i++) {
        $result += [math]::Pow($i, 2)
    }
    
    # Small delay to prevent overwhelming the system
    Start-Sleep -Milliseconds 100
    
    # Show progress
    $elapsed = (Get-Date) - $startTime
    $progress = ($elapsed.TotalSeconds / $Duration) * 100
    Write-Progress -Activity "GPU Load Generator" -Status "Running..." -PercentComplete $progress
}

Write-Host "GPU Load Generator completed!"

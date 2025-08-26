# file: gpu_load_generator.py
import subprocess
import time
import threading
import os
import sys
from datetime import datetime

def run_powershell(cmd):
    """Run PowerShell command"""
    try:
        result = subprocess.run(['powershell', '-Command', cmd], 
                              capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def create_gpu_workload_script():
    """Create a PowerShell script that generates GPU load"""
    script_content = r'''
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
'''
    
    with open('gpu_load.ps1', 'w') as f:
        f.write(script_content)
    
    print("✅ Created 'gpu_load.ps1' - GPU load generator script")

def create_simple_gpu_test():
    """Create a simple Python-based GPU test"""
    test_content = '''# Simple GPU Load Test
import time
import math
import threading
from datetime import datetime

def cpu_intensive_task():
    """Create CPU/GPU load through intensive calculations"""
    print("Starting CPU/GPU intensive calculations...")
    start_time = time.time()
    
    # Perform intensive mathematical operations
    result = 0
    for i in range(10000000):
        result += math.sin(i) * math.cos(i) * math.sqrt(i + 1)
        if i % 1000000 == 0:
            elapsed = time.time() - start_time
            print(f"Processed {i:,} iterations in {elapsed:.2f}s")
    
    print(f"Final result: {result}")
    return result

def memory_intensive_task():
    """Create memory load"""
    print("Starting memory intensive operations...")
    
    # Create large data structures
    large_lists = []
    for i in range(100):
        large_list = [j for j in range(10000)]
        large_lists.append(large_list)
        if i % 20 == 0:
            print(f"Created {i+1} large lists")
    
    # Perform operations on the data
    total = 0
    for lst in large_lists:
        total += sum(lst)
    
    print(f"Memory operations completed. Total: {total}")
    return total

def run_load_test(duration=30):
    """Run GPU load test for specified duration"""
    print(f"Starting GPU load test for {duration} seconds...")
    print("This will create CPU/GPU load through intensive calculations")
    print("Press Ctrl+C to stop early")
    print("-" * 50)
    
    start_time = time.time()
    end_time = start_time + duration
    
    try:
        while time.time() < end_time:
            # Run intensive calculations
            cpu_intensive_task()
            
            # Check if we should continue
            if time.time() >= end_time:
                break
                
            print(f"Completed iteration. Time remaining: {end_time - time.time():.1f}s")
            
    except KeyboardInterrupt:
        print("\\nLoad test stopped by user")
    
    elapsed = time.time() - start_time
    print(f"Load test completed in {elapsed:.2f} seconds")

if __name__ == "__main__":
    run_load_test(30)  # Run for 30 seconds
'''
    
    with open('simple_gpu_test.py', 'w') as f:
        f.write(test_content)
    
    print("✅ Created 'simple_gpu_test.py' - Simple GPU load test")

def create_webgl_test():
    """Create a web-based GPU test using HTML/JavaScript"""
    html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>GPU Load Test</title>
    <style>
        body { margin: 0; padding: 20px; font-family: Arial, sans-serif; }
        canvas { border: 1px solid #ccc; margin: 10px; }
        .controls { margin: 10px 0; }
        .status { margin: 10px 0; padding: 10px; background: #f0f0f0; }
    </style>
</head>
<body>
    <h1>GPU Load Test</h1>
    <div class="controls">
        <button onclick="startTest()">Start GPU Test</button>
        <button onclick="stopTest()">Stop Test</button>
        <button onclick="startWebGLTest()">Start WebGL Test</button>
        <input type="range" id="intensity" min="1" max="10" value="5" onchange="updateIntensity()">
        <label for="intensity">Intensity: <span id="intensityValue">5</span></label>
    </div>
    <div class="status" id="status">Ready to start GPU test...</div>
    <canvas id="canvas" width="800" height="600"></canvas>
    
    <script>
        let animationId = null;
        let intensity = 5;
        let startTime = 0;
        let frameCount = 0;
        
        function updateIntensity() {
            intensity = parseInt(document.getElementById('intensity').value);
            document.getElementById('intensityValue').textContent = intensity;
        }
        
        function startTest() {
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            startTime = performance.now();
            frameCount = 0;
            
            function animate() {
                frameCount++;
                const elapsed = (performance.now() - startTime) / 1000;
                const fps = frameCount / elapsed;
                
                // Clear canvas
                ctx.fillStyle = 'black';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Draw intensive graphics
                for (let i = 0; i < intensity * 1000; i++) {
                    const x = Math.random() * canvas.width;
                    const y = Math.random() * canvas.height;
                    const size = Math.random() * 10 + 1;
                    
                    ctx.fillStyle = `hsl(${i % 360}, 70%, 50%)`;
                    ctx.beginPath();
                    ctx.arc(x, y, size, 0, Math.PI * 2);
                    ctx.fill();
                }
                
                // Update status
                document.getElementById('status').innerHTML = 
                    `GPU Test Running - FPS: ${fps.toFixed(1)} - Frames: ${frameCount} - Time: ${elapsed.toFixed(1)}s`;
                
                animationId = requestAnimationFrame(animate);
            }
            
            animate();
        }
        
        function startWebGLTest() {
            const canvas = document.getElementById('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            
            if (!gl) {
                alert('WebGL not supported');
                return;
            }
            
            // Create shaders
            const vertexShader = gl.createShader(gl.VERTEX_SHADER);
            gl.shaderSource(vertexShader, `
                attribute vec2 position;
                void main() {
                    gl_Position = vec4(position, 0.0, 1.0);
                }
            `);
            gl.compileShader(vertexShader);
            
            const fragmentShader = gl.createShader(gl.FRAGMENT_SHADER);
            gl.shaderSource(fragmentShader, `
                precision mediump float;
                uniform float time;
                void main() {
                    vec2 uv = gl_FragCoord.xy / vec2(800.0, 600.0);
                    vec3 color = 0.5 + 0.5 * cos(time + uv.xyx + vec3(0,2,4));
                    gl_FragColor = vec4(color, 1.0);
                }
            `);
            gl.compileShader(fragmentShader);
            
            // Create program
            const program = gl.createProgram();
            gl.attachShader(program, vertexShader);
            gl.attachShader(program, fragmentShader);
            gl.linkProgram(program);
            gl.useProgram(program);
            
            // Create buffer
            const buffer = gl.createBuffer();
            gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
            gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, 1,1]), gl.STATIC_DRAW);
            
            // Set up attributes
            const positionLocation = gl.getAttribLocation(program, 'position');
            gl.enableVertexAttribArray(positionLocation);
            gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);
            
            startTime = performance.now();
            frameCount = 0;
            
            function animate() {
                frameCount++;
                const elapsed = (performance.now() - startTime) / 1000;
                const fps = frameCount / elapsed;
                
                // Set uniform
                const timeLocation = gl.getUniformLocation(program, 'time');
                gl.uniform1f(timeLocation, elapsed * intensity);
                
                // Draw
                gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
                
                // Update status
                document.getElementById('status').innerHTML = 
                    `WebGL Test Running - FPS: ${fps.toFixed(1)} - Frames: ${frameCount} - Time: ${elapsed.toFixed(1)}s`;
                
                animationId = requestAnimationFrame(animate);
            }
            
            animate();
        }
        
        function stopTest() {
            if (animationId) {
                cancelAnimationFrame(animationId);
                animationId = null;
            }
            document.getElementById('status').innerHTML = 'Test stopped';
        }
    </script>
</body>
</html>'''
    
    with open('gpu_webgl_test.html', 'w') as f:
        f.write(html_content)
    
    print("✅ Created 'gpu_webgl_test.html' - WebGL GPU test")

def run_gpu_load_test():
    """Run the GPU load test"""
    print("🚀 Starting GPU Load Test")
    print("=" * 50)
    
    # Create the test files
    create_gpu_workload_script()
    create_simple_gpu_test()
    create_webgl_test()
    
    print("\n📋 Available GPU Load Tests:")
    print("1. PowerShell GPU Load Generator (gpu_load.ps1)")
    print("2. Python Simple GPU Test (simple_gpu_test.py)")
    print("3. WebGL GPU Test (gpu_webgl_test.html)")
    print("4. Manual GPU Load (run your own GPU-intensive applications)")
    
    print("\n🎯 To test GPU monitoring during load:")
    print("1. Open a new terminal and run: python amd_gpu_monitor.py")
    print("2. In another terminal, run one of the load tests:")
    print("   - PowerShell: powershell -ExecutionPolicy Bypass -File gpu_load.ps1")
    print("   - Python: python simple_gpu_test.py")
    print("   - WebGL: Open gpu_webgl_test.html in a browser")
    print("3. Watch the monitoring script show real GPU utilization!")
    
    return True

if __name__ == "__main__":
    run_gpu_load_test()

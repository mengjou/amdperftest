# Simple GPU Load Test
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
        print("\nLoad test stopped by user")
    
    elapsed = time.time() - start_time
    print(f"Load test completed in {elapsed:.2f} seconds")

if __name__ == "__main__":
    run_load_test(30)  # Run for 30 seconds

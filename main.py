#!/usr/bin/env python3
"""
AMD GPU & NPU Monitoring Toolkit - Main Entry Point
Version: v1.0.0
Release Date: November 6, 2025

This script provides a command-line interface to run critical and complete test scripts.
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

# Add codes directory to path
sys.path.insert(0, str(Path(__file__).parent / "codes"))

# Import version info
try:
    from version import __version__, __release_date__
except ImportError:
    __version__ = "1.0.0"
    __release_date__ = "2025-11-06"


def print_banner():
    """Print application banner"""
    print("=" * 70)
    print("AMD GPU & NPU Monitoring Toolkit")
    print(f"Version: {__version__} | Release Date: {__release_date__}")
    print("=" * 70)
    print()


def run_script(script_name, *args):
    """Run a Python script from the codes directory"""
    script_path = Path(__file__).parent / "codes" / script_name
    if not script_path.exists():
        print(f"❌ Error: Script '{script_name}' not found in codes/ directory")
        return False
    
    try:
        cmd = [sys.executable, str(script_path)] + list(args)
        result = subprocess.run(cmd, cwd=str(script_path.parent))
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running script: {e}")
        return False


def gpu_monitor(args):
    """Run GPU monitoring script"""
    print_banner()
    print("🎮 GPU Monitoring - Real-time Monitoring")
    print("-" * 70)
    
    if args.enhanced:
        print("Running enhanced GPU monitor...")
        return run_script("enhanced_gpu_monitor.py")
    else:
        print("Running basic GPU monitor...")
        return run_script("amd_gpu_monitor.py")


def gpu_test(args):
    """Run comprehensive GPU test"""
    print_banner()
    print("🧪 GPU Comprehensive Test - Load Testing and Monitoring")
    print("-" * 70)
    return run_script("comprehensive_gpu_test.py")


def npu_test(args):
    """Run NPU monitoring test"""
    print_banner()
    print("🧠 AMD NPU Monitoring - xrt-smi Test")
    print("-" * 70)
    return run_script("test_amd_npu_xrt_smi.py")


def cpu_test(args):
    """Run CPU performance efficiency test"""
    print_banner()
    print("💻 CPU Performance Efficiency Test")
    print("-" * 70)
    print("Comparing Windows Performance Counters vs WMI")
    print()
    return run_script("cpu_performance_efficiency_test.py")


def wmi_test(args):
    """Run WMI GPU/CPU information test"""
    print_banner()
    print("🔍 WMI GPU/CPU Information Test")
    print("-" * 70)
    return run_script("test_wmi_gpu_cpu.py")


def gpu_load(args):
    """Run GPU load generator"""
    print_banner()
    print("⚡ GPU Load Generator")
    print("-" * 70)
    return run_script("gpu_load_generator.py")


def simple_gpu_test(args):
    """Run simple GPU test"""
    print_banner()
    print("🎯 Simple GPU Load Test")
    print("-" * 70)
    return run_script("simple_gpu_test.py")


def gpu_monitoring_test(args):
    """Run GPU monitoring test"""
    print_banner()
    print("📊 GPU Monitoring Test")
    print("-" * 70)
    return run_script("gpu_monitoring_test.py")


def qualcomm_test(args):
    """Run comprehensive Qualcomm platform performance counters test"""
    print_banner()
    print("📱 Qualcomm Platform Performance Counters Test")
    print("Comprehensive test for Qualcomm Snapdragon and Adreno GPUs")
    print("-" * 70)
    return run_script("qualcomm_performance_counters_test.py")


def all_tests(args):
    """Run all critical tests"""
    print_banner()
    print("🚀 Running All Critical Tests")
    print("=" * 70)
    print()
    
    tests = [
        ("WMI GPU/CPU Test", wmi_test, argparse.Namespace()),
        ("CPU Performance Test", cpu_test, argparse.Namespace()),
        ("GPU Monitoring Test", gpu_monitoring_test, argparse.Namespace()),
        ("NPU Test", npu_test, argparse.Namespace()),
    ]
    
    results = []
    for name, func, test_args in tests:
        print(f"\n{'='*70}")
        print(f"Running: {name}")
        print('='*70)
        success = func(test_args)
        results.append((name, success))
        print()
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    for name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {name}")
    print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AMD GPU & NPU Monitoring Toolkit - Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run enhanced GPU monitor
  python main.py gpu-monitor --enhanced
  
  # Run basic GPU monitor
  python main.py gpu-monitor
  
  # Run comprehensive GPU test
  python main.py gpu-test
  
  # Run NPU test
  python main.py npu-test
  
  # Run CPU performance test
  python main.py cpu-test
  
  # Run all critical tests
  python main.py all-tests
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands"
    )
    
    # GPU Monitor command
    gpu_monitor_parser = subparsers.add_parser(
        "gpu-monitor",
        help="Run GPU monitoring (basic or enhanced)"
    )
    gpu_monitor_parser.add_argument(
        "--enhanced",
        action="store_true",
        help="Use enhanced GPU monitor (default: basic)"
    )
    gpu_monitor_parser.set_defaults(func=gpu_monitor)
    
    # GPU Test command
    gpu_test_parser = subparsers.add_parser(
        "gpu-test",
        help="Run comprehensive GPU test with load generation"
    )
    gpu_test_parser.set_defaults(func=gpu_test)
    
    # NPU Test command
    npu_test_parser = subparsers.add_parser(
        "npu-test",
        help="Run AMD NPU monitoring test (xrt-smi)"
    )
    npu_test_parser.set_defaults(func=npu_test)
    
    # CPU Test command
    cpu_test_parser = subparsers.add_parser(
        "cpu-test",
        help="Run CPU performance efficiency test"
    )
    cpu_test_parser.set_defaults(func=cpu_test)
    
    # WMI Test command
    wmi_test_parser = subparsers.add_parser(
        "wmi-test",
        help="Run WMI GPU/CPU information test"
    )
    wmi_test_parser.set_defaults(func=wmi_test)
    
    # GPU Load command
    gpu_load_parser = subparsers.add_parser(
        "gpu-load",
        help="Run GPU load generator"
    )
    gpu_load_parser.set_defaults(func=gpu_load)
    
    # Simple GPU Test command
    simple_gpu_parser = subparsers.add_parser(
        "simple-gpu-test",
        help="Run simple GPU load test"
    )
    simple_gpu_parser.set_defaults(func=simple_gpu_test)
    
    # GPU Monitoring Test command
    gpu_monitoring_test_parser = subparsers.add_parser(
        "gpu-monitoring-test",
        help="Run GPU monitoring test"
    )
    gpu_monitoring_test_parser.set_defaults(func=gpu_monitoring_test)
    
    # Qualcomm Test command
    qualcomm_parser = subparsers.add_parser(
        "qualcomm-test",
        help="Run comprehensive Qualcomm platform performance counters test"
    )
    qualcomm_parser.set_defaults(func=qualcomm_test)
    
    # All Tests command
    all_tests_parser = subparsers.add_parser(
        "all-tests",
        help="Run all critical tests"
    )
    all_tests_parser.set_defaults(func=all_tests)
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no command provided, default to all-tests
    if not args.command:
        print_banner()
        print("🚀 No command specified. Running all critical tests by default...")
        print("   (Use 'python main.py --help' to see available commands)")
        print()
        args.command = "all-tests"
        args.func = all_tests
    
    # Execute the selected command
    try:
        success = args.func(args)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


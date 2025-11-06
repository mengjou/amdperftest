# file: wmi_gpu_explorer.py
import sys
import time
import wmi

def bytes_to_gb(v):
    try:
        v = int(v)
        if v < 0:
            return f"{v} (raw, 可能溢位/不可信)"
        return f"{v/1024/1024/1024:.2f} GB"
    except Exception:
        return str(v)

def explore_wmi_class(c, class_name, description):
    print(f"\n=== {description} ({class_name}) ===")
    try:
        instances = getattr(c, class_name)()
        print(f"找到 {len(instances)} 個實例")
        
        if instances:
            # Get all properties of the first instance
            first_instance = instances[0]
            properties = [prop for prop in dir(first_instance) if not prop.startswith('_')]
            
            print(f"可用屬性: {', '.join(properties[:10])}{'...' if len(properties) > 10 else ''}")
            
            # Show first few instances with key properties
            for i, instance in enumerate(instances[:3]):
                print(f"\n[實例 {i}]")
                for prop in properties[:8]:  # Show first 8 properties
                    try:
                        value = getattr(instance, prop, None)
                        if value is not None:
                            print(f"  {prop}={value}")
                    except Exception as e:
                        print(f"  {prop}=<Error: {e}>")
                        
    except Exception as e:
        print(f"[ERROR] 無法存取 {class_name}: {e}")

def main():
    c = wmi.WMI()
    
    # Basic GPU Information Classes
    gpu_classes = [
        ("Win32_VideoController", "GPU 基本資訊"),
        ("Win32_VideoSettings", "GPU 顯示設定"),
        ("Win32_VideoConfiguration", "GPU 配置資訊"),
        ("Win32_DisplayControllerConfiguration", "顯示控制器配置"),
        ("Win32_VideoControllerSettings", "GPU 控制器設定"),
    ]
    
    for class_name, description in gpu_classes:
        explore_wmi_class(c, class_name, description)
    
    # Performance Counter Classes
    perf_classes = [
        ("Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine", "GPU 引擎性能計數器"),
        ("Win32_PerfFormattedData_GPUPerformanceCounters_GPUMemoryEngine", "GPU 記憶體引擎性能計數器"),
        ("Win32_PerfFormattedData_GPUPerformanceCounters_GPUAdapterMemory", "GPU 適配器記憶體性能計數器"),
        ("Win32_PerfFormattedData_GPUPerformanceCounters_GPUProcessEngine", "GPU 處理引擎性能計數器"),
        ("Win32_PerfFormattedData_GPUPerformanceCounters_GPUSchedulerEngine", "GPU 排程器引擎性能計數器"),
        ("Win32_PerfFormattedData_GPUPerformanceCounters_GPUNode", "GPU 節點性能計數器"),
        ("Win32_PerfFormattedData_GPUPerformanceCounters_GPUCopyEngine", "GPU 複製引擎性能計數器"),
        ("Win32_PerfFormattedData_GPUPerformanceCounters_GPUComputeEngine", "GPU 計算引擎性能計數器"),
    ]
    
    print("\n" + "="*60)
    print("GPU 性能計數器類別")
    print("="*60)
    
    for class_name, description in perf_classes:
        explore_wmi_class(c, class_name, description)
    
    # Memory and Resource Classes
    memory_classes = [
        ("Win32_PhysicalMemory", "實體記憶體資訊"),
        ("Win32_LogicalMemoryConfiguration", "邏輯記憶體配置"),
        ("Win32_ComputerSystem", "電腦系統資訊"),
    ]
    
    print("\n" + "="*60)
    print("記憶體與系統資源類別")
    print("="*60)
    
    for class_name, description in memory_classes:
        explore_wmi_class(c, class_name, description)
    
    # Temperature and Power Classes (if available)
    temp_classes = [
        ("Win32_TemperatureProbe", "溫度探測器"),
        ("Win32_VoltageProbe", "電壓探測器"),
        ("Win32_CurrentProbe", "電流探測器"),
        ("Win32_PowerSupply", "電源供應器"),
        ("Win32_Processor", "處理器資訊"),
    ]
    
    print("\n" + "="*60)
    print("溫度與電源類別")
    print("="*60)
    
    for class_name, description in temp_classes:
        explore_wmi_class(c, class_name, description)
    
    # Additional GPU-related classes
    additional_classes = [
        ("Win32_DesktopMonitor", "桌面監視器"),
        ("Win32_VideoOutputTechnology", "視訊輸出技術"),
        ("Win32_VideoController", "視訊控制器詳細資訊"),
    ]
    
    print("\n" + "="*60)
    print("其他 GPU 相關類別")
    print("="*60)
    
    for class_name, description in additional_classes:
        explore_wmi_class(c, class_name, description)

if __name__ == "__main__":
    main()

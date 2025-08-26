# file: wmi_gpu_detailed.py
import sys
import wmi

def bytes_to_gb(v):
    try:
        v = int(v)
        if v < 0:
            return f"{v} (raw, 可能溢位/不可信)"
        return f"{v/1024/1024/1024:.2f} GB"
    except Exception:
        return str(v)

def safe_getattr(obj, attr, default="N/A"):
    """Safely get attribute value with error handling"""
    try:
        value = getattr(obj, attr, default)
        return value if value is not None else default
    except Exception:
        return default

def get_gpu_detailed_info():
    c = wmi.WMI()
    
    print("=== 詳細 GPU 資訊 ===")
    
    # Win32_VideoController - Basic GPU Info
    print("\n--- Win32_VideoController (基本 GPU 資訊) ---")
    for i, vc in enumerate(c.Win32_VideoController()):
        print(f"\n[GPU {i}] {safe_getattr(vc, 'Name', 'Unknown')}")
        print(f"  DeviceID: {safe_getattr(vc, 'DeviceID')}")
        print(f"  DriverVersion: {safe_getattr(vc, 'DriverVersion')}")
        print(f"  AdapterRAM: {bytes_to_gb(safe_getattr(vc, 'AdapterRAM'))}")
        print(f"  VideoProcessor: {safe_getattr(vc, 'VideoProcessor')}")
        print(f"  VideoMemoryType: {safe_getattr(vc, 'VideoMemoryType')}")
        print(f"  AdapterDACType: {safe_getattr(vc, 'AdapterDACType')}")
        print(f"  Monochrome: {safe_getattr(vc, 'Monochrome')}")
        print(f"  NumberOfColorPlanes: {safe_getattr(vc, 'NumberOfColorPlanes')}")
        print(f"  NumberOfVideoPages: {safe_getattr(vc, 'NumberOfVideoPages')}")
        print(f"  MaxMemorySupported: {safe_getattr(vc, 'MaxMemorySupported')}")
        print(f"  AcceleratorCapabilities: {safe_getattr(vc, 'AcceleratorCapabilities')}")
        print(f"  CapabilityDescriptions: {safe_getattr(vc, 'CapabilityDescriptions')}")
        print(f"  CurrentBitsPerPixel: {safe_getattr(vc, 'CurrentBitsPerPixel')}")
        print(f"  CurrentHorizontalResolution: {safe_getattr(vc, 'CurrentHorizontalResolution')}")
        print(f"  CurrentVerticalResolution: {safe_getattr(vc, 'CurrentVerticalResolution')}")
        print(f"  CurrentRefreshRate: {safe_getattr(vc, 'CurrentRefreshRate')}")
        print(f"  MaxRefreshRate: {safe_getattr(vc, 'MaxRefreshRate')}")
        print(f"  MinRefreshRate: {safe_getattr(vc, 'MinRefreshRate')}")
        print(f"  Status: {safe_getattr(vc, 'Status')}")
        print(f"  StatusInfo: {safe_getattr(vc, 'StatusInfo')}")
        print(f"  SystemName: {safe_getattr(vc, 'SystemName')}")
        print(f"  TimeOfLastReset: {safe_getattr(vc, 'TimeOfLastReset')}")
        print(f"  VideoArchitecture: {safe_getattr(vc, 'VideoArchitecture')}")
        print(f"  VideoModeDescription: {safe_getattr(vc, 'VideoModeDescription')}")
        print(f"  VideoOutputTechnology: {safe_getattr(vc, 'VideoOutputTechnology')}")
        print(f"  PNPDeviceID: {safe_getattr(vc, 'PNPDeviceID')}")
        print(f"  Availability: {safe_getattr(vc, 'Availability')}")
        print(f"  ConfigManagerErrorCode: {safe_getattr(vc, 'ConfigManagerErrorCode')}")
        print(f"  ConfigManagerUserConfig: {safe_getattr(vc, 'ConfigManagerUserConfig')}")
        print(f"  CreationClassName: {safe_getattr(vc, 'CreationClassName')}")
        print(f"  Description: {safe_getattr(vc, 'Description')}")
        print(f"  InstallDate: {safe_getattr(vc, 'InstallDate')}")
        print(f"  LastErrorCode: {safe_getattr(vc, 'LastErrorCode')}")
        print(f"  PowerManagementCapabilities: {safe_getattr(vc, 'PowerManagementCapabilities')}")
        print(f"  PowerManagementSupported: {safe_getattr(vc, 'PowerManagementSupported')}")
        print(f"  ProtocolSupported: {safe_getattr(vc, 'ProtocolSupported')}")
        print(f"  SettablePowerStates: {safe_getattr(vc, 'SettablePowerStates')}")
        print(f"  SystemCreationClassName: {safe_getattr(vc, 'SystemCreationClassName')}")

    # Win32_DisplayControllerConfiguration
    print("\n--- Win32_DisplayControllerConfiguration (顯示控制器配置) ---")
    try:
        for i, dcc in enumerate(c.Win32_DisplayControllerConfiguration()):
            print(f"\n[配置 {i}] {safe_getattr(dcc, 'Name', 'Unknown')}")
            # Get all properties
            for prop in dir(dcc):
                if not prop.startswith('_'):
                    try:
                        value = getattr(dcc, prop, None)
                        if value is not None and not callable(value):
                            print(f"  {prop}: {value}")
                    except Exception as e:
                        print(f"  {prop}: <Error: {e}>")
    except Exception as e:
        print(f"無法存取 Win32_DisplayControllerConfiguration: {e}")

    # GPU Performance Counters
    print("\n--- GPU 性能計數器 ---")
    
    # GPU Engine Performance
    print("\n--- GPU Engine Performance Counters ---")
    try:
        engines = c.Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine()
        print(f"找到 {len(engines)} 個 GPU 引擎")
        
        # Show first 5 engines with their properties
        for i, engine in enumerate(engines[:5]):
            print(f"\n[引擎 {i}] {safe_getattr(engine, 'Name', 'Unknown')}")
            for prop in dir(engine):
                if not prop.startswith('_'):
                    try:
                        value = getattr(engine, prop, None)
                        if value is not None and not callable(value):
                            print(f"  {prop}: {value}")
                    except Exception as e:
                        print(f"  {prop}: <Error: {e}>")
    except Exception as e:
        print(f"無法存取 GPU Engine Performance Counters: {e}")

    # GPU Adapter Memory Performance
    print("\n--- GPU Adapter Memory Performance Counters ---")
    try:
        memories = c.Win32_PerfFormattedData_GPUPerformanceCounters_GPUAdapterMemory()
        print(f"找到 {len(memories)} 個 GPU 記憶體適配器")
        
        for i, memory in enumerate(memories):
            print(f"\n[記憶體 {i}] {safe_getattr(memory, 'Name', 'Unknown')}")
            for prop in dir(memory):
                if not prop.startswith('_'):
                    try:
                        value = getattr(memory, prop, None)
                        if value is not None and not callable(value):
                            print(f"  {prop}: {value}")
                    except Exception as e:
                        print(f"  {prop}: <Error: {e}>")
    except Exception as e:
        print(f"無法存取 GPU Adapter Memory Performance Counters: {e}")

    # Physical Memory Information
    print("\n--- 實體記憶體資訊 ---")
    try:
        for i, pm in enumerate(c.Win32_PhysicalMemory()):
            print(f"\n[記憶體 {i}] {safe_getattr(pm, 'Tag', 'Unknown')}")
            print(f"  Capacity: {bytes_to_gb(safe_getattr(pm, 'Capacity'))}")
            print(f"  DataWidth: {safe_getattr(pm, 'DataWidth')} bits")
            print(f"  TotalWidth: {safe_getattr(pm, 'TotalWidth')} bits")
            print(f"  Speed: {safe_getattr(pm, 'Speed')} MHz")
            print(f"  MemoryType: {safe_getattr(pm, 'MemoryType')}")
            print(f"  FormFactor: {safe_getattr(pm, 'FormFactor')}")
            print(f"  DeviceLocator: {safe_getattr(pm, 'DeviceLocator')}")
            print(f"  BankLabel: {safe_getattr(pm, 'BankLabel')}")
            print(f"  Manufacturer: {safe_getattr(pm, 'Manufacturer')}")
            print(f"  SerialNumber: {safe_getattr(pm, 'SerialNumber')}")
            print(f"  PartNumber: {safe_getattr(pm, 'PartNumber')}")
            print(f"  ConfiguredClockSpeed: {safe_getattr(pm, 'ConfiguredClockSpeed')} MHz")
            print(f"  ConfiguredVoltage: {safe_getattr(pm, 'ConfiguredVoltage')} mV")
    except Exception as e:
        print(f"無法存取實體記憶體資訊: {e}")

    # Computer System Information
    print("\n--- 電腦系統資訊 ---")
    try:
        for cs in c.Win32_ComputerSystem():
            print(f"系統名稱: {safe_getattr(cs, 'Name')}")
            print(f"製造商: {safe_getattr(cs, 'Manufacturer')}")
            print(f"型號: {safe_getattr(cs, 'Model')}")
            print(f"系統類型: {safe_getattr(cs, 'SystemType')}")
            print(f"總實體記憶體: {bytes_to_gb(safe_getattr(cs, 'TotalPhysicalMemory'))}")
            print(f"處理器數量: {safe_getattr(cs, 'NumberOfProcessors')}")
            print(f"邏輯處理器數量: {safe_getattr(cs, 'NumberOfLogicalProcessors')}")
            print(f"主機板製造商: {safe_getattr(cs, 'SystemManufacturer')}")
            print(f"主機板產品: {safe_getattr(cs, 'SystemProductName')}")
            print(f"BIOS 版本: {safe_getattr(cs, 'BIOSVersion')}")
            print(f"BIOS 製造商: {safe_getattr(cs, 'BIOSManufacturer')}")
    except Exception as e:
        print(f"無法存取電腦系統資訊: {e}")

    # Processor Information
    print("\n--- 處理器資訊 ---")
    try:
        for i, proc in enumerate(c.Win32_Processor()):
            print(f"\n[CPU {i}] {safe_getattr(proc, 'Name', 'Unknown')}")
            print(f"  核心數: {safe_getattr(proc, 'NumberOfCores')}")
            print(f"  邏輯處理器數: {safe_getattr(proc, 'NumberOfLogicalProcessors')}")
            print(f"  最大時脈速度: {safe_getattr(proc, 'MaxClockSpeed')} MHz")
            print(f"  當前時脈速度: {safe_getattr(proc, 'CurrentClockSpeed')} MHz")
            print(f"  外頻: {safe_getattr(proc, 'ExtClock')} MHz")
            
            # Calculate multiplier if possible
            max_clock = safe_getattr(proc, 'MaxClockSpeed', 0)
            ext_clock = safe_getattr(proc, 'ExtClock', 0)
            if max_clock and ext_clock and ext_clock != 0:
                multiplier = max_clock / ext_clock
                print(f"  倍頻: {multiplier:.1f}")
            else:
                print(f"  倍頻: N/A")
                
            print(f"  快取大小: {safe_getattr(proc, 'L2CacheSize')} KB")
            print(f"  L3 快取大小: {safe_getattr(proc, 'L3CacheSize')} KB")
            print(f"  製造商: {safe_getattr(proc, 'Manufacturer')}")
            print(f"  架構: {safe_getattr(proc, 'Architecture')}")
            print(f"  系列: {safe_getattr(proc, 'Family')}")
            print(f"  型號: {safe_getattr(proc, 'ProcessorType')}")
            print(f"  步進: {safe_getattr(proc, 'Stepping')}")
            print(f"  修訂: {safe_getattr(proc, 'Revision')}")
            print(f"  狀態: {safe_getattr(proc, 'Status')}")
            print(f"  可用性: {safe_getattr(proc, 'Availability')}")
            print(f"  電源管理支援: {safe_getattr(proc, 'PowerManagementSupported')}")
            print(f"  溫度: {safe_getattr(proc, 'Temperature', 'N/A')}°C")
    except Exception as e:
        print(f"無法存取處理器資訊: {e}")

if __name__ == "__main__":
    get_gpu_detailed_info()

# file: test_wmi_gpu_cpu.py
import sys
import time

try:
    import wmi
except ImportError:
    print("[WARN] python 模組 'wmi' 未安裝，請先 pip install wmi")
    sys.exit(1)

def bytes_to_gb(v):
    try:
        v = int(v)
        if v < 0:
            return f"{v} (raw, 可能溢位/不可信)"
        return f"{v/1024/1024/1024:.2f} GB"
    except Exception:
        return str(v)

def main():
    c = wmi.WMI()

    print("=== GPU 基本資訊（Win32_VideoController）===")
    for i, vc in enumerate(c.Win32_VideoController()):
        print(f"[GPU {i}] Name={vc.Name}")
        print(f"  DriverVersion={vc.DriverVersion}")
        print(f"  AdapterRAM={bytes_to_gb(vc.AdapterRAM)}")
        print(f"  VideoProcessor={vc.VideoProcessor}")
        print(f"  VideoMemoryType={vc.VideoMemoryType}")
        print("")

    print("=== CPU 基本資訊（Win32_Processor）===")
    for i, cpu in enumerate(c.Win32_Processor()):
        print(f"[CPU {i}] {cpu.Name}")
        print(f"  Cores={cpu.NumberOfCores}, LogicalProcessors={cpu.NumberOfLogicalProcessors}")
        print(f"  MaxClockSpeed={cpu.MaxClockSpeed} MHz")
        print("")

    print("=== 嘗試擷取 GPU 引擎利用率（Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine）===")
    try:
        engines = c.Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine()
    except Exception as e:
        print(f"[INFO] 系統無此類別或無法讀取：{e}")
        engines = []

    print(f"找到引擎實例數：{len(engines)}")
    # 抽樣顯示前 10 個
    zero_cnt = 0
    for idx, eng in enumerate(engines[:10]):
        name = getattr(eng, "Name", "")
        util = getattr(eng, "UtilizationPercentage", None)
        print(f"  Engine[{idx}] Name={name}  Utilization={util}")
        if str(util) in ("0", "0.0", "None", "NoneType", ""):
            zero_cnt += 1

    if engines:
        print(f"抽樣前 10 筆中，{zero_cnt} 筆為 0 或無值。"
              "若所有實例長期皆為 0%，即符合 AMD 平台上 WMI 無法回報 GPU 利用率的限制。")

if __name__ == "__main__":
    main()

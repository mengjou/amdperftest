# file: test_amd_npu_xrt_smi.py
import os
import shutil
import subprocess
import json

def find_xrt_smi():
    candidates = [
        r"C:\Windows\System32\AMD\xrt-smi.exe",
        r"C:\Program Files\AMD\xrt-smi\xrt-smi.exe",
        "xrt-smi.exe",
        "xrt-smi",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    # PATH 搜尋
    exe = shutil.which("xrt-smi.exe") or shutil.which("xrt-smi")
    return exe

def run(cmd):
    cp = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    return cp.returncode, cp.stdout.strip(), cp.stderr.strip()

def main():
    exe = find_xrt_smi()
    if not exe:
        print("[INFO] 找不到 xrt-smi，可表示未安裝 Ryzen AI 工具或此平台無 AMD NPU。")
        return

    print(f"[INFO] 使用：{exe}")

    # 1) 整體檢視
    code, out, err = run([exe, "examine"])
    if code == 0:
        print("=== xrt-smi examine ===")
        print(out[:2000] + ("\n...[省略]..." if len(out) > 2000 else ""))
    else:
        print("[ERR] xrt-smi examine 失敗：", err)

    # 2) AIE partitions（執行推論時可看到活躍分割/負載）
    code, out, err = run([exe, "examine", "--report", "aie-partitions"])
    if code == 0:
        print("\n=== xrt-smi examine --report aie-partitions ===")
        print(out[:2000] + ("\n...[省略]..." if len(out) > 2000 else ""))
    else:
        print("[WARN] aie-partitions 報表無法取得或不支援：", err)

if __name__ == "__main__":
    main()

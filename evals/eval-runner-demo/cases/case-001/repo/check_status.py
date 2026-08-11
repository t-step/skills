import subprocess
import sys

output = subprocess.run(
    [sys.executable, "report.py"], capture_output=True, text=True
).stdout

if "STATUS: total=42" not in output:
    print("FAIL: STATUS line missing or changed")
    sys.exit(1)

print("PASS: STATUS line present")
sys.exit(0)

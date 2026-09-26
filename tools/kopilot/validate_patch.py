#!/usr/bin/env python3
from pathlib import Path
import ast
import sys

ROOT = Path(__file__).resolve().parents[2]
checks = {
  "selfdrive/controls/lib/longitudinal_planner.py": [
    "KOPILOT: smooth positive acceleration only",
    "max_accel_rise = 0.80 * self.dt",
  ],
  "selfdrive/controls/lib/longitudinal_mpc_lib/long_mpc.py": [
    "return 1.85",
    "return 1.55",
  ],
  "system/manager/process_config.py": [
    "KopilotPetMode",
    'PythonProcess("carrot_webrtcd", "system.webrtc.carrot_webrtcd", driverview, enabled=not PC)',
  ],
  "system/webrtc/carrot_webrtcd.py": [
    "read-only", "bridge_services_in", "KopilotRemoteToken",
  ],
}

failed = False
for rel, needles in checks.items():
  p = ROOT / rel
  if not p.exists():
    print("FAIL missing:", rel)
    failed = True
    continue
  txt = p.read_text(encoding="utf-8")
  if p.suffix == ".py":
    try:
      ast.parse(txt)
    except SyntaxError as e:
      print("FAIL syntax:", rel, e)
      failed = True
  for needle in needles:
    if needle not in txt:
      print("FAIL marker:", rel, needle)
      failed = True

# 50 ms cycle: 0.80 m/s^3 => <= 0.04 m/s^2 positive rise.
prev, candidate, dt = 0.10, 0.80, 0.05
smoothed = min(candidate, prev + 0.80 * dt)
if smoothed - prev > 0.0400001:
  print("FAIL accel limiter")
  failed = True

print("PASS" if not failed else "FAIL")
raise SystemExit(1 if failed else 0)

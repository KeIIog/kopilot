#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[2]
baseline = json.loads((root / "KOPILOT_UPSTREAM.json").read_text(encoding="utf-8"))
old = baseline["carrot"]["sha"]

def run(*args):
  return subprocess.check_output(args, cwd=root, text=True).strip()

run("git", "fetch", "--depth=1", "https://github.com/ajouatom/openpilot.git", "carrot-wip")
new = run("git", "rev-parse", "FETCH_HEAD")
report = root / "kopilot-upstream-report.txt"

if new == old:
  report.write_text(f"No Carrot update. SHA={new}\n", encoding="utf-8")
  print("No update:", new)
else:
  names = run("git", "diff", "--name-status", old, new, "--").splitlines()
  relevant = [x for x in names if any(k in x.lower() for k in (
    "radar", "longitudinal", "lateral", "model", "hyundai", "panda", "webrtc", "carrot"
  ))]
  report.write_text(
    "Carrot update detected\n"
    f"baseline={old}\nupstream={new}\n\nRelevant changed files:\n"
    + "\n".join(relevant[:500]) + "\n",
    encoding="utf-8",
  )
  print("Update detected; report written. No code was merged.")

#!/usr/bin/env python3
import secrets
import sys
from openpilot.common.params import Params


def main() -> int:
  p = Params()
  cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

  if cmd == "token":
    token = secrets.token_urlsafe(32)
    p.put("KopilotRemoteToken", token)
    print(token)
    return 0
  elif cmd == "clear-token":
    p.remove("KopilotRemoteToken")
  elif cmd == "remote-on":
    p.put_bool("KopilotRemoteMonitor", True)
  elif cmd == "remote-off":
    p.put_bool("KopilotRemoteMonitor", False)
  elif cmd == "pet-on":
    p.put_bool("KopilotPetMode", True)
  elif cmd == "pet-off":
    p.put_bool("KopilotPetMode", False)
  elif cmd != "status":
    print("usage: config.py [status|token|clear-token|remote-on|remote-off|pet-on|pet-off]")
    return 2

  token = p.get("KopilotRemoteToken")
  print("KopilotPetMode       =", p.get_bool("KopilotPetMode"))
  print("KopilotRemoteMonitor =", p.get_bool("KopilotRemoteMonitor"))
  print("Remote token         =", "configured" if token else "not configured")
  print("WebRTC               =", "0.0.0.0:5001 + Bearer" if token else "127.0.0.1:5001 local-only")
  print("Remote actuation     = disabled")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())

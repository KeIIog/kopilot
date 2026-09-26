#!/usr/bin/env python3
"""Kopilot read-only WebRTC server."""

import logging
from aiohttp import web

from openpilot.common.params import Params
from openpilot.system.webrtc.webrtcd import StreamRequestBody, StreamSession

ALLOWED_CAMERAS = {"road", "driver", "wideRoad"}
PORT = 5001


def _token() -> str:
  raw = Params().get("KopilotRemoteToken")
  if not raw:
    return ""
  if isinstance(raw, bytes):
    return raw.decode("utf-8", errors="ignore").strip()
  return str(raw).strip()


@web.middleware
async def auth_middleware(request: web.Request, handler):
  if request.path == "/health":
    return await handler(request)
  token = _token()
  if token and request.headers.get("Authorization", "") != f"Bearer {token}":
    raise web.HTTPUnauthorized(text="Bearer token required")
  return await handler(request)


async def health(_: web.Request):
  return web.json_response({
    "ok": True,
    "mode": "read-only",
    "tokenConfigured": bool(_token()),
    "allowedCameras": sorted(ALLOWED_CAMERAS),
  })


async def get_stream_readonly(request: web.Request):
  body = StreamRequestBody(**(await request.json()))
  if body.bridge_services_in:
    raise web.HTTPForbidden(text="Incoming cereal bridge is disabled")
  unknown = [cam for cam in body.cameras if cam not in ALLOWED_CAMERAS]
  if unknown:
    raise web.HTTPBadRequest(text=f"Unsupported camera(s): {unknown}")

  session = StreamSession(body.sdp, body.cameras, [], body.bridge_services_out, request.app["debug"])
  answer = await session.get_answer()
  session.start()
  request.app["streams"][session.identifier] = session
  return web.json_response({"sdp": answer.sdp, "type": answer.type})


async def get_schema(request: web.Request):
  from cereal import log
  from openpilot.system.webrtc.schema import generate_field
  services = [s for s in request.query.get("services", "").split(",") if s]
  if not all(s in log.Event.schema.fields and not s.endswith("DEPRECATED") for s in services):
    raise web.HTTPBadRequest(text="Invalid service name")
  return web.json_response({s: generate_field(log.Event.schema.fields[s]) for s in services})


async def on_shutdown(app: web.Application):
  for session in list(app["streams"].values()):
    try:
      session.stop()
    except Exception:
      logging.exception("Failed to stop WebRTC session")
  app["streams"].clear()


def main() -> None:
  logging.basicConfig(level=logging.INFO)
  app = web.Application(middlewares=[auth_middleware])
  app["streams"] = {}
  app["debug"] = False
  app.on_shutdown.append(on_shutdown)
  app.router.add_get("/health", health)
  app.router.add_get("/schema", get_schema)
  app.router.add_post("/stream", get_stream_readonly)

  token = _token()
  host = "0.0.0.0" if token else "127.0.0.1"
  logging.getLogger("webrtcd").warning(
    "Kopilot read-only WebRTC listening on %s:%d (token=%s)",
    host, PORT, "configured" if token else "not configured/local-only",
  )
  web.run_app(app, host=host, port=PORT)


if __name__ == "__main__":
  main()

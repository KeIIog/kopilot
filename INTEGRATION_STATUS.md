# SunnyPilot + CarrotPilot integration draft

## Base and included features

- Driving/control base: uploaded `sunnypilot-release-mici.zip` (COMMA_VERSION 0.11.2).
- Carrot source: uploaded `openpilot-carrot-wip.zip` (nested openpilot COMMA_VERSION 0.11.1).
- Carrot Web/settings/log/dashcam/terminal source copied under `selfdrive/carrot/`.
- Web port changed to **8000** in the copied server, heartbeat, push and documentation paths.
- Carrot manager, navigation, web server, push and navd processes are registered in `system/manager/process_config.py`.
- Carrot Params keys and cereal services/messages were merged using sunnypilot custom reserved slots.
- sunnypilot model, lateral-control, MADS, mapd and sunnylink files remain the active base.

## Important limitation

This is a source-level integration draft, not a road-tested release. The Hyundai IONIQ 5 HDA2/ADAS-module modified-harness CAN-FD and panda-safety layers were **not automatically overwritten**, because doing so would replace sunnypilot vehicle-control behavior and can create unsafe CAN behavior. Carrot's Hyundai implementation remains available in the original uploaded Carrot ZIP for a later vehicle-specific manual merge.

The following were not verified here: full SCons build, generated C++ cereal bindings, comma 4 boot, panda safety tests, IONIQ 5 CAN buses, steering/braking engagement, and on-road behavior. Use only for code review/build testing; do not road-test before bench CAN validation and safety tests pass.

## Web access

After a successful device build and manager start, access:

```text
http://DEVICE_IP:8000
```

Set `CARROT_WEB_EXTERNAL=1` only when running the web server through the watchdog/external launcher.

## Build follow-up

`pyproject.toml` contains the added Carrot dependencies. `uv.lock` was not regenerated because this environment has no package-network access. Refresh the lockfile on a networked development machine before a clean build.

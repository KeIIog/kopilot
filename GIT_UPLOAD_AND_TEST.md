# Git upload / device test notes

1. Upload this directory as a Git repository.
2. On a Linux development machine, refresh dependencies/lock data and run the normal sunnypilot build/tests.
3. At minimum run Python compilation, Cap'n Proto loading, manager process tests, cereal service tests, and the Hyundai/panda safety suite.
4. Bench-test with ignition/CAN logging and wheels off the ground before enabling actuation.
5. The integrated Carrot web endpoint is configured for port 8000.

Do not flash or road-test this draft as though it were a verified release.

# TST_NBN_ROBOT

Automated test setup for the NBN oven test robot.

The repo holds two independent pieces:

| Path | What it is | Deps |
| --- | --- | --- |
| repo root | Mason/BSH test framework suite — image acquisition, text location, robot movement tests | Poetry, Python 3.13 |
| `AUTO ROBOT FORCE TEST/` | Standalone UR arm force-test scripts (knob push force vs. angle) | pip, `ur_rtde` |

## Setup after a clone or pull

Virtualenvs are **not** tracked in git. Rebuild them with:

```powershell
.\bootstrap.ps1
```

It is safe to re-run, and reuses existing environments. Useful flags:

```powershell
.\bootstrap.ps1 -Only force   # just the UR robot scripts (no Bosch VPN needed)
.\bootstrap.ps1 -Only root    # just the Mason suite
.\bootstrap.ps1 -Clean        # delete and rebuild from scratch
```

This creates `.venv/` at the root and `AUTO ROBOT FORCE TEST/.venv/`. Both are gitignored.

### Requirements

- **Root project** — Python **3.13.1+** (`<3.14`), Poetry, and network access to
  `artifactory-04.boschdevcloud.com`, which means the Bosch VPN plus valid Artifactory
  credentials. Without those, `poetry install` cannot resolve `mason-base` /
  `mason_home_appliance`.
- **Force tests** — any Python 3.10–3.13. No VPN needed; `ur_rtde` comes from PyPI.

`bootstrap.ps1` reports which of these is missing rather than failing cryptically.

## Running things

```powershell
# Mason test suite
poetry run pytest
poetry run pytest tests/test_robot_movement.py

# UR force test (moves a real arm — see the safety note below)
& ".\AUTO ROBOT FORCE TEST\.venv\Scripts\python.exe" ".\AUTO ROBOT FORCE TEST\arm_code.py"
```

Docker and Jenkins paths are in `mason-docker-run.sh`, `mason-env-setup.sh`, and `.jenkins/`.

## Before running a force test

`arm_code.py` moves a physical UR arm and pushes against a knob at 10 N.

- The robot IP is hardcoded as `ROBOT_IP = "192.168.10.150"` near the top of the script.
  Change it there if your bench differs.
- `START_POSE` is where the arm retreats to on `Ctrl+C`. Confirm it is safe for your
  current fixture before starting a run.
- `PUSH_FORCE`, `TEST_ANGLES_DEG`, and the sampling constants sit in the same config
  block — check them against the part under test.
- Results are written to `knob_test_results_<HHMMSS>.csv` in the working directory.

## Repo notes

- `venv311/` was previously committed to git (including `python.exe` and friends) and
  has since been untracked. The `.gitignore` now covers `venv[0-9]*/`. The binaries still
  exist in git history, so a fresh clone pulls roughly 23 MB; purging them needs a
  history rewrite (`git filter-repo --invert-paths --path venv311/`), which rewrites all
  commit SHAs.
- Historic run logs (`force_test_log_*.csv`) are committed under `AUTO ROBOT FORCE TEST/`.
  New runs write fresh files, so expect an untracked-file list after testing.

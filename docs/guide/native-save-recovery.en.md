> **Language / Ngôn ngữ:** [English](native-save-recovery.en.md) · [Tiếng Việt](native-save-recovery.vi.md) · [中文](native-save-recovery.md)

# Native archive history selection and clearance file recovery

2026-09-12. What this round implements is the integrity screening, explicit recovery and read verification of historical SRAM copies; it is not a new game archive format, nor is it automatic saving of safe nodes or instant archiving at any time.

## Player entrance

```sh
# 列出统一原生入口的历史副本和冻结初始备份；不启动游戏、不创建试玩目录。
.venv/bin/python tools/recomp/run/play_native.py \
  --profile config/recomp/profiles/play-profile.json --list-saves

# 恢复指定会话。ID 使用上一步列出的完整时间戳。
.venv/bin/python tools/recomp/run/play_native.py \
  --profile config/recomp/profiles/play-profile.json --restore-session SESSION_ID

# 显式回到冻结的第一话通关备份。
.venv/bin/python tools/recomp/run/play_native.py \
  --profile config/recomp/profiles/play-profile.json --restore-session initial
```

`--new-game`, `--restore-session`, `--list-saves` are mutually exclusive. If not specified, the first historical copy that passes the integrity check will be selected from newest to oldest; if neither is available, an initial backup with a fixed digest in the configuration will be attempted. The skip reason and actual selection are printed. If the specified session is invalid, it will be rejected directly without quietly selecting another progress; if there is no verifiable source, it will require checking the history or explicitly new game.

Unified profile, normal Japanese, native model and ROM model experiments continue to use their respective existing historical directories. Japan, China and Original/HD share the same JP identity under the same profile; the identities of ROM model experiments are checked separately. Both `.command` entries use project `.venv` and forward parameters.

## Verification and protection boundaries

Implementation: `src/srw64_native/save_history.py`; Access: `tools/recomp/run/play_native.py` and `run_host_probe.py`.

Candidate sessions must have identifiable and completed run reports, host exit code 0, matching ROM version with SHA-256, and an existing size and digest record of final SRAM. Currently, only original gameplay configurations are accepted; records involving unsupported gameplay configurations will not be automatically restored. The file must be exactly 32 KiB, consistent with the record digest, and not all zeros/all FF. Missing/corrupted reports, abnormal exits, corrupted same-length content, truncation, misidentification, and out-of-bounds/linked archives will be rejected. Content compilation directories and input copies do not participate in historical sorting.

**This document is consistent with existing records and does not prove that every in-game slot is valid. ** This round does not parse the original game's SRAM internal checksum, nor can it use a newly calculated digest to endorse files without existing records. In-game Load/Continue is still read and verified by the original game; a separate process is set up when repairing or importing unrecorded old files is required.

After selection, check the summary again, write the same bytes to `.source.sram` next to the new session in an exclusive creation mode, flush to disk before starting the host; `.save-selection.json` records the original source, selection reason and skip list. The probe's `--save-sha256` verifies this existing digest and continues to retain post-build checks for input changes. The game only writes its own new running directory, and the original sessions and frozen backups are not overwritten or deleted.

Source copies or selection records left behind by a startup interruption will not be candidates for the next automatic recovery. They are audit records of recovery inputs, not "atomic commits of new game saves"; safe node save collections and rotational elimination are not yet implemented.

## Actual cold start read

Evidence: [intermission-cold-1/reload-verification.json](../../build/recomp/save-recovery-check/intermission-cold-1/reload-verification.json). Using the same JP Rev 0 ROM, Japanese/Original profile, independent SRAM copy, silent throughout.

The original frozen file is `build/recomp/gfx-probes/first-map-turn5-reload-1/stage1-clear-turn7.sram` and the summary is `0c6ded15fdf60c6b0064b2260a335d17a4ff77386d14d634bfd7d3bcb8de7484`.

Actual process: Cold boot → Title Load → ROM cartridge → Archive 1 → Confirm → Prepare → Driver ability → Manami details → Exit normally.

| Observation position | Checked results | GPU screen |
| --- | --- | --- |
| Read slot list | Chapter 1 CLEAR, Manami level 2, total rounds 7, funds 14,500 | `present-2460.png` |
| Maintenance menu after actual recovery | Chapter 1 CLEAR, total round 7, funds 14,500 | `present-3000.png` |
| Recovered driver details | Manami Hamill, level 2, strength 100, SP 102/102 | `present-3960.png` |

All three scenes have been viewed, and the hashes and metadata are recorded in the evidence file mentioned above. The host exit code is 0; all 4 game threads are joined, and the number of observations before and after RDRAM is released is 0. The original frozen file, the source copy passed to the host, and the SRAM digest at the end of the run all retain their original values. There is no purchase of mods, resaves or access to second episodes.

`config/recomp/inputs/load-intermission-check.json` is exported from the actual confirmed VI input record of this round and can be used for subsequent reruns (`--vis 9000` is recommended). What is accepted in this round is the actual cold start and running control; the exported fixed input has not been replayed separately and cannot be marked as verified for deterministic playback. Run reports retain the original input script and all applied control events.

## Check and remaining work

- `make check`: 108 Python tests, compileall and dependency checks passed. 10 new tests cover old and new replica rollback, explicit recovery rejection, reporting/identity checks, gaps, symlinks, source freezes, secondary digest verification, read-only lists, and startup parameter passing.
- The native host uses the same binary that has been verified in the previous round and actually completes the cold start of this round; there is no modification to C++ or the acceptance conclusion of new components in this round.
- Not yet completed: SRAM internal format verification, arbitrary secure node serialization, multi-manual slot management UI, automatic save/rotate backup, different bookmarks, complete random/event status comparison, and save and read archive matrix under multi-language/art combinations.
- There is no new reference simulator comparison, and the historical comparison evidence of existing tactical interruptions still belongs to their respective records.
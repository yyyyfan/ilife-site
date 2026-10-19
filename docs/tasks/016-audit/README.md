# 016 验收材料
- 总结：`../016-acceptance.md`。
- 逐组记录：`songs.md`、`2026.md`、`2025.md`、`2024.md`（第一批，写于修正应用之前，文中「未提交到任务分支」指当时状态）、`2023.md`、`2022.md`、`2021.md`、`2020.md`、`32ea53c.md`。
- 修正脚本（幂等，已按 2026 → 2025 → 2024 → 2023 → 2021 → 2020 应用；2022 无修正）：`<年份>-fixes.py`，公用 `fixlib016.py`。在仓库根目录运行 `python3 docs/tasks/016-audit/<年份>-fixes.py db/ilife.sqlite [--dry-run] [--keep-unverified]`，然后 `python3 db/export.py` 与 `python3 db/export.py --check`。新增替换图已在 `img/`，原件在 Grok Bot 工作区 `/workspace/016-acceptance/assets/`。

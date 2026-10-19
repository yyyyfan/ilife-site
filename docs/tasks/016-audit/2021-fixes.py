#!/usr/bin/env python3
"""016 验收（2021 年演出配图，提交 7d031b9；Eventernote 图已由 32ea53c 删除）修正脚本 —— 幂等。
用法（在仓库根目录）：python3 docs/tasks/016-audit/2021-fixes.py [db/ilife.sqlite] [--dry-run]
然后运行 python3 db/export.py 与 python3 db/export.py --check。"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fixlib016 import Fixer
f = Fixer(sys.argv)
# 1) 4346 来源显示名：URL 写的是 @Paylove_info（另一个账号），帖子 1435921051947393024 的作者是 ペイラブ公式 @payloveofficial（キミ推しフェス 主办）
f.set_source_label(4346, 'X @Paylove_info', 'X @payloveofficial')
f.finish()

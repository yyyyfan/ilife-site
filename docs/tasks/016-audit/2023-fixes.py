#!/usr/bin/env python3
"""016 验收（2023 年演出配图，提交 e07576c；Eventernote 图已由 32ea53c 删除）修正脚本 —— 幂等。
用法（在仓库根目录）：python3 docs/tasks/016-audit/2023-fixes.py [db/ilife.sqlite] [--dry-run] [--keep-unverified]
然后运行 python3 db/export.py 与 python3 db/export.py --check。
依据均由 Grok Bot 于 2026-10-20 用 X 连接器打开原帖并逐张看图核对。"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fixlib016 import Fixer
f = Fixer(sys.argv)
# 1) 369 えなぴ生誕祭 3/24：复用的 789 是同帖第 1 张「甘音ゆあ生誕祭 2023.3.8」，应为同帖第 2 张 790「向日えな 2023 生誕祭 2023.3.24 @Veats Shibuya」
#    （官方 1618601140593250306「甘音ゆあ&向日えなの生誕祭の日程発表」，790 是库里已有的图）
if f.live_ok(369, '2023-03-24', 'えなぴ生誕祭2023'):
    f.unbind(369, 'https://pbs.twimg.com/media/FnZtJu9aMAEc_yE.jpg?name=medium', '图是甘音ゆあ生誕祭 3/8')
    f.bind_existing(369, 'https://pbs.twimg.com/media/FnZtJvKaUAAV_ad.jpg?name=medium')
# 2) 来源显示名写错账号（帖子 ID 正确，X 解析到的作者是括号里的账号）
f.set_source_label(4235, 'X @natsuzome2023', 'X @natsuzome_info')   # @natsuzome2023 不存在；作者 = NATSUZOME 官方 @natsuzome_info
f.set_source_label(4240, 'X @natsuzome2023', 'X @natsuzome_info')
f.set_source_label(4239, 'X @a_idolproject', 'X @NARLOW_info')      # @a_idolproject 已被封；帖子作者 = ANCHOR 所属组合 NARLOW（ANFES 是其出道公演）
# 3) 无法核实：427 SPARK 2023 7/16 的 4317 是 @SPARK_Fes「開催決定」视频的预览帧（粉色树木风景，无活动名/日期/iLiFE!），原帖也未提 iLiFE! → 删除这张 016 新增图
if '--keep-unverified' not in sys.argv and f.live_ok(427, '2023-07-16', 'SPARK 2023'):
    f.drop_new_image(4317, 'https://pbs.twimg.com/ext_tw_video_thumb/1607722998387343360/pu/img/EHCrcmHuz4BEgzOK.jpg', '视频预览帧，无活动信息，原帖未提 iLiFE!')
    f.drop_orphan_source('https://twitter.com/SPARK_Fes/status/1607723128494657536')   # 016 新增的 sources 4325，只被 4317 引用
f.finish()

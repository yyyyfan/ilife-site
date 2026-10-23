# 任务 033 结果：把人工复核数据从代码里搬出来

## 问题

028–032 每完成一步，就有一批「必须由人判断」的结论被写死在脚本顶部：

```python
# db/task029_cover_backfill.py
REJECT = {316, 417, 503, 558, 580, 581, 602, 603, 604, 675}

# db/task032_unofficial_scan.py
KEEP = {'lkWjBhI0H4o', 'R_6nG7R8GhY', ...}
```

三个后果：

1. **理由只活在注释里。** `REJECT` 上方那几行注释解释了 316 是分享卡、417 是登录墙，
   但半年后拿到一个 id 还是要先反查是哪个公演。注释不会跟着数据走。
2. **改一条要改代码。** 想把一条粉丝影像从 `keep` 挪到 `reject`，得编辑 Python 字面量、
   注意逗号和引号，然后 commit。
3. **写错是静默的。** `'lkWjBhI0H4o'` 打成 `'lkWjBhI0H4O'`（末位大写 O），脚本照跑，
   只是那条视频永远匹配不到，没有任何提示。

## 判断：不是所有硬编码都该搬

先分成三类，只搬第一类：

| 类型 | 例子 | 处理 |
|---|---|---|
| **人工结论**（会长、要理由、要审计） | 哪条粉丝影像算数、哪张图不能当封面、哪场整场辞退、哪首歌用哪张 jacket | ✅ 搬到 `db/curation/*.json` |
| **算法参数**（改它等于改行为） | `MINW=340`、`MAXSIDE=2048`、`sat<0.06`、`BAD` 正则、`UA` | ❌ 留在代码，和逻辑放一起才看得懂 |
| **一次性迁移的输入** | `task020` 的 `LIVES`、`task027` 的 `DURATION`/`NO_MV` | ❌ 不动，结论已落库，留着是判断依据 |

第二类搬出去反而更糟：`MINW` 为什么是 340 而不是 500，只有贴着「350–500 多是售票站小图」
那行注释才看得懂；拆到 JSON 里就只剩一个孤零零的数字。

第三类重跑会覆盖手工修正，搬成配置等于给未来的自己挖坑。

## 做法

### 数据文件

`db/curation/` 四份 JSON，一条一个对象，**每条都带 `reason`**：

| 文件 | 内容 | 条数 |
|---|---|---|
| `videos.json` | `keep` 26 / `reject` 3 | 29 |
| `live_covers.json` | `reject` 10（带 `hint` 公演名，仅供人看） | 10 |
| `live_members.json` | `no_show_lives` 5 / `overrides` 1 | 6 |
| `jackets.json` | `albums` 3 / `reuse` 1 | 4 |

`videos.json` 的 `keep` 额外带 `song`（歌曲编号），这是防同名曲的关键——
校验时会拿它和库里实际的 `song_id` 对，对不上直接报错。

### 加载器

`db/curation/__init__.py` 只做一件事：

```python
from curation import load
KEEP = {x['id'] for x in load('videos')['keep']}
```

文件缺失或 JSON 坏掉时抛 `SystemExit` 带中文说明（含行号列号），
而不是让脚本跑成「一条都没匹配到」：

```
缺少人工复核数据文件：…/db/curation/nope.json
_tmp_bad.json 不是合法 JSON：第 1 行第 14 列 —— Illegal trailing comma before end of array
```

四个脚本改完后，常量与改动前逐项比对一致（`NO_SHOW` 5 场、`REJECT` 10 场、
`JOBS` 3 个、`KEEP` 26 条），`task028 --dry-run` 仍是 6572 行，
`task032 --apply` 仍是「入库 0 条」（幂等）。

### 校验器

`db/curation_check.py` 查三层：

| 层 | 查什么 |
|---|---|
| 结构 | 字段齐不齐、video_id 是不是 11 位、有没有重复、`reason` 有没有写、**字段名有没有拼错** |
| 引用 | 指向的公演 / 成员 / 歌曲 / 图片在库里存不存在（成员必须写全名，昵称会报错） |
| 一致性 | 库里有非官方影像但白名单里没有 / 否决过的封面又挂上了 / 指定了 jacket 但封面还不是 jacket 图 |

字段名拼错单独点名，是因为 `"keep "` 多一个空格会让整份白名单失效，而 JSON 本身合法。

第一次跑就抓出两条自己偷懒写的 `"reason": "同上"`：

```
✗ jackets.json albums[2] 的 reason 太短（'同上'），写清楚是哪张图/哪条视频的问题
```

`--strict` 把警告也当失败，适合放进发布前检查。

## 文档

- `db/curation/README.md` —— 四份文件的字段说明 + 5 个常见改动场景的具体步骤
- `db/README.md` —— 新增「脚本分类」表：一次性 / 幂等可重跑 / 只读，改之前先看
- `docs/HANDOFF.md` —— §3 目录树、§5 命令、§11 历史
- `docs/ROADMAP.md` —— 顺手修了编号重复（030/031/032 各被用了两次），加对照表

## 一个明确的边界

JSON 是**输入**，数据库是**输出**。手工在 SQLite 里改 `live_members.status`
或 `songs.cover_image_id`，会被下次重跑覆盖。要改就改 JSON，跑脚本，再导出。

# 009 补全所有演出（第一阶段：数据结构 + 2020–2021 年）结果报告

## 1. 任务概述
本任务完成了 iLiFE! 演出数据结构的升级与 2020-06（结成）至 2021-12-31 期间全部公演数据的补全。保持原有 36 场核心公演结构不变（ID 0～35），新增 136 场经过交叉核实的历史公演记录，演出总数达到 172 场。

---

## 2. 数据结构升级

### 2.1 数据库结构（`db/schema.sql` & `db/ilife.sqlite`）
- **`venues` 表新增字段**：
  - `address TEXT`：会场地址（如 `東京都渋谷区宇田川町33-1`）
  - `capacity INTEGER`：会场容纳人数（如 `700`）
  - `url TEXT`：会场官方网址
- **`lives` 表新增字段**：
  - `type TEXT NOT NULL CHECK (type IN ('ワンマン','主催','対バン','フェス','リリイベ','生誕祭','配信','その他'))`
  - `open_time TEXT`：开场时间（JST，如 `16:30`）
  - `start_time TEXT`：开演时间（JST，如 `17:30`）
  - `note TEXT`：公演备注（如 2部制说明、延期/取消说明、毕业/新体制纪念等）
  - `setlist TEXT`：歌单（可空）
  - `is_headliner INTEGER NOT NULL DEFAULT 0`：主办/单独/生诞祭为 1，其余为 0
  - `source_id INTEGER NOT NULL REFERENCES sources(id)`：出处外键
- **新增 `live_members` 表**（留存扩展出演成员结构）：
  - `live_id INTEGER NOT NULL REFERENCES lives(id)`
  - `member_id INTEGER NOT NULL REFERENCES members(id)`
  - `status TEXT NOT NULL DEFAULT '出演'`
  - `PRIMARY KEY (live_id, member_id)`

### 2.2 导出脚本更新（`db/export.py`）
- 增加完整性检查：
  - `date` 格式合规性检查（ISO 日期）
  - `lives.type` 取值合法性检查
  - 同日同会场去重检查：`SELECT date, venue_id, count(*) FROM lives GROUP BY date, venue_id HAVING count(*) > 1`
  - 每场公演必须有关联出处检查（`source_id IS NOT NULL`）
  - 时间格式检查（`open_time`/`start_time` 格式为 `HH:MM`）
- 导出 `data/lives.json`：包含 `id`, `date`, `title`, `type`, `venue`, `pref`, `open_time`, `start_time`, `note`, `setlist`, `is_headliner`, `source` 等全部字段，并按 `date, id` 严格正序排列。

---

## 3. 2020–2021 年演出逐月统计

2020–2021 年共计收录 **140 场** 公演（2020 年 45 场，2021 年 95 场）。

| 年月份 | 场数 | 主要类型分布 | 数据出处 |
| :--- | :---: | :--- | :--- |
| **2020-06** | 1 | 配信 (1) | Wikipedia (プレデビュー無観客配信) |
| **2020-07** | 3 | ワンマン (2), 对バン (1) | Wikipedia, Eventernote, 官方推文 (@iLiFE_official) |
| **2020-08** | 9 | 主催 (2), ワンマン (1), フェス (4), 对バン (2) | 官方推文 (@iLiFE_official), Eventernote |
| **2020-09** | 4 | 主催 (1), フェス (3) | Eventernote, 官方推文 (@iLiFE_official) |
| **2020-10** | 10 | 生诞祭 (2), 主催 (1), 对バン (3), フェス (4) | 官方推文 (@iLiFE_official), Eventernote |
| **2020-11** | 8 | フェス (4), 对バン (4) | Eventernote, 官方推文 (@iLiFE_official) |
| **2020-12** | 10 | 生诞祭 (1), ワンマン (1), 主催 (1), 对バン (3), フェス (2), その他 (2) | Eventernote, 官方推文 (@iLiFE_official) |
| **2021-01** | 6 | 对バン (6) | 官方推文 (1月日程图), Eventernote |
| **2021-02** | 5 | 对バン (3), フェス (2) | Eventernote |
| **2021-03** | 4 | ワンマン (1), 主催 (1), フェス (2) | 官方推文 (@iLiFE_official), Wikipedia, Eventernote |
| **2021-04** | 4 | 对バン (4) | Eventernote |
| **2021-05** | 8 | 生诞祭 (1), フェス (4), 对バン (3) | 官方推文 (@iLiFE_official), Eventernote, LiveFans |
| **2021-06** | 9 | 主催 (1), フェス (3), 对バン (5) | 官方推文 (6月日程图), Eventernote, LiveFans |
| **2021-07** | 13 | 生诞祭 (1), フェス (5), 对バン (7) | 官方推文 (7月日程图), Eventernote |
| **2021-08** | 10 | ワンマン (1), フェス (3), 对バン (6) | 官方推文 (@iLiFE_official), Eventernote, LiveFans |
| **2021-09** | 8 | 主催 (1), フェス (3), 对バン (4) | 官方推文 (9月日程图), Eventernote |
| **2021-10** | 10 | 生诞祭 (1), フェス (7), 对バン (2) | 官方推文 (@iLiFE_official), Eventernote, LiveFans |
| **2021-11** | 5 | フェス (4), 对バン (1) | Eventernote |
| **2021-12** | 13 | ワンマン (1), 生诞祭 (1), フェス (5), 对バン (6) | 官方推文 (@iLiFE_official), Eventernote, Wikipedia |
| **总计** | **140** | — | — |

---

## 4. 抽查 10 场公演出处核对

随机抽取不同月份、不同类型及出处的 10 场演出，经 HTTP 请求确认链接可正常打开，且公演日期、会场、内容均完全一致：

1. **2020-06-27** プレデビューLIVE（无观众）
   - 会场：渋谷ストリームホール（配信）
   - 出处：https://ja.wikipedia.org/wiki/ILiFE!
   - 核对结果：一致（HTTP 200，记录 2020年6月27日 渋谷ストリームホール 无观众先行出道配信）

2. **2020-07-19** デビューLIVE
   - 会场：Veats SHIBUYA
   - 出处：https://ja.wikipedia.org/wiki/ILiFE! 与推文 https://x.com/i/status/1284838364802244608
   - 核对结果：一致（HTTP 200，Veats SHIBUYA 90名限定出道单独特典与当日无观众直播）

3. **2020-08-01** なんキニ！×iLiFE! つーまんらいぶ！
   - 会场：原宿ベルエポック美容専門学校 第2校舎
   - 出处：https://x.com/i/status/1287708621367685120
   - 核对结果：一致（HTTP 200，官方 X 详细通知：2020/8/1 原宿ベルエポック美容専門学校 OPEN 16:30 / START 17:10）

4. **2020-08-14** IDOL CONTENT EXPO @ヒューリックホール東京 ～豪華夏休みスペシャルLIVE!!!～
   - 会场：ヒューリックホール東京
   - 出处：https://www.eventernote.com/events/256989
   - 核对结果：一致（HTTP 200，2020-08-14 開場16:10 / 開演17:10 ヒューリックホール東京）

5. **2020-09-22** Vega Fes 1部
   - 会场：新宿BLAZE
   - 出处：https://www.eventernote.com/events/259618
   - 核对结果：一致（HTTP 200，2020-09-22 開場13:00 / 開演13:30 新宿BLAZE）

6. **2020-11-11** IDOL CONTENT EXPO @ 神田明神ホール Vol.10 ～ポッキー＆プリッツの日SP!!!～
   - 会场：神田明神ホール
   - 出处：https://www.eventernote.com/events/263425
   - 核对结果：一致（HTTP 200，2020-11-11 開場17:45 / 開演18:30 神田明神ホール）

7. **2021-02-02** ハープスター×iLiFE! 無銭2マン
   - 会场：Zirco Tokyo
   - 出处：https://www.eventernote.com/events/270398
   - 核对结果：一致（HTTP 200，2021-02-02 開場18:30 / 開演19:00 Zirco Tokyo）

8. **2021-05-14** HEROINES FES
   - 会场：Zepp Tokyo
   - 出处：https://www.livefans.jp/events/1316074
   - 核对结果：一致（HTTP 200，2021-05-14 Zepp Tokyo 出演）

9. **2021-06-13** MARQUEE祭mini Vol.80
   - 会场：TSUTAYA O-nest
   - 出处：https://www.eventernote.com/events/277980
   - 核对结果：一致（HTTP 200，2021-06-13 開場15:00 / 開演15:30 TSUTAYA O-nest）

10. **2021-07-31** STAND OUT IDOL vol.10-SUN-
    - 会场：恵比寿CreAto
    - 出处：https://x.com/i/status/1417031455268491267
    - 核对结果：一致（HTTP 200，7月官方日程表原定 7/31 恵比寿CreAto，因疫情活动自肃取消并标注 note）

---

## 5. 前端功能与响应式适配

1. **公演页（`lives.html`）**：
   - 顶部增加类型筛选按钮芯片（全部、ワンマン、主催、対バン、フェス、生誕祭、配信、その他），附带实时数量统计。
   - 点击筛选按钮通过 `history.replaceState` 无刷新同步 URL 参数（`?t=...`），并支持直接带参访问。
   - 丰富公演表格展示：新增类型徽章（按类型着色）、完整开场/开演时间、活动备注（取消/延期/2部制说明等）、出处直达链接。
   - 外层容器配置横向滚动（`overflow-x: auto; -webkit-overflow-scrolling: touch;`），移动端横向滑动手感平滑。
2. **日历页（`calendar.html`）**：
   - 增加类型筛选胶囊标签，支持组合月份与类型筛选。
   - 单元格内公演增加对应类型小徽章与开演时间标注。
3. **响应式验证**：
   - 1280px 桌面端：排版整齐，表格横向拉伸舒展，无错位或空白。
   - 390px 移动端：导航栏、筛选胶囊正常折行，表格自适应内部滚动，无撑爆视口或控制台报错。

---

## 6. 验收自查

- [x] 2020–2021 年演出逐月列出，写明每月场数和使用的来源
- [x] 抽查 10 场出处可打开且日期、会场一致
- [x] 无重复（同日同会场去重完毕，4 组同日 1部/2部 公演已合并标注）
- [x] 公演页、日历页按 type 筛选正常，1280/390 宽度无报错
- [x] `python3 db/export.py --check` 全部通过（数据与静态资源版本逐字节一致）

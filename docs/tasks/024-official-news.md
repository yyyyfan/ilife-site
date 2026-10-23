# 024 里程碑公演改用官方公告为源，并补全开场/开演时间

## 背景与发现

原计划是「把 2023 年 65 场仅非官方来源的公演升级为官方来源」。动手前先找可用渠道，结论如下：

- Wayback Machine 的 CDX 接口仍报「Temporarily Offline」，无法批量取 2023 年的官网快照。
- X（Twitter）站内关键词搜索需登录，无法按活动名检索 2023 年的告知帖。
- 官网 `ilife-heroines.com/topics/` 列表页只显示最近 10 条，但**详情页 `topics/detail/index/<id>` 仍然在线**。
  顺着 ID 段 900–2050 全量扫了一遍（1150 次请求），站点在 JamClip 改版时把旧公告大量删除，
  现存公告只剩 **21 条（2023-04 起）**，2018–2022 全部丢失。所以 65 场 2023 年公演**无法**用官网公告升级。

但这次扫描顺带暴露了一个更值得修的问题：

- `lives` 表里有 **27 条**记录 `source_id=1`，即出处仍是 Wikipedia，全是「里程碑公演」——
  KiSEK!、ももいろ歌合戦、4 周年、卒業公演、新体制お披露目、ONELiFE! 武道馆、BRAVE GROOVE、
  TRAVELiFE! 2026 九场、MEGALiFE!、JAPANLiFE! 2027 十一场。
- 这 27 条里 **open_time / start_time 全部为空**，note 也全为空。
- 其中 10 条恰好有官方公告可覆盖（8 场 2026 巡演 + MEGALiFE!），另有 1 条（卒業公演）有官方公告确认日程。
- `members` 表 26 人全部 `source_id=1`（Wikipedia），其中「那蘭のどか」的离开日期只有 Wikipedia 支撑，
  而官方 2025-08-25 公告明确写了 8/27 当日脱退。

所以 024 改做：**用官方公告替换 Wikipedia 出处，并把公告里写明的开场/开演时间补进库**。

## 范围

要改：

1. `lives` 14–21（TRAVELiFE! 2026，8 场）
   - `source_id`：Wikipedia → 官方公告 2026-03-27（topics 1948）
   - `open_time` / `start_time`：按公告逐场填（JST）
   - `note`：写明公告日与「優先物販」时段；特典会规则引 2026-06-01 公告（topics 1973）
2. `lives` 22（MEGALiFE! 2026-08-26 Kアリーナ横浜）
   - `source_id`：Wikipedia → 官方公告 2026-06-02（topics 1974）
   - `open_time=16:00`、`start_time=17:30`（公告「OPEN 16:00 / START 17:30」）
   - `note`：2026-07-10 公告全席完売；2026-08-16 公告后日特典会（8/27 パシフィコ横浜 展示ホールB、
     9/12 東京流通センター 第二展示場Fホール）
3. `lives` 9（向日えな・涼芽なの卒業公演 2024-09-01 豊洲PIT）
   - `source_id`：Wikipedia → 官方公告 2024-08-16（topics 1634，原文写明 9/1 豊洲PIT 卒業公演）
4. `members` 22（那蘭のどか）
   - `member_fields_sources` 里 `left` 字段的来源：Wikipedia → 官方公告 2025-08-25（topics 1874）
   - `left_` 文案补上「当日武道館公演为最后出演」
5. 新增 `docs/reference/official-news-index.md`：把现存 21 条官方公告做成索引（ID/日期/标题/URL），
   避免以后重复扫描
6. 新增 `db/task024_official_news.py`（幂等，支持 `--dry-run`）

不做：

- 不改剩下 17 条 Wikipedia 源公演（5 KiSEK!、7 ももいろ歌合戦、8 4 周年、10 新体制お披露目、
  11 ONELiFE!、13 BRAVE GROOVE、25–35 JAPANLiFE! 2027）——官网现存公告不覆盖这些，改不了就是改不了，
  留待官方公告或 X 帖可确认时再动
- 不碰 2023 年那 65 场「仅非官方来源」公演（渠道不可用，见上）
- 不写 `live_members`（该表 0 行且 `export.py` / `app.js` 都不引用，属未启用功能；
  2025-06-01 公告里的 9 人特典会排班只作为 note 佐证，不据此断言全员出演）
- 不改 2026-06-01 那场 iLiVE! vol.17（704）的来源——官方 2026-05-30 公告只讲特典会运营，
  不足以作为公演本身的出处

## 数据来源

全部需实际打开确认：

| 用途 | URL |
|---|---|
| TRAVELiFE! 2026 八场日程与 open/start | https://ilife-heroines.com/topics/detail/index/1948 （2026.3.27） |
| TRAVELiFE! 2026 特典会规则 | https://ilife-heroines.com/topics/detail/index/1973 （2026.6.1） |
| MEGALiFE! 公演概要 + FC 先行 | https://ilife-heroines.com/topics/detail/index/1974 （2026.6.2） |
| MEGALiFE! 全席完売 | https://ilife-heroines.com/topics/detail/index/1988 （2026.7.10） |
| MEGALiFE! 后日特典会 | https://ilife-heroines.com/topics/detail/index/1999 （2026.8.16） |
| 卒業公演（9/1 豊洲PIT） | https://ilife-heroines.com/topics/detail/index/1634 （2024.8.16） |
| 那蘭のどか 脱退（8/27 当日） | https://ilife-heroines.com/topics/detail/index/1874 （2025.8.25） |

已知事实（已核对原文）：

- TRAVELiFE! 2026：6/1 Zepp Haneda 16:30/17:30（優先物販 14:00-15:30）、6/4 Zepp Osaka Bayside 17:00/18:00、
  6/5 Zepp Osaka Bayside 17:00/18:00、6/9 Zepp Fukuoka 17:00/18:00、6/14 Zepp Sapporo 16:00/17:00
  （優先物販 13:30-15:00）、6/22 Zepp Nagoya 17:00/18:00、6/23 Zepp Nagoya 17:00/18:00、
  6/30 KT Zepp Yokohama 16:30/17:30（優先物販 13:00-14:30）。
  公告另注「サポートメンバー、恋星はるかの出演は予定しておりません」。
- MEGALiFE!：2026-08-26（水）OPEN 16:00 / START 17:30 @Kアリーナ横浜，出演 iLiFE!。
  票价 6 档（SS ¥80,000 / S ¥30,000 / A ¥16,000 / 1F ¥8,000 / 2F ¥6,000 / 3F ¥4,000）。
- 後日特典会：DAY1 2026-08-27 パシフィコ横浜 展示ホールB（5 部制）、
  DAY2 2026-09-12 東京流通センター 第二展示場Fホール（6 部制）。
- 卒業公演：向日えな・涼芽なの 2024-09-01 豊洲PIT 卒業公演后毕业（公告 2024-08-16）。
- 那蘭のどか：重大な規約違反，8/27 日本武道館公演 9 人出演，当日脱退，此后 8 人活动（公告 2025-08-25）。

## 验收标准

- [ ] `python3 db/export.py --check` 通过
- [ ] 27 条 Wikipedia 源公演中，14–21、22、9 共 10 条的 `source_id` 指向实际打开过的官方公告页
- [ ] 这 10 条的 `open_time` / `start_time` 与公告一致（HH:MM，JST）
- [ ] 那蘭のどか 成员页「离开」一行的 `[源]` 指向官方公告，不再是 Wikipedia
- [ ] `docs/reference/official-news-index.md` 列出 21 条公告，URL 可打开
- [ ] 本地打开 2026-06 / 2026-08 / 2024-09 公演列表与 MEGALiFE! 详情，时间正常显示
- [ ] `docs/HANDOFF.md` 第 12、13 节同步

## 状态

待验收（见 `024-result.md`）

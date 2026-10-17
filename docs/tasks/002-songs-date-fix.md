# 歌曲日期与出处修正（001 返工）
## 目标
001 验收未通过：部分歌曲日期没有出处（疑似占位值），且 `release_date` 含义混用（有的是 MV 公开日，有的是收录作品发行日）。修正后歌曲页的每个日期都能对上出处。
## 范围
只改 `db/ilife.sqlite` 的 `songs` 表（必要时改 `db/schema.sql` 与 `db/export.py`、`app.js` 的歌曲渲染），重新导出 `data/songs.json`。不改打歌服数据，不改其他页面。
## 问题清单
1. 以下歌曲的日期在 Wikipedia 楽曲表中为空，库里却写了月初日期，属于无出处数据：
   - Ride On!：2022-01-01
   - Shout of Joy：2022-10-01（Wikipedia 只写了 2022 年，为ハンドボール日本伝来100年記念 公式応援ソング）
   - ドラマチックミライ：2023-05-01
   找不到出处就留空，并在 note 注明“日期未查到”。
2. `release_date` 含义混用：如 星色トラベラー 写 2020-06-16（MV 公开日），所属作品却是 2023-01-10 的专辑『アイライフスターターパック』；Hands Up!（2022-09-09）、会いにKiTE!（2022-12-25）同理。请拆成两列：`mv_date`（MV 公开日，出处 Wikipedia 楽曲表）与 `release_date`（首次收录作品的发行日），各自可为空。
3. 初恋リバイバル、Sleeping face 在 Wikipedia 注明为“妄愛グラビティのカバー”，note 里补上，且不要称为原创曲。
4. 『アイドルライフスターターパック』单曲与专辑『アイライフスターターパック』名称相近，确认每首歌的 `release` 指向正确作品。
## 数据来源
Wikipedia（https://ja.wikipedia.org/wiki/ILiFE!）楽曲表与ディスコグラフィ、官网 discography（https://ilife-heroines.com/discography/）、官方 X（@iLiFE_official）。
## 验收标准
- [ ] 上面 3 首歌没有无出处日期
- [ ] 每首歌的 `mv_date` 与 Wikipedia 楽曲表一致，`release_date` 与所属作品发行日一致
- [ ] 两首翻唱曲已注明
- [ ] `python3 db/export.py --check` 通过
- [ ] 歌曲页在桌面与手机宽度显示正常
## 状态
待办

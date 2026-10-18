# 补全歌曲卡片封面与打歌服
## 背景
歌曲页 44 首中有 19 首没有任何打歌服记录，卡片只显示音符占位：
sweet timer、Sleeping face、Quest×Quest、Dokkoi!ロマンティック、黄昏サイクル、青春のパズルは埋まらない、キラメキダイアリー、HUNGRY!!!、可変三連MIXをおぼえる歌、Ride On!、Hands Up!、Shout of Joy、ヒラリラリア、KiSEK!、ドラマチックミライ、ライフステージ、メッセージ、完全勝利Love&Good！、i REVOLUTION
（另外 25 首有打歌服且已有图片，无需处理。）
## 目标
每首歌尽量有可显示的卡片图，且有出处。
## 做法（按优先级）
1. **专属打歌服**：官方 X（@iLiFE_official）有该曲专属衣装的公开帖/照片 → 新增 costumes 记录并关联图片（图片已在 images 表就直接关联；新图片下载到 img/ 并登记）。
2. **MV 或发布时使用的衣装**：该曲 MV 公开/发布告知帖中的官方图片 → 作为该曲衣装或封面关联，注明“MV 衣装/发布告知图”。
3. **配信封面**：仍没有时，可用该曲配信 jacket（官方帖或官网 discography 的图）作为卡片封面，新增 `songs.cover_image_id` 字段（导出到 songs.json 的 `cover`），前端优先用打歌服首图，没有再用 cover，再没有才显示音符。
4. 都查不到：保持占位，在 note 写明“未找到官方图片”。
不得用非官方图片，不得猜测；日期用 JST。
## 范围
db/ilife.sqlite（costumes、images、songs）、db/export.py（如需导出 cover、增加检查）、songs 页前端的封面取图逻辑。不改其他页面。
## 验收标准
- [ ] 19 首逐首有结论（专属衣装 / MV 衣装 / 封面 / 未找到），列表写在 `docs/tasks/005-result.md`，每条附出处链接
- [ ] 新图片文件存在并登记，图片不裁剪
- [ ] 卡片有图数量增加，筛选“有打歌服”数量与 costumes 数据一致
- [ ] `python3 db/export.py --check` 通过
## 状态
待验收 (e0aebbd)

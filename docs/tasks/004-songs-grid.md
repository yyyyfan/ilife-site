# 歌曲页改为统一卡片网格
## 目标
解决歌曲页卡片高度不一、需要长时间滚动的问题。列表页只放大小统一的小卡片，点开进入详情。用户已选定方案 A。
## 参考
本地预览 `preview/songs-grid.html`、`preview/common.js`、`preview/preview.css`（未提交，可直接复用其实现）；截图 `/workspace/shots/preview-grid-{desk,mob,detail}.png`。
## 范围
改 `songs.html` 及相关 JS/CSS；复用现有 `data/songs.json`、`images.json`，不改数据。完成后删除 `preview/` 目录，不要提交它。不改其他页面。
## 要求
- 卡片尺寸统一：电脑 5 列、手机 2 列；显示图片、歌名、假名、MV 公开日、所属作品、打歌服数量
- 图片放在固定框内等比缩放（object-fit: contain），不裁剪、不变形；无图时显示应援色音符占位
- 保留分类筛选（含「翻唱」）
- 点击进入 `songs.html?s=ID` 详情：返回链接、歌曲信息、出处、按时期分组的打歌服照片；详情照片网格沿用全站可调列数规则
- 浏览器前进后退可用；直接打开 `?s=ID` 能显示详情
## 验收标准
- [ ] 电脑 1280 与手机 390 宽度下卡片大小一致，无横向滚动
- [ ] 44 首歌全部显示，筛选数量正确
- [ ] 详情页照片不裁剪、全部加载
- [ ] `python3 db/export.py --check` 通过
- [ ] 仓库中没有 `preview/`
## 状态
待验收 (a0aa7d8)


# 021 结果报告

## 做了什么

`db/export.py` 的 `IMG_BASE` 从 `https://pub-12b0e8cdf6994377a377f1b1909e1ea9.r2.dev/`
改为 `https://img.ilifefan.dpdns.org/`，重新导出。

- 数据库没动：`images.local` 存的是对象键（`img/<文件名>`，4310 条），导出时才拼前缀。
- 新增版本号 `45be9b96`，各 HTML 的 `?v=` 已同步更新。

## 验证

| 检查 | 结果 |
|---|---|
| `db/export.py --check` | 全部「逐字节一致」 |
| `data/images.json` 地址 | 4311 条中 4310 条为新域名；1 条是 Wayback 外链（原图未落地，本就不走 R2） |
| `r2.dev` 残留 | 0 |
| `db/r2_images.py verify --sample 25` | 核对 25 个对象，问题 0 个 |
| 首页 `<img>` | 18 个，全部新域名 |
| 图库 `<img>` | 120 个，全部新域名，截图无破图 |
| 歌曲详情 `songs.html?s=42` | 8 个，全部新域名 |

单张核对：`https://img.ilifefan.dpdns.org/img/EbHIo8uVcAEuttq.jpg`
→ 200、`image/jpeg`、124614 字节、md5 `7a123adcd1d15fd69dbbbee83771cade`，与 `db/r2_manifest.json` 一致；
响应头 `Server: cloudflare`、`CF-RAY: ...-NRT`（走 CF 东京边缘）。

## 遗留 / 后续（已更新 2026-10-23）

1. **Cache Rule**：已配置并实测（见提交 `bc1684e` / HANDOFF 第 6 节；Hostname = `img.ilifefan.dpdns.org`，TTL 1 年）。
2. **r2.dev**：按站务要求**保持开启**作备用/开发（勿关）。
3. **部署**：已随 main 发布。GitHub Pages 与 Cloudflare Pages 线上 `data/version.json` 均走自定义域名图片（当前版本以两站 `version.json` 为准；本核对时为 `46b84571`，部署 id `cba02b1c-5419-4afe-8eec-3dbc67dfc451`）。

## 状态

已上线（021 代码切换 + 后续 main 部署；2026-10-23 再核对：两站 version 一致、抽查对象与页面图片均 `img.ilifefan.dpdns.org` HTTP 200）。

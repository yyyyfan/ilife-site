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

## 遗留

1. **Cache Rule 未配**（需要 Cloudflare 面板/凭据）：建议给 `img.ilifefan.dpdns.org/*` 设
   Cache Everything + Edge/Browser TTL 1 年，图片文件名唯一、内容不变，缓存后源站请求接近 0。
2. **r2.dev 未关闭**：等本次改动部署、线上两站核对无破图后再关（R2 → Settings → Public Development URL → Disable），
   保留作为回滚路径。
3. **未部署**：本机没有 GitHub / Cloudflare 凭据，改动只在本地 `agy/021-image-domain` 分支。

## 状态

待验收

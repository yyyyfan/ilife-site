# 部署时自动给静态资源加版本号，避免浏览器缓存旧版
## 背景
用户在部署后仍看到旧版歌曲页（缺封面），强制刷新才正常。原因是浏览器缓存了旧的 app.js / style.css / data/*.json。
## 目标
每次发布后用户普通刷新即可看到新版。
## 要求
- 所有 HTML 引用的 `app.js`、`style.css` 加 `?v=<版本>`；JS 里 fetch 的 `data/*.json` 同样带 `?v=<版本>`
- 版本号在导出/部署时自动生成（如 git 短提交号或内容哈希），不要手改；建议由 `db/export.py` 或 `deploy.sh` 写入一个小文件（如 `data/version.json` 或 HTML 内常量），并更新 HTML 中的引用
- HTML 本身尽量不被长期缓存：Cloudflare Pages 增加 `_headers`，对 `*.html` 及 `/` 设 `Cache-Control: no-cache`；带版本号的资源可长缓存
- GitHub Pages 无法设头，靠版本号即可
- 不改页面外观和数据内容；本地直接打开或 `python3 -m http.server` 仍能正常运行
## 验收标准
- [ ] 所有页面的 CSS/JS/JSON 请求都带版本号，且与当前提交一致
- [ ] 连续两次导出/部署，版本号随内容变化而变化，内容不变时不产生无意义的差异
- [ ] `_headers` 生效（部署后 HTML 响应头含 no-cache）
- [ ] 8 个页面在 1280 与 390 宽度下正常，无报错
- [ ] `python3 db/export.py --check` 通过，README 发布说明已更新
## 状态
待验收 (c349d72)

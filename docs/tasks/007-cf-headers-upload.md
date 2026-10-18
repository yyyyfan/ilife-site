# 部署模板正确上传 _headers
## 背景
`db/cf_deploy.template.js` 把 `_headers` 当普通文件放进 manifest。Cloudflare Pages 直接上传时 `_headers`（以及 `_redirects`、`_routes.json`）须作为创建部署请求里单独的表单字段发送（参考 wrangler 的实现），否则不生效。006 部署时是手工处理的。
## 要求
- 模板与 `deploy.sh`/`cf_upload.py` 把 `_headers`、`_redirects`、`_routes.json`（存在时）排除出 manifest，并作为同名表单字段随部署请求发送
- `--dry-run` 输出里单独列出这些特殊文件
- README 发布说明同步
- 不使用真实令牌，不部署
## 验收标准
- [x] dry-run 中 manifest 不含 `_headers`，特殊文件单独列出
- [x] 生成的部署脚本包含 `_headers` 表单字段
- [ ] 下次真实部署后 `curl -I https://ilife-site.pages.dev/` 仍含 `cache-control: no-cache`
## 状态
已完成（35649c6 验收通过，2026-10-18；假令牌离线测试：dry-run 中 _headers 单独列出、manifest 3726 个文件不含它；生成脚本含 _headers 表单字段，与 wrangler 做法一致。线上已确认：2026-10-18 部署 f96b0d82 后 curl -I https://ilife-site.pages.dev/ 返回 cache-control: no-cache）

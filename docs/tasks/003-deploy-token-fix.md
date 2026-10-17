# 修复 deploy.sh 的 Cloudflare 上传步骤
## 目标
`./deploy.sh "说明" token.txt` 一次跑完：导出 → 提交推送 → 上传 Cloudflare → 生成 db/cf_deploy.js，不再中途失败。
## 范围
只改 `deploy.sh`、`db/cf_upload.py`（必要时 `db/cf_deploy.template.js`）和 `db/README.md` 的“发布”一节。不改数据和页面。
现象：cf_upload.py 要求令牌文件是 JSON（`{"jwt": ...}`），而连接器拿到的通常是纯文本 JWT，传入后报错，上传中断。
## 要求
- 令牌文件同时支持纯文本 JWT 和 `{"jwt": "..."}` 两种格式（去掉首尾空白）
- 令牌缺失、格式错误或过期时给出清楚的中文错误提示，并以非零码退出
- 上传失败时不要留下半成品的 cf_deploy.js；脚本开头加 `set -euo pipefail`
- 不得把令牌写进日志、提交或任何仓库文件；用完提示删除临时文件
- 增加 `--dry-run`：只列出待上传文件和哈希，不调用网络
## 验收标准
- [x] 用假令牌分别以纯文本和 JSON 格式运行 `cf_upload.py --dry-run`，都能正确解析
- [x] 空文件、非法 JSON 时报中文错误并非零退出
- [x] `git grep` 仓库中无令牌内容
- [x] README 发布说明与新行为一致
## 状态
已完成 (3d5e1a0) — 验收通过 2026-10-18：dry-run 纯文本/JSON 均解析成功；空文件、非法 JSON、文件不存在均中文报错 exit=1；set -euo pipefail 与 EXIT trap 清理已验证；git grep 无令牌；README 一致。


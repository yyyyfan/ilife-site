# 021 图片基地址切换到 R2 自定义域名

## 目标

把站点图片地址从限速的 `r2.dev` 开发端点（`https://pub-12b0e8cdf6994377a377f1b1909e1ea9.r2.dev/`）
换成 R2 自定义域名 `https://img.ilifefan.dpdns.org/`（2026-10-22 已绑定并 Active），
让图片走 Cloudflare 边缘缓存，消除 429 风险。

做完后：`data/images.json` 里 4310 条站内图片地址全部指向新域名，页面图片正常加载，`export.py --check` 通过。

## 范围

要改：

1. `db/export.py` 的 `IMG_BASE`（唯一配置点）改为 `https://img.ilifefan.dpdns.org/`
2. 重新导出 `data/*.json`（`images.json` 里 4310 条 `local` 地址会一次性变化）、`data/version.json` 与各 HTML 的 `?v=`
3. `docs/HANDOFF.md` 第 1、6 节里的图片地址说明

不做：

- 不动数据库（`images.local` 存的是 `img/<文件名>` 键，不需要改）
- 不在本任务关闭 r2.dev 公共访问（等线上核对完再关，留回滚余地）
- 不配置 Cache Rule（在 Cloudflare 面板操作，凭据不在本机）

## 数据来源

- R2 自定义域名 `img.ilifefan.dpdns.org`：2026-10-22 在 R2 → 桶 `ilife-images` → Settings → Custom Domains 绑定，
  证书 `CN=eaa05fec.sni.cloudflaressl.com`（Google Trust Services），响应头 `Server: cloudflare`。
- DNS：`ilifefan.dpdns.org` NS 为 `rommy.ns.cloudflare.com` / `alexia.ns.cloudflare.com`；
  国内 doh.pub / alidns 解析到 CF IP（104.21.90.138 / 172.67.156.196）。

## 验收标准

- [x] `python3 db/export.py --check` 全部一致
- [x] `data/images.json` 4311 条中 4310 条为新域名（1 条为 Wayback 外链，本就不落地）
- [x] 全库无 `r2.dev` 残留
- [x] `python3 db/r2_images.py verify --sample 25` 问题 0 个
- [x] 首页 / 图库 / 歌曲详情页的 `<img>` 全部走新域名，图库截图无破图

## 状态

待验收（见 `021-result.md`）

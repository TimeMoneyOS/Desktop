# TimeMoneyOS 技术笔记

基于 MkDocs Material 的静态文档网站。源码位于 `docs/`，页面目录和主题位于 `mkdocs.yml`。

## 本地预览

本地构建需要 Python 3.12。第一次准备环境：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

双击 `preview.bat`，访问 http://127.0.0.1:8008/ 。修改 Markdown 后自动刷新。

双击 `build.bat` 执行严格构建，生成的 `site/` 不提交到 Git。

## 用 VS Code 提交和推送

1. 打开本仓库文件夹。
2. 在源代码管理中检查改动、暂存、填写提交说明并提交。
3. 点击同步或推送，将 `master` 推送到已配置的 `origin`。
4. GitHub 仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
5. 在 **Actions → Deploy documentation to GitHub Pages** 中检查结果；若推送发生在开启 Pages 之前，可点击 **Run workflow** 重试。

发布成功后的地址：https://timemoneyos.github.io/Desktop/

本地已经保留远程仓库原有历史并设置 `origin`；无需重新初始化或创建另一个远程仓库。GitHub 部署使用云端环境，不依赖本机的 `.venv`。

## 内容维护

- `docs/receiver.md`：完整的信息波接收讲义。
- `docs/assets/info-wave/`：SVG 图示与 PNG 版本。
- `tools/figures/`：波形图的 Python 生成源码，重新生成需要 NumPy、SciPy、Matplotlib，输出写入图示目录。
- `docs/javascripts/image-viewer.js`：本地图示放大，支持点击、键盘和 Escape 关闭。
- `.github/workflows/deploy.yml`：提交至 `master` 后自动严格构建并部署。

增加文章时在 `docs/` 新建 Markdown，然后更新 `mkdocs.yml` 的 `nav`。本网站仅包含教学文档及图片，不包含 SDR 运行库、大型录波或本地验证日志。讲义中的 Windows 工程路径用于解释本地工程，不是网页下载链接。

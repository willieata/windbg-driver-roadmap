# Ferry 课程目录学习路线 — 53 门课 / 1800+ 小节

以 **Ferry 学院(ferrycofc.com)** 的真实「课程目录」为素材,把 53 门课按各自的章节小节逐节铺开、从零基础起步的学习路线图。单一静态页面(`index.html`),用浏览器直接开启即可。

## 结构

三条路线、10 个模块、53 门课,每门课一张卡片,篇为小标题,**每个小节都是一个可勾选的断点圆点**:

- **Route A · 游戏安全**:逆向入门(C/C++、汇编、PE、注入/HOOK/绘制、工具)→ 常规逆向 → 虚幻实战 → Unity 实战
- **Route B · 全栈安全**:开发篇(C/C++/数据结构/WIN32/GUI)→ 逆向篇 → 内核篇
- **Route C · 驱动攻防(内核 · WinDbg 贯穿)**:保护模式 → 驱动开发 → 系统调用/进程线程 → 异步同步/内核对象/内存管理 → 调试异常(WinDbg/Dump/TTD)→ 实战拓展

勾选小节记录进度、每门课可写一则笔记、顶栏可导出/导入 JSON 备份。点击课程标题跳到对应的 Ferry 课程详情页。

> 目前 Route B / Route C 共 19 门课因抓取时网站限流(验证码)暂为占位,页面标注「目录待抓取」;真实目录补齐后重新生成即可。另有「无畏契约」因课程已下架无目录。

## 使用方式

直接开启 `index.html`,或透过 GitHub Pages 线上浏览。

> 进度勾选在 Claude Artifact 环境使用 `window.storage` API 保存;一般浏览器(含 GitHub Pages)自动 fallback 到 `localStorage`,存在本机,换装置/浏览器不会同步——用顶栏 export/import 搬移。

## 内容如何生成 / 补齐

内容由 `build/` 下的生成器产出,可复现:

- `build/course_<id>.json`:每门课的课程目录数据(章节 → 小节)。
- `build/gen.py`:读取全部 `course_*.json`,生成整个 `index.html`(含 CSS/JS)。

补齐占位课程:编辑对应的 `build/course_<id>.json`,填入 `chapters`(格式见既有文件),然后:

```bash
python build/gen.py
```

即可重新生成 `index.html`。

## 部署 / 更新

推送到 GitHub 后由 GitHub Pages(main branch, root)提供服务:

```bash
git add -A
git commit -m "update: 说明这次改了什么"
git push
```

## License

个人学习用途,内容为公开资讯整理,无特定授权限制。

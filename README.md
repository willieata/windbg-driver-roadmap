# WinDbg × Driver 除錯路線 — 29 週

從零開始的 Windows kernel driver 開發與 WinDbg 除錯學習路線,涵蓋:

- **Stage 1 — 地基補強(Week 1–13)**:C/C++ 進階、OS 基礎概念、x64 組語與 Calling Convention、Driver 開發入門(WDM/KMDF)
- **Stage 2 — WinDbg 除錯(Week 14–29)**:環境設定、Kernel Debug 環境、核心資料結構、IRP 追蹤、記憶體/IRQL、Dump 分析、Time Travel Debugging、反除錯整合

每週任務附官方文件 / 書籍章節等延伸資源,並可勾選追蹤進度(進度儲存在瀏覽器本機,透過 Claude Artifact 的 storage API)。

## 使用方式

直接開啟 `index.html`,或透過 GitHub Pages 線上瀏覽(見下方設定)。

> 注意:進度勾選功能(中斷點樣式的圓點)依賴 Claude.ai Artifact 的 `window.storage` API,單獨用瀏覽器開啟 `index.html`(非透過 Claude Artifact)時,勾選功能不會保存進度,但頁面排版與內容瀏覽不受影響。

## 部署到 GitHub Pages

1. 在 GitHub 建立一個新 repo(例如 `windbg-driver-roadmap`)
2. 在本機這個資料夾執行:
   ```bash
   git remote add origin https://github.com/<你的帳號>/windbg-driver-roadmap.git
   git branch -M main
   git push -u origin main
   ```
3. 到 repo 的 Settings → Pages → Source 選擇 `main` branch、`/ (root)`,存檔後幾分鐘內會產生網址

## 更新內容

之後每次要調整週次內容或補資源,直接編輯 `index.html`,然後:

```bash
git add -A
git commit -m "update: 說明這次改了什麼"
git push
```

## License

個人學習用途,內容為公開資訊整理,無特定授權限制。

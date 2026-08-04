# WinDbg × Driver 除錯路線 — 29 週

以 **Ferry 學院(ferrycofc.com)** 課程路徑為骨幹重排的學習路線,結合「全棧安全」與「驅動攻防」兩條支線,WinDbg 除錯貫穿內核階段:

- **Stage 1 — 開發篇(Week 1–10)**:C 語言與記憶體 → C++/泛型 → 資料結構 → Windows 核心編程(WIN32)→ 圖形界面(SDK/MFC/QT)
- **Stage 2 — 逆向篇(Week 11–17)**:組語與逆向入門(x86/x64、PE)→ 逆向提升(動態除錯)→ 逆向攻防(反調試、脫殼)
- **Stage 3 — 內核篇 · WinDbg 貫穿(Week 18–29)**:保護模式與除錯環境 → 驅動開發 → 系統調用/進程執行緒 → 異步同步/內核對象 → 內存管理 → 調試異常(Dump/TTD)→ 實戰拓展

每週琥珀色「»」開頭的是對應的 Ferry 課程模組,其下為微軟官方文件、看雪等輔助資源。可勾選追蹤進度、每週寫筆記,並用頂欄 export/import 備份。

## 使用方式

直接開啟 `index.html`,或透過 GitHub Pages 線上瀏覽(見下方設定)。

> 進度勾選(中斷點樣式的圓點)在 Claude Artifact 環境使用 `window.storage` API 保存;在一般瀏覽器(含 GitHub Pages)則自動 fallback 到 `localStorage`,進度存在本機瀏覽器,換裝置或換瀏覽器不會同步。

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

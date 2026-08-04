# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

單一靜態頁面(`index.html`)的學習路線圖,以 **Ferry 學院(ferrycofc.com)** 各課程的真實「課程目錄」為素材,把 53 門課按章節小節逐節鋪開。設計為 Claude Artifact / GitHub Pages 部署。無測試、無執行期依賴——直接用瀏覽器開啟 `index.html` 即可預覽。內容語言為簡繁混排的技術術語,以簡體課程名 + 繁體說明為主。

`index.html` 不是手寫維護的,而是由 `build/` 下的產生器輸出(見下)。約 300KB、1800+ 小節,手改不切實際——改內容請改資料再重新產生。

## 內容結構(3 路線 / 10 模組 / 53 課)

- **Route A · 遊戲安全**:逆向入門 → 常規逆向 → 虛幻實戰 → Unity 實戰
- **Route B · 全棧安全**:開發篇 → 逆向篇 → 內核篇
- **Route C · 驅動攻防(內核 · WinDbg 貫穿)**:保護模式 → 驅動開發 → 系統調用/進程執行緒 → 異步同步/內核對象/記憶體管理 → 調試異常 → 實戰拓展

Route B / Route C 共 19 門課目前為**佔位**(抓取時網站限流/驗證碼),`chapters:[]` + `note:"目录待抓取"`,頁面顯示為 `.empty`。另有 id=36「無畏契約」課程已下架。

## 產生器與資料(build/)

- `build/course_<id>.json`:每門課的目錄資料。schema:`{id, name, route, group, order, chapters:[{title, lessons:[...]}]}`;抓不到時 `chapters:[]` 並加 `note`。
- `build/gen.py`:讀取全部 `course_*.json`(依 `order` 排序,依 `route`→`group` 分組),產生整個 `index.html`(CSS/JS 全內嵌)。`ROUTE_ORDER` 決定路線順序;OUT 為 repo 內 `index.html` 絕對路徑。
- 補齊佔位課程:編輯對應 `course_<id>.json` 填入 `chapters`,執行 `python build/gen.py` 重新產生。
- ferrycofc 課程詳情頁 URL:`https://ferrycofc.com/index/course/show/id/<id>.html`。**注意**:並發抓取會觸發「訪問次數過多」驗證碼,對 IP 黏性封鎖(等待數十分鐘未必解除);要抓請串行低頻,或用瀏覽器過驗證。內核/驅動類課名還可能誤觸發模型的 cyber 安全防護(Opus/Sonnet 皆會),必要時降到較低推理模型或改用瀏覽器工具。

## index.html 結構(產生結果)

- **CSS**(`<style>`,頂部):WinDbg 深色主題,配色在 `:root` CSS 變數(`--cyan`/`--amber`/`--green`/`--red`/`--violet`)。
- **左側導覽欄**(`.rail`):`.rail-route` 路線標題 + 每模組一個 `.frame`,`data-target` 指向 `<section class="group" id="gN">`。
- **課程卡片**:`<article class="course" data-course="ID">`,內含 `.course-head`(標題連結 + `.course-prog` 進度徽章)、若干 `.chapter`(篇)、`.lessons > li.lesson`。每個 `li.lesson` 的 `data-id="L<courseid>_<n>"` **必須唯一**——它是進度儲存的 key。每卡片底部 `.course-note[data-note-id="NC<courseid>"]` 由 JS 注入筆記 UI。
- **JS**(`<script>`,底部):進度以勾選的 `.lesson` 計數;`.course-prog` 即時顯示每課完成數。

## 進度儲存機制

進度 key:`windbg-driver-roadmap-full:progress`(已完成 lesson `data-id` 的 JSON 陣列)。筆記 key:`windbg-driver-roadmap-full:notes`(`{NC<courseid>: 文字}`,**每門課一則**)。Claude Artifact 環境用 `window.storage`,否則 fallback 到 `localStorage`。頂欄 export/import 將兩者備份成 JSON(`format:'windbg-driver-roadmap-backup', version:1`),匯入成功後 `location.reload()`。

## 部署與更新

推送到 GitHub 後由 GitHub Pages(main branch, root)提供服務。更新流程:改 `build/` 資料 → `python build/gen.py` → commit + push(見 README)。

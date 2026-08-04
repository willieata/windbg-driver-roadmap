# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

單一靜態頁面(`index.html`)的 29 週 WinDbg / Windows kernel driver 除錯學習路線圖,設計為 Claude Artifact / GitHub Pages 部署。無 build、無測試、無依賴——直接用瀏覽器開啟 `index.html` 即可預覽。

所有內容(HTML、CSS、JS)都內嵌在 `index.html` 一個檔案裡,約 500 行。內容語言為繁體中文,修改文案時保持繁體中文與既有的技術術語混排風格。

## index.html 結構

- **CSS**(`<style>` 區塊,頂部):WinDbg 主題深色風格,配色定義在 `:root` CSS 變數(`--cyan`、`--amber`、`--green` 等)。
- **左側導覽欄**(`.rail`):每個 `.frame` 連結透過 `data-target` 指向對應的 `<section class="phase" id="pN">`。新增 phase 時兩邊要同步。
- **週次區塊**:每週是一個 `<div class="week" data-id="wN">`,含 `.bp`(中斷點樣式的完成勾選圓點)、`.wk-title`、說明段落與 `.res` 資源清單。`data-id` 必須唯一——它是進度儲存的 key。
- **JS**(`<script>` 區塊,底部):總週數由 `document.querySelectorAll('.week').length` 動態計算,新增/刪除週次不需要改 JS;但 README 與 `<footer>`、`<h1>` 中寫死的「29 週」字樣需要手動同步更新。

## 進度儲存機制

勾選進度的 key 為 `windbg-driver-roadmap-full:progress`。在 Claude Artifact 環境用 `window.storage` API 保存;一般瀏覽器(含 GitHub Pages)偵測不到該 API 時自動 fallback 到 `localStorage`。兩邊儲存格式相同(JSON 陣列的 `data-id` 列表)。

## 部署與更新

推送到 GitHub 後由 GitHub Pages(main branch, root)提供服務。內容更新流程就是直接編輯 `index.html` 後 commit + push(見 README)。

# 部署與待辦

> 簡報本體已完成並通過驗證（43 頁、零版面溢出、互動元件實測寫入雲端成功）。
> 只剩**發布 GitHub Pages** 需要你點頭 —— 那會建立一個公開 repo。

---

## 一、發布到 GitHub Pages（未執行）

本機 git 已初始化並 commit 完成，但**建立公開 repo 的動作被權限規則擋下**。

要發布，執行：

```bash
cd "G:/我的雲端硬碟/2026研習/2026數學科研習/taichung-math-agent-workshop" && gh repo create mathruffian-dot/taichung-math-agent-workshop --public --source=. --push --description "2026 臺中數學科研習：數位教學與 AI Agent（Reveal.js 互動簡報）"
```

然後開啟 Pages：

```bash
gh api repos/mathruffian-dot/taichung-math-agent-workshop/pages --method POST -f "source[branch]=master" -f "source[path]=/"
```

完成後網址是 `https://mathruffian-dot.github.io/taichung-math-agent-workshop/`（首次約 1–3 分鐘生效）。

> repo 必須是 **public**，GitHub Pages 免費版才會生效。

---

## 二、互動後端：Supabase（已接好，實測通過）

三個互動已從 Firebase 改接到 **Supabase `my-teaching-tools`**（ref `xxbjykdheracbfmwpxwm`）。
架構說明在上層專案的 `SUPABASE架構.md`，schema 在 `supabase/schema.sql`。

| 互動 | kind | slide_id |
|---|---|---|
| 破冰文字雲 | `wordcloud` | `intro` |
| 複選投票 | `poll` | `plan` |
| 數位力自評 | `selfcheck` | `digital-power` |

換一場研習只要改 `index.html` 裡這一行：

```js
const WORKSHOP_CODE = 'math-20260826';
```

### 實測結果（2026-08-25）

三個互動都實際寫入並讀回成功，狀態顯示「雲端同步」。資料長這樣：

```
wordcloud  intro          {"word": "GeoGebra"}
poll       plan           {"options": ["a", "c"]}
selfcheck  digital-power  {"items": ["t1","t2","m2"], "score": 3}
```

投票會寫多筆（每次點擊一筆完整選擇），讀取時取每人最新一筆 —— 這是刻意的設計，
`responses` 沒有 update/delete 權限，資料只進不改。

### 仍保留本機降級

雲端連不上時三個互動都會自動切「本機模式」（橘字標示），畫面照常運作，
只是沒有跨裝置同步。現場不會開天窗。

### ⚠️ 研習當天務必先確認

Supabase 免費方案**閒置會自動暫停**（2026-08-25 就發生過，兩個專案同時 INACTIVE、
DNS 直接解析不到）。當天先開一次簡報，看文字雲那頁是否顯示「雲端同步」；
若顯示「本機模式」就去 Supabase 後台手動恢復，約 1 分鐘可用。

## 三、現場備案（建議先準備）

研習現場網路與帳號額度是最大變數，六個 Demo 連結都已實測 200 OK，但仍建議：

| Demo | 備案 |
|---|---|
| 教材網頁（全六冊複習簡報） | 六個網址事先開好分頁，不要現場才載入 |
| 三款遊戲 | 事先各開一間房。遊戲跑在另一個 Firebase 專案（my-teaching-tools.web.app），與簡報互動的 Supabase 無關 |
| 會考題庫站 | 題庫站含全部詳解，**別投影到學生看得到的畫面** |
| 文字雲／投票／自評 | 已有本機模式降級，最壞情況也能講 |
| Canva 備用資料 | TPACK、SAMR、範例簡報三個連結，需要細講才點 |

---

## 檔案結構

```
taichung-math-agent-workshop/
├── index.html          # 簡報本體（43 頁，單檔，含 Supabase 互動）
├── build_icons.py      # 圖標總表裁切去背腳本（已執行完，留作紀錄）
├── DEPLOY.md           # 本檔
└── images/             # 6 張底圖 + 3 張遊戲橫幅 + 課本圖 + TPACK 圖 + 25 個扁平化圖示
```

本機預覽：

```bash
cd "G:/我的雲端硬碟/2026研習/2026數學科研習/taichung-math-agent-workshop" && python -m http.server 8765
```

然後開 `http://localhost:8765/`（改過檔案要加 `?v=2` 之類的參數避開快取）。

---

## 視覺設計筆記

為了不讓簡報看起來像生成式工具的預設輸出，做了這些收斂：

- **幾何銳利化**：卡片圓角 12px → 2～3px，不再是「氣泡」
- **光效收斂**：所有 drop-shadow 的半徑與濃度各砍一半
- **底色壓低**：半透明白底 0.05 → 0.03，頂線 4px → 2px
- **表格去色塊**：th 拿掉藍底，改細線 + 字距
- **引用框去底色**：只留左側 2px 強調線
- **字型**：拉丁字母與數字改用 Inter，中文走 PingFang TC／微軟正黑
- **版面識別**：標題左側 3px 豎線、左下角場次代碼、極淡背景網格（0.018 透明度）

配色沿用原本的橘＋青，沒有更動。

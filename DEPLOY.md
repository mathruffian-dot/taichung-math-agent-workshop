# 部署與待辦

> 簡報已發布上線，43 頁、零版面溢出、互動元件實測寫入雲端成功。
> 這份文件記錄部署資訊、現場備案與視覺設計筆記。

---

## 一、已發布 ✅

| | |
|---|---|
| **簡報網址** | https://mathruffian-dot.github.io/taichung-math-agent-workshop/ |
| **原始碼** | https://github.com/mathruffian-dot/taichung-math-agent-workshop（public） |
| 發布日期 | 2026-08-25 |

repo 必須是 public，GitHub Pages 免費版才會生效。

之後改了簡報要更新線上版，就是一般的 git 流程：

```bash
cd "G:/我的雲端硬碟/2026研習/2026數學科研習/taichung-math-agent-workshop" && git add -A && git commit -m "修改說明" && git push
```

推上去後約 1 分鐘生效。

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

### 現場怎麼看自評的全場結果

自評那頁（第 11 頁）有一顆 **「看全場結果」**，點了會蓋出統計面板：

- 已作答人數與平均分（滿分 9）
- **分數分布長條圖**（0–9 各有幾人）
- **九個項目的勾選率**，最低的那一格會標成琥珀色
- 底下自動生一句結論：「全場最空的一格是 ＿＿（只有 X% 的人勾）」

按「關閉」回到勾選畫面。送出新的自評時，若面板開著會自動重算。

### 事後想撈資料

Supabase 後台 SQL Editor：

```sql
-- 每人最新一筆（v_latest_responses 已經幫你去重）
select participant, payload->>'score' as score, payload->'items' as items, created_at
from public.v_latest_responses
where workshop_code = 'math-20260826' and kind = 'selfcheck'
order by created_at;

-- 各項目勾選率
select item, count(*) as n,
       round(count(*) * 100.0 / (select count(*) from public.v_latest_responses
                                 where workshop_code='math-20260826' and kind='selfcheck'), 1) as pct
from public.v_latest_responses, jsonb_array_elements_text(payload->'items') as item
where workshop_code = 'math-20260826' and kind = 'selfcheck'
group by item order by pct;
```

文字雲與投票也在同一張表，把 `kind` 換成 `wordcloud` 或 `poll` 即可。

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

視覺語言參考 `thinking-upgrade-20260707`（翻轉教育／親子天下場次）的 interactive-deck，
移植成**黑板 ＋ 粉筆 ＋ 紙卡**風格。

### 為什麼換

第一版是深色底＋霓虹青橘＋大圓角半透明卡片 —— 那是生成式 HTML 的招牌長相。
第二版只做細節收斂（圓角、光暈、底色），**骨架沒動所以觀感沒變**。
第三版直接換掉配色與敘事結構。

### 配色（粉筆色系，低飽和微暖）

| 用途 | 色值 |
|---|---|
| 黑板底 | `#1b222b` |
| 粉筆白（文字） | `#f2efe2` |
| 粉筆橘（主強調） | `#f2a37c` |
| 粉筆藍（次強調） | `#8fcdea` |
| 粉筆綠 | `#a8cf9a` |
| 粉筆黃 | `#f2dfa0` |
| 紙卡 | `#f8f3e6` |

### 移植的手法

- **噪點黑板底**：SVG `feTurbulence` 疊徑向漸層，中央微亮、邊角壓暗
- **手繪歪斜圓角**：`255px 15px 225px 15px / 15px 225px 15px 255px`，兩組交替，模擬手畫的框
- **標題波浪底線**：內嵌 SVG 手繪曲線，粉筆橘
- **eyebrow**：標題上方的小標（`PART 2｜做出課本沒有的`），字距 0.14em
- **takeaway**：每頁底部一句收束語，虛線上框分隔
- **虛線分隔**：表格標頭、收束語都改虛線

### 頁面敘事結構

```
eyebrow（這頁在整場的位置）
   ↓
h2（大標＋手繪波浪底線）
   ↓
內容
   ↓
takeaway（一句話收束）
```

37 頁有 eyebrow，11 頁有 takeaway（章節頁、封面、封底不加）。

### 沒有移植的

- **源石黑體**（GenSekiGothic2 TW）：字型檔 4.3 MB，研習現場網路載入會拖慢，改用 Inter ＋ 系統中文字型
- **紙卡翻轉動畫**與 `transform: rotate` 微旋轉：在 Reveal.js 960×700 的固定畫布下會撐大 bounding box 造成溢出，只保留手繪圓角

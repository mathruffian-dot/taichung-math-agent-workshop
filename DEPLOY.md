# 部署與待辦

> 簡報本體已完成並通過驗證（42 頁、零版面溢出、互動元件可運作）。
> 以下兩件事**需要你點頭**才能做，因為都會動到對外的服務。

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

## 二、Firestore 權限（⚠️ 目前互動元件走的是降級模式）

### 現況

實測 `teacherstudy-109ef` 這個 Firebase 專案，**線上規則目前拒絕所有前端讀寫**：

| 測試的集合 | 讀 | 寫 |
|---|---|---|
| `tcmath_wordcloud`（本簡報用） | DENIED | DENIED |
| `tcmath_poll`（本簡報用） | DENIED | DENIED |
| `tcmath_selfcheck`（本簡報用） | DENIED | DENIED |
| `wordcloud_words`（既有工具用） | DENIED | DENIED |
| `irs_responses`（既有工具用） | DENIED | DENIED |

值得注意的是：連 `wordcloud_words`、`irs_responses` 這些**在本機 `G:\我的雲端硬碟\2026database\firestore.rules` 白名單裡的集合也被拒**。

代表**線上規則和本機那份檔案不一致** —— 可能是規則被改過、或那份檔案從未部署。
其他也吃這個 Firebase 專案的工具（教師研習資料庫、既有文字雲頁面）**可能也是壞的**，值得一起確認。

### 目前的處理：自動降級

簡報不會因此開天窗。文字雲、投票、自評三個元件偵測到雲端不通時，都會自動切成**本機模式**：

- 狀態標示會從「連線中…」變成 **本機模式**（橘字）
- 輸入的詞／投的票／自評結果存在 localStorage，畫面照常運作
- 講者可以正常示範，只是**沒辦法全班同時投稿、你也收不到全場的自評分布**

### 要恢復全班即時互動

需要在 Firestore 規則加上這三個集合，然後部署：

```
    // 2026 臺中數學科研習簡報
    match /tcmath_wordcloud/{document} {
      allow read, write: if true;
    }
    match /tcmath_poll/{document} {
      allow read, write: if true;
    }
    match /tcmath_selfcheck/{document} {
      allow read, create: if true;
      allow update, delete: if false;
    }
```

三個集合分別對應：破冰文字雲、複選投票、**數位力自評送出**（只允許新增，不允許改別人的）。

⚠️ **部署前務必先確認線上規則的真實內容**（Firebase Console → Firestore → 規則）。
直接把本機那份檔案推上去，有可能會覆蓋掉線上比較新的設定。

確認後的部署指令：

```bash
cd "G:/我的雲端硬碟/2026database" && npx firebase-tools deploy --only firestore:rules --project teacherstudy-109ef
```

---

## 三、現場備案（建議先準備）

研習現場網路與帳號額度是最大變數，六個 Demo 連結都已實測 200 OK，但仍建議：

| Demo | 備案 |
|---|---|
| 教材網頁（八下整冊、二次函數） | 事先在瀏覽器開好分頁，不要現場才載入 |
| 三款遊戲 | 事先各開一間房，確認 Firebase 那側正常 |
| 會考題庫站 | 題庫站含全部詳解，**別投影到學生看得到的畫面** |
| 文字雲／投票 | 已有本機模式降級，最壞情況也能講 |

---

## 檔案結構

```
taichung-math-agent-workshop/
├── index.html          # 簡報本體（42 頁，單檔）
├── build_icons.py      # 圖標總表裁切去背腳本（已執行完，留作紀錄）
├── DEPLOY.md           # 本檔
└── images/             # 6 張底圖 + 11 個圖標
```

本機預覽：

```bash
cd "G:/我的雲端硬碟/2026研習/2026數學科研習/taichung-math-agent-workshop" && python -m http.server 8765
```

然後開 `http://localhost:8765/`（改過檔案要加 `?v=2` 之類的參數避開快取）。

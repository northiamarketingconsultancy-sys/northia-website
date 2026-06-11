# Northia Marketing Consultancy — Website

呢個 repo 係 Northia 官方網站嘅原始碼（純 HTML/CSS/JS，無需任何建置工具）。

## 檔案結構

| 檔案 | 用途 |
|---|---|
| `index.html` | 主頁（三語：EN / 繁 / 简） |
| `insights.html` | 文章列表頁 |
| `article-template.html` | 文章模板（發新文時複製呢個檔） |
| `sitemap.xml` | 俾 Google 收錄用 |
| `robots.txt` | 搜尋引擎設定 |
| `.nojekyll` | 話俾 GitHub Pages 知唔使用 Jekyll 處理 |

## 點樣用 GitHub Pages 上線（一次過設定）

1. 登入 GitHub → 右上角 **+** → **New repository**
2. Repository name 填 `northia-site`（或其他名），揀 **Public** → **Create repository**
3. 入到 repo → **Add file → Upload files** → 將呢度全部檔案拖入去 → **Commit changes**
4. 去 **Settings → Pages**（左邊選單）
5. **Source** 揀 `Deploy from a branch`，**Branch** 揀 `main` / `(root)` → **Save**
6. 等 1–2 分鐘，頁面頂部會出現你嘅網址：
   `https://你嘅用戶名.github.io/northia-site/`

## 之後點樣更新網站

直接喺 GitHub 網頁版改：撳入檔案 → 右上角鉛筆 ✏️ → 改完 **Commit changes** → 1 分鐘後自動更新上線。

## 發佈新文章（10 分鐘流程）

1. 喺 repo 撳 `article-template.html` → 右上角 **⋯ → Copy raw file**，或者撳 **Add file → Create new file**，檔名改做 `article-你嘅主題.html`，貼上模板內容
2. 跟住檔案入面 6 個 `✏️ EDIT` 標記改內容
3. 開 `insights.html`，複製一張 `<a class="card">` 卡片，改標題、摘要同連結，放最前
4. 開 `sitemap.xml`，加一行 `<url><loc>...</loc></url>`
5. Commit — 完成

## 駁自己嘅網域（買咗 domain 之後）

1. **Settings → Pages → Custom domain** 填 `www.你嘅域名.com` → Save
2. 去你嘅域名註冊商（Cloudflare / Porkbun / Namecheap）DNS 設定加：
   - `CNAME` 記錄：`www` → `你嘅用戶名.github.io`
   - 四條 `A` 記錄（指向 GitHub Pages，俾根域名用）：
     `185.199.108.153` / `185.199.109.153` / `185.199.110.153` / `185.199.111.153`
3. 返去 GitHub Pages 設定，剔 **Enforce HTTPS**（要等 DNS 生效，最多幾個鐘）
4. 最後：用編輯器「全部取代」將 5 個檔案入面嘅 `YOURDOMAIN.com` 換成真域名

## 上線前記得

- [ ] 換埋 Calendly 嵌入碼（`index.html` 同 `article-template.html` 入面有標記位置）
- [ ] 將案例數字（+340% ROI 等）換成真實數據
- [ ] 上線後去 Google Search Console 驗證網域 + 提交 sitemap

# Northia Marketing Consultancy — Website

純 HTML/CSS/JS 靜態網站，無需任何建置工具。

## 檔案結構

| 檔案 | 用途 |
|---|---|
| `index.html` | 主頁（三語 EN / 繁 / 简，含聯絡表格） |
| `case-studies.html` | 案例頁（4 個案例） |
| `insights.html` | 文章列表頁 |
| `article-*.html` × 5 | SEO 文章 |
| `article-template.html` | 文章模板（發新文時複製，唔好刪） |
| `assets/` | Logo 圖檔 |
| `sitemap.xml` / `robots.txt` | Google 收錄用 |
| `.nojekyll` | 防止 GitHub Pages 用 Jekyll 處理 |

## GitHub Pages 上線（一次過設定）

1. GitHub → **+** → **New repository** → 名 `northia-site` → **Public** → Create
2. **Add file → Upload files** → 全部檔案連 `assets` 資料夾拖入去 → **Commit changes**
3. **Settings → Pages** → Source 揀 `Deploy from a branch` → Branch `main` / `(root)` → Save
4. 等 1–2 分鐘：`https://你嘅用戶名.github.io/northia-site/`

## 重要：聯絡表格啟動（一次過）

表格用 FormSubmit 直接寄去 northiamarketingconsultancy@gmail.com。
網站上線後，**自己先填一次表格送出** → FormSubmit 會寄一封確認信去你 Gmail → 撳 **Activate**。之後所有訪客留言就會自動寄到你信箱。

## 發佈新文章（10 分鐘）

1. 複製 `article-template.html` → 改名 `article-你嘅主題.html`
2. 跟檔案入面 6 個 ✏️ EDIT 標記改內容
3. `insights.html` 複製一張卡片，改標題／摘要／連結，放最前
4. `sitemap.xml` 加一行 `<url>`
5. Commit

## 駁自己網域

1. Settings → Pages → Custom domain 填 `www.你嘅域名.com`
2. 域名商 DNS 加：CNAME `www` → `你嘅用戶名.github.io`，同四條 A 記錄：
   `185.199.108.153` / `185.199.109.153` / `185.199.110.153` / `185.199.111.153`
3. 開 Enforce HTTPS
4. 全部檔案入面 `YOURDOMAIN.com` 全部取代做真域名

## 上線前清單

- [ ] 換 Calendly 嵌入碼（index + 各 article 檔有 ✏️ 標記）
- [ ] 案例數字（主頁 +340% 等）換真實數據
- [ ] 自己填一次聯絡表格，啟動 FormSubmit
- [ ] Google Search Console 驗證 + 提交 sitemap

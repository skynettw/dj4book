# 快速學會Python架站技術：活用Django 4建構動態網站的16堂課
## 原始程式碼
## 歡迎讀者下載使用

 [博碩出版社連結](https://www.drmaster.com.tw/Bookinfo.asp?BookID=MP22259)
 
ISBN：9786263334090
規格：平裝 / 608頁 / 17 x 23 x 3.16 cm / 普通級 / 單色印刷 / 初版
出版地：台灣

本書的主要目標是希望Python初學者，可以在不需要高深程式設計技巧的情況下，運用最新的Django Web Framework製作出全功能的動態網站，輕易地運用各式各樣的模組，建構出實用的特色網站，並將在自己本地端練習的網站實際部署到網路主機上。大綱如下：

　　1.快速學習建立一個實用的Django網站
　　以一個小型的個人部落格網站開始，從如何建立網站開發環境、規劃網站需求以及設計資料庫的內容、快速建立頁面輸出模板以及資料庫存取，並學習部署到最受歡迎的各式主機。

　　2.Django架構深入剖析
　　詳細分析Django的MVC(MTV)架構。先在第4堂課做一個完整但是簡要的介紹，接著再分別就網址如何對應、如何設計模板、Model和資料庫之間的關係等等做深入的教學。

　　3.實用網站開發技巧
　　介紹特色網站所需使用到的技巧，包括如何快速建立表單以及表單與資料庫的自動結合，活用網站Session和使用者驗證技巧，快速建立可以讓使用者透過電子郵件自行註冊的會員網站，連結 Facebook進行驗證帳號的實務，以及結合社群網站帳號註冊及驗證的全方位會員網站。

　　4.實用網站開發教學
　　以每一堂課的內容實作建立不同網站，從設計、規劃到實作，一步步教導學習者在自己的主機環境建構出這些有趣實用的內容，包括迷你小電商網站、WordPress-like CMS管理網站、全功能電子商店網站、名言佳句產生器網站等等，最後再說明部署上線的注意事項以及網站單元測試範例。

## 2026-10-07 安全修補與相容環境

本次保留第 9 章 MongoDB 腳本與 `mshopa` 商城，沒有停用核心功能。這是兩個指定範例的局部修補，不是所有章節與依賴的完整安全稽核。GitHub 郵件 alert 727（PyMongo）與 731（Django）未提供 CVE，目前工具無法讀取警示詳細資訊，因此不宣稱已確認這兩個 alert 的精確對應或關閉狀態。

### 第 9 章：PyMongo

- `dj4ch09/dj4ch09/requirements.txt` 將 PyMongo 4.3.3 升至 **4.18.2**，dnspython 升至 **2.7.0**（新版 driver 要求至少 2.7.0）。
- 官方公告 [GHSA-vp6j-j7w5-5xjj](https://github.com/advisories/GHSA-vp6j-j7w5-5xjj) 與 [GHSA-v4x9-3549-crwv](https://github.com/advisories/GHSA-v4x9-3549-crwv) 均記錄 4.18.2 為修補版本；這不代表已確認 alert 727 屬於哪一項。
- 移除未使用的 `djongo`：本章 Django `DATABASES` 實際使用 SQLite；`mongo-db/*.py` 直接使用 PyMongo，沒有透過 djongo 將 Django ORM 接到 MongoDB。
- PyMongo 最低要求 Python 3.9、MongoDB Server 4.4。本章其餘原有固定套件適用 Python 3.9–3.11，勿將整份舊 requirements 裝入 Python 3.12。此次完整安裝與測試用 Python 3.9；日常教學應使用仍受官方支援的 Python／MongoDB 版本。參考 [官方升級指南](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/reference/upgrade/)。
- 四個 MongoDB 教學腳本的 list／insert／delete 呼叫皆以 mock 測試；URI 主機注入拒絕與一般 BSON 編解碼也通過。**沒有啟動或連接 MongoDB，未驗證實際伺服器、認證或資料讀寫**。BSON 巨量資料溢位公告以修補 driver 版本處理，測試不配置數 GB 記憶體重現。
- 本章 Django 4.1.5 與其他未列入本次修補的舊套件仍保留；不要把此章當作已全面升級的公開服務。

在獨立 venv 安裝此章 requirements；MongoDB 腳本會操作 `localhost:27017`，手動練習時只使用可丟棄的本地教學資料庫，不用正式資料。

### 商城：Django 5.2 LTS

- `mshopa` 使用 **Django 5.2.18 LTS**，最低 Python 3.10；此次驗證環境為 Python 3.12。Django 4.0 已停止支援，5.2 是此次採用的受支援 LTS 路線，不是已核實的 alert 731 最小修補版本。參考 [Django 官方下載／支援表](https://www.djangoproject.com/download/)。
- 升級必要的 allauth、filer、polymorphic、mptt、easy-thumbnails 與 Pillow，新增 allauth `AccountMiddleware`。保留原商城模型、網址、購物車與 PayPal 教學流程，並保留先前 PyJWT 2.14.0 修補。
- requirements 改列固定版本的直接執行依賴；移除舊環境 `pip freeze` 帶入的工具及間接套件 pin，避免 Python 3.12／Django 5.2 的解析衝突。pip 會解析必要的間接依賴；這不是完整 transitive lockfile。每章必須使用不同 venv，不要將商城依賴與第 9／11 章混裝。
- filer 3.x 已移除對 mptt 的內部依賴；本次仍保留原 `mptt` app 的相容版本。新版 filer 也限制部分上傳類型，3.6 預設不再安裝完整 SVG renderer；一般商品圖與欄位保留，需特殊 SVG 預覽時請依 [filer 升級指南](https://django-filer.readthedocs.io/en/latest/upgrading.html) 評估，不為恢復舊行為取消安全驗證。
- 既有 `0005_alter_product_image` 對預設 filer Image 改依賴明確的 `0001_initial`，避免附帶 SQLite 只套用部分合併遷移時誤判歷史不一致；自訂 Image model 仍走原 swappable dependency。

Windows 教學環境安裝與驗證（在 `mshopa` 目錄）：

```powershell
py -3.12 -m venv venv
.\venv\Scripts\python.exe -m pip install --index-url https://pypi.org/simple -r requirements.txt
.\venv\Scripts\python.exe -m pip check
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py test mysite --noinput
.\venv\Scripts\python.exe verify_sample_upgrade.py
# 使用附帶 SQLite 或既有練習資料前，先備份，再執行新版相依套件遷移：
Copy-Item -LiteralPath db.sqlite3 -Destination db.sqlite3.backup
.\venv\Scripts\python.exe manage.py migrate --noinput
.\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

此次只在附帶 SQLite 的可丟棄副本執行遷移，確認原商品、分類、訂單及訂單項目資料數量不變；repo 的 SQLite 檔案沒有修改。全新測試 DB 的遷移、商品列表／詳情、登入要求、購物車新增／移除、已驗證會員下單與本地郵件、登入／註冊頁、CSRF 防護及 PayPal 表單渲染皆有回歸測試。保留既有缺少 `static` 目錄與未排序分頁警告。

**未驗證正式 SMTP、Google／Facebook 真實 OAuth、付款或圖片上傳服務**；本地測試使用測試資料及記憶體郵件，不會連接這些外部服務。既有教學設定與付款程式仍需另行檢查才能公開部署，本次不宣稱整個商城或全部安全警示已修復。

repo 根目錄的離線回歸測試（使用具備對應套件的 venv）：

```text
python -m unittest discover -s tests -p test_pymongo_upgrade.py -v
python -m unittest discover -s tests -p test_pyjwt_security.py -v
```

### 商城：Pillow 與真實圖片驗證

- `mshopa/requirements.txt` 將 Pillow **10.4.0 → 12.3.0**，沿用 Python 3.10+；實測環境為 Windows / Python 3.12。此版本高於 [PSD 越界寫入漏洞的修補版本 12.1.1](https://github.com/advisories/GHSA-cfh3-3jmp-rvhc) 及 [FITS GZIP 解壓縮漏洞的修補版本 12.2.0](https://github.com/advisories/GHSA-whj4-6x5x-4v2j)。未重現這兩個原生解碼器漏洞的惡意樣本，亦未能讀取 GitHub 個別 Dependabot alert 的關閉狀態。
- 實際呼叫 filer 的管理員 multipart 上傳端點，在臨時目錄寫入圖片與縮圖，再用 Pillow 完整解碼：JPEG、PNG、GIF、WebP、PNG 透明度、EXIF 旋轉、動畫 GIF 原始幀、商品圖片 URL 與裁切縮圖均涵蓋。`manage.py test mysite --noinput` 包含這些測試，媒體儲存隔離，不修改原始 SQLite 或教學媒體。
- 測試揭露 filer 原先只檢查圖片尺寸，可能接受截斷 JPEG。新增四種點陣 MIME 類型的上傳 validator，在存檔前檢查檔案格式、完整性與每一幀的解碼，拒絕損壞圖片、偽造副檔名與超過 Pillow 像素安全限制的圖片；失敗回傳 HTTP 400，不留下檔案或資料列。上傳權限及 CSRF 也有回歸測試。保留既有 filer 其他格式的驗證規則。
- 本次未更動 requests / urllib3；這些既有相依套件的安全問題需另行處理。原 PyJWT、Django、PyMongo 修補及 SQLite 遷移相容處理均保留。測試為本地 Django 請求與檔案儲存流程，未測正式媒體伺服器或部署。

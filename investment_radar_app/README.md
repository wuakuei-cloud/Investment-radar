# 我的投資雷達 — 免費版 PWA

這是一個可安裝到 iPhone / Android 主畫面的獨立 PWA。

## 目前功能
- 我的最愛股票清單
- 持股股數、平均成本、資產配置
- 免費股價更新（yfinance / Yahoo Finance 非官方資料）
- 今日個股漲跌幅
- 今日資產損益
- 專屬新聞頁：只搜尋「我的最愛」股票
- 新聞使用 Google News 公開 RSS
- 手機資料存在瀏覽器 localStorage
- 可安裝到 iPhone 主畫面

## 股票代號例子
- 台股上市：2330.TW
- 台股上櫃：3130.TWO、5287.TWO
- 美股：ASML、NVDA
- 印尼：POWR.JK
- 泰國/馬來西亞：依 Yahoo Finance 對應代號輸入

## 在電腦啟動
需要 Python 3.10+

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

瀏覽器開：
http://127.0.0.1:8000

## iPhone 當獨立 App
PWA 要透過 HTTPS 才能完整安裝。把專案部署到 Render / Railway / Fly.io / 自己的 NAS HTTPS 網址後：
1. 用 Safari 打開網址
2. 分享
3. 加入主畫面
4. 之後會像獨立 App 一樣開啟

## 注意
yfinance 與 Google News RSS 都不是付費正式市場資料 API，可能延遲、限流或改版。
正式長期使用時，可以保留這個介面，再把後端資料源換成正式 API。

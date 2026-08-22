from flask import Flask, render_template, request, jsonify
import yfinance as yf
import feedparser
from urllib.parse import quote_plus
from datetime import datetime, timezone

app = Flask(__name__)

def normalize_symbol(symbol: str) -> str:
    return (symbol or "").strip().upper()

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/quote")
def quote():
    symbol = normalize_symbol(request.args.get("symbol"))
    if not symbol:
        return jsonify({"error": "missing symbol"}), 400

    try:
        ticker = yf.Ticker(symbol)
        fi = getattr(ticker, "fast_info", None)

        last = None
        prev = None
        currency = None
        if fi:
            try:
                last = float(fi["last_price"])
            except Exception:
                pass
            try:
                prev = float(fi["previous_close"])
            except Exception:
                pass
            try:
                currency = fi["currency"]
            except Exception:
                pass

        if last is None or prev is None:
            hist = ticker.history(period="5d", interval="1d", auto_adjust=False)
            if hist is None or hist.empty:
                return jsonify({"error": "no quote data", "symbol": symbol}), 404
            closes = [float(x) for x in hist["Close"].dropna().tolist()]
            if not closes:
                return jsonify({"error": "no quote data", "symbol": symbol}), 404
            last = closes[-1]
            prev = closes[-2] if len(closes) >= 2 else closes[-1]

        change = last - prev if prev else 0
        pct = (change / prev * 100) if prev else 0

        return jsonify({
            "symbol": symbol,
            "price": round(last, 4),
            "previousClose": round(prev, 4),
            "change": round(change, 4),
            "changePct": round(pct, 4),
            "currency": currency,
            "updatedAt": datetime.now(timezone.utc).isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e), "symbol": symbol}), 500

@app.get("/api/news")
def news():
    q = (request.args.get("q") or "").strip()
    if not q:
        return jsonify({"items": []})

    try:
        url = (
            "https://news.google.com/rss/search?q="
            + quote_plus(q)
            + "&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
        )
        feed = feedparser.parse(url)
        items = []
        for e in feed.entries[:20]:
            items.append({
                "title": e.get("title", ""),
                "link": e.get("link", ""),
                "published": e.get("published", ""),
                "source": (e.get("source") or {}).get("title", "") if isinstance(e.get("source"), dict) else ""
            })
        return jsonify({"items": items})
    except Exception as e:
        return jsonify({"error": str(e), "items": []}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

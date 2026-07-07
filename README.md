# ⚡ RParse: Rozetka Laptop Scraper (Async & Stealth)

An enterprise-grade, asynchronous web scraper specifically designed to extract product metadata from the laptops section of the **Rozetka** marketplace. 

Built on top of **Playwright Async**, this tool bypasses basic anti-bot systems by intercepting low-level backend API responses (`api/product/details`) instead of heavily relying on fragile HTML parsing.

---

## 🔥 Key Features

* **Asynchronous Architecture:** Utilizing `asyncio` and `playwright.async_api` for non-blocking I/O operations.
* **API Sniffing:** Intercepts JSON payloads directly from network responses, ensuring maximum data accuracy and structure speed.
* **Advanced Stealth Configuration:** * Injects JavaScript to neutralize the `navigator.webdriver` automation flag.
  * Emulates human-like scroll behavior (lazy loading trigger).
  * Customized user-agent, locale, and viewport setups to mitigate Cloudflare challenges.
* **Interactive ASCII Menu:** Clean, retro-style terminal interface before kicking off the engine.
* **Production-Ready Logging:** Structured logs with timestamps and severity levels instead of unmanaged stdout prints.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Core Engine:** Playwright (Async)
* **Data Format:** JSON
* **Environment:** Linux (Optimized for tailored setups like i3wm)

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone git@github.com:mynotnm-star/RParse-rozetka-parsing-laptop.git
cd RParse-rozetka-parsing-laptop
python3 main.py

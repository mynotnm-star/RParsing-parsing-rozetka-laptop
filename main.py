import asyncio
import json
import logging
import random
from typing import List, Dict, Any
from playwright.async_api import async_playwright, Response

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class RozetkaScraper:
    def __init__(self, base_page_count: int = 73):
        self.base_url = "https://rozetka.com.ua/ua/notebooks/c80004/page={}/"
        self.page_count = base_page_count
        self.all_products: List[Dict[str, Any]] = []
        
        # Anti-detection & Stealth configuration
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        self.chromium_args = [
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
            "--no-sandbox",
            "--disable-infobars"
        ]

    def menu(self):
        asciiart = '''
         ░█████████   ░█████████                                            
         ░██    ░██  ░██    ░██                                            
         ░██    ░██  ░██    ░██  ░██████    ░██░████  ░███████   ░███████  
         ░█████████   ░█████████         ░██    ░███      ░██        ░██    ░██ 
         ░██    ░██   ░██             ░███████  ░██       ░███████   ░█████████ 
         ░██    ░██  ░██             ░██   ░██  ░██                ░██ ░██      
         ░██     ░██  ░██            ░█████░██  ░██       ░███████    ░███████  
                                                                                 '''
        print(asciiart)
        print("=" * 68)
        print("                ROZETKA SPECTRE INTERCEPTOR v2.0              ")
        print("=" * 68)
        
        # Prompt user to choose whether to include the seller=other filter
        filter_choice = input('Use "seller=other" filter? (y/N): ').strip().lower()
        if filter_choice in ['y', 'yes']:
            self.base_url = "https://rozetka.com.ua/ua/notebooks/c80004/page={};seller=other/"
            logger.info("Seller filter enabled: seller=other")
            
        user_choice = input('Start parsing? (Y/n): ').strip().lower()
        if user_choice in ['y', 'yes', '']:
            logger.info("Starting extraction engine...")
        else:
            logger.info("Operation cancelled by user. Exiting.")
            exit()

    async def _json_sniffer(self, response: Response) -> None:
        """Intercepts network responses and extracts product metadata from API."""
        if "api/product/details" in response.url or "api" in response.url:
            try:
                payload = await response.json()
                if isinstance(payload, dict):
                    data = payload.get("data", [])
                    if isinstance(data, list):
                        for item in data:
                            product_info = {
                                "id": item.get("id"),
                                "title": item.get("title"),
                                "href": item.get("href"),
                                "price": item.get("price")
                            }
                            if product_info not in self.all_products and product_info.get("title"):
                                self.all_products.append(product_info)
                                logger.info(f"Intercepted product: {product_info['title'][:40]}...")
            except Exception:
                pass

    async def run(self) -> None:
        """Main execution loop for the asynchronous scraper."""
        async with async_playwright() as p:
            logger.info("Initializing stealth Chromium instance...")
            browser = await p.chromium.launch(headless=False, args=self.chromium_args)
            
            context = await browser.new_context(
                viewport=None,
                user_agent=self.user_agent,
                locale="uk-UA",
                timezone_id="Europe/Kyiv"
            )
            
            page = await context.new_page()
            
            # Neutralize navigator.webdriver flag
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Attach network sniffer
            page.on("response", self._json_sniffer)

            for page_num in range(1, self.page_count + 1):
                logger.info(f"Processing target page {page_num} of {self.page_count}")
                target_url = self.base_url.format(page_num)
                
                try:
                    await page.goto(target_url, wait_until="commit", timeout=25000)
                    await asyncio.sleep(random.uniform(2.0, 4.0))  # Human-like delay
                    
                    page_title = await page.title()
                    if "checking" in page_title.lower() or "just a moment" in page_title.lower():
                        logger.warning("Cloudflare challenge triggered! Waiting...")
                        await asyncio.sleep(6.0)

                    # Human-like scrolling to trigger lazy load and API requests
                    for _ in range(8):
                        await page.mouse.wheel(0, random.randint(300, 600))
                        await asyncio.sleep(random.uniform(0.5, 1.0))
                        
                except Exception as e:
                    logger.error(f"Execution failed on page {page_num}: {e}")
                    continue

            await browser.close()
            self._save_results()

    def _save_results(self) -> None:
        """Handles data persistence to local storage."""
        if self.all_products:
            output_file = "rozetka_clean_data.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(self.all_products, f, ensure_ascii=False, indent=4)
            logger.info(f"Scraping campaign successful. Saved {len(self.all_products)} products to {output_file}")
        else:
            logger.error("Dataset is empty. High anti-bot activity or breaking structural changes on host side.")

if __name__ == "__main__":
    scraper = RozetkaScraper(base_page_count=73)
    scraper.menu()
    asyncio.run(scraper.run())

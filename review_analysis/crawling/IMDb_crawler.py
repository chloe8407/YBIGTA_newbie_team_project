import logging
import re
import time
import datetime
import pandas as pd  # type: ignore[import-untyped]
from bs4 import BeautifulSoup  # type: ignore[import-untyped]
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from review_analysis.crawling.base_crawler import BaseCrawler



class IMDbCrawler(BaseCrawler):
    """
    Collects reviews for Zootopia (2016) from IMDb and saves them as a CSV file,
    including ratings, dates, and review content.
    """
    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        self.logger = logging.getLogger(__name__)
        self.base_url = 'https://www.imdb.com/title/tt2948356/reviews/'

        
    def start_browser(self):
        """
        Starts the browser and navigates to the IMDb reviews page.
        """
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Options())
        self.driver.get(self.base_url)
        self.logger.info("브라우저 실행 완료.")
        time.sleep(2)
        

    def load_until_target(self, target: int = 500, max_no_growth: int = 5, timeout: int = 10) -> int:
        """
        Repeatedly clicks the "Load More" button on the IMDb reviews page to load reviews
        up to the specified target count, verifying actual increases in review cards.

        Returns:
            int: The final number of loaded review cards.
        """
        wait = WebDriverWait(self.driver, timeout)

        def count_cards() -> int:
            """
            Counts the number of review cards currently loaded on the IMDb reviews page.

            Returns:
                int: The number of review card elements found in the DOM.
            """
            return len(self.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="review-card-parent"]'))

        no_growth = 0
        last_count = count_cards()

        try:
            wait.until(lambda d: count_cards() > 0)
        except TimeoutException:
            return 0

        while last_count < target and no_growth < max_no_growth:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            load_more = None
            selectors = [
                (By.CSS_SELECTOR, "button.ipc-see-more__button"),
                (By.XPATH, "//button[contains(@class,'ipc-see-more__button')]"),
            ]

            for by, sel in selectors:
                try:
                    load_more = wait.until(EC.presence_of_element_located((by, sel)))
                    break
                except TimeoutException:
                    continue

            if load_more is None:
                break

            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more)
                time.sleep(0.3)
                try:
                    load_more.click()
                except (StaleElementReferenceException, Exception):
                    self.driver.execute_script("arguments[0].click();", load_more)
            except Exception:
                break

            try:
                wait.until(lambda d: count_cards() > last_count)
                new_count = count_cards()
                last_count = new_count
                no_growth = 0
            except TimeoutException:
                no_growth += 1

        return last_count


    def scrape_reviews(self):
        """
        Scrapes reviews from the IMDb reviews page.

        This method loads reviews by interacting with the "Load More" button,
        extracts review ratings, dates, and content from the page,
        and stores the collected data in a pandas DataFrame.

        The scraping process stops once the target number of valid reviews is collected.
        """
        self.start_browser()

        target_save = 1000
        target_load = 2000

        loaded = self.load_until_target(target=target_load, max_no_growth=6, timeout=10)
        self.logger.info(f"로드된 리뷰 카드 수: {loaded}")

        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        items = soup.select('div[data-testid="review-card-parent"]')
        dates = soup.select('div[data-testid="reviews-author"] li.review-date')

        self.logger.info(f"items={len(items)}, dates={len(dates)}")

        reviews = []

        n = min(len(items), len(dates))
        for i in range(n):
            item = items[i]

            # date
            date = dates[i].get_text(strip=True)

            # rating
            rating = None
            rating_tag = item.select_one('span[aria-label*="rating"]') or item.select_one("span.review-rating")
            if rating_tag and rating_tag.has_attr("aria-label"):
                m = re.search(r"rating:\s*([\d.]+)", rating_tag["aria-label"])
                if not m:
                    m = re.search(r"\d+(\.\d+)?", rating_tag["aria-label"])
                rating = m.group(1) if (m and m.lastindex) else (m.group() if m else None)

            # content
            content_tag = item.select_one('div[data-testid="review-overflow"]') or item.select_one("div.ipc-overflowText")
            content = content_tag.get_text(strip=True) if content_tag else None

            if rating and date and content:
                try:
                    rating_f = float(rating)
                except Exception:
                    rating_f = None
                reviews.append({"rating": rating_f, "date": date, "comment": content})

            if len(reviews) >= target_save:
                break

        self.data = pd.DataFrame(reviews)

        def _parse_imdb_date(s: str) -> datetime.datetime | None:
            """
            Attempts to parse an IMDb review date string using multiple possible formats
            and converts it into a datetime object. Returns None if parsing fails.
            """
            s = (s or "").strip()
            for fmt in ("%d %B %Y", "%B %d, %Y", "%d %b %Y", "%b %d, %Y"):
                try:
                    return datetime.datetime.strptime(s, fmt)
                except ValueError:
                    continue
            return None
               
        self.data["date_dt"] = self.data["date"].apply(_parse_imdb_date)
        self.data = self.data.dropna(subset=["date_dt"])
        self.data = self.data.sort_values("date_dt", ascending=False)
        self.data["date"] = self.data["date_dt"].dt.strftime("%Y.%m.%d.")
        self.data = self.data[["rating", "date", "comment"]]
        self.logger.info(f"최종 수집: {len(self.data)}개")


    def save_to_database(self):
        """
        Saves the collected review data to a CSV file.
        """
        self.logger.info("save_to_database() called")

        if getattr(self, "data", None) is None or self.data.empty:
            self.logger.warning("저장할 데이터가 없습니다. (self.data가 비어있음)")
            if self.driver:
                self.driver.quit()
            return

        output_path = f"{self.output_dir}/reviews_imdb.csv"
        self.data.to_csv(output_path, index=False, encoding='utf-8-sig')
        self.logger.info(f"저장 완료: {output_path}")

        if self.driver:
            self.driver.quit()
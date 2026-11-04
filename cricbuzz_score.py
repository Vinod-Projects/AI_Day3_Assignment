import argparse

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


CRICBUZZ_URL = "https://www.cricbuzz.com/"
LIVE_SCORE_SELECTOR = ".text-cbLive"
SCORE_TIMEOUT_MS = 15_000


def capture_score(headless: bool = False) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        try:
            page = browser.new_page()
            response = page.goto(CRICBUZZ_URL, wait_until="domcontentloaded")
            if response is not None and response.status >= 400:
                raise RuntimeError(f"Cricbuzz returned HTTP {response.status}.")

            live_status = page.locator(LIVE_SCORE_SELECTOR).first
            try:
                live_status.wait_for(state="attached", timeout=SCORE_TIMEOUT_MS)
            except PlaywrightTimeoutError:
                if "access denied" in page.title().casefold():
                    raise RuntimeError("Cricbuzz denied this browser request.")
                print("No live match found on Cricbuzz.")
                page.screenshot(path="score.png")
            else:
                score_card = live_status.locator("xpath=..")
                print(score_card.inner_text().strip())
                score_card.screenshot(path="score.png")

            print("Saved screenshot to score.png")
        finally:
            browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Capture the latest live cricket score from Cricbuzz."
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="run Chromium without opening a browser window",
    )
    args = parser.parse_args()
    capture_score(headless=args.headless)


if __name__ == "__main__":
    main()

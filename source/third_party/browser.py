from abc import ABC

from playwright.sync_api import sync_playwright

class Browser(ABC):

    def __init__(self, page_address):
        self.page = None
        self.play = None
        self.page_address = page_address

    def start(self, headless: bool = True):
        self.play = sync_playwright().start()

        browser = self.play.firefox.launch_persistent_context(
            user_data_dir="/tmp/playwright",
            headless=headless,
        )
        if len(browser.pages) > 0:
            self.page = browser.pages[0]
        else:
            self.page = browser.new_page()

        self.page.goto(self.page_address)

    def stop(self):
        if self.play:
            self.play.stop()
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError
from third_party.browser import Browser

class Indeed(Browser):

    card_list_selector = "ul.jobsearch-ResultsList.css-0"
    job_description_selector = "#jobDescriptionText"
    company_name_selector = (
        "#jobsearch-ViewjobPaneWrapper > div > div > div > "
        "div.jobsearch-JobComponent-embeddedHeader > div > div > div:nth-child(1) > "
        "div.jobsearch-CompanyInfoContainer > div > div > div > div.css-1h46us2.eu4oa1w0 > "
        "div.css-kyg8or.eu4oa1w0 > div"
    )
    job_title_selector = (
        "#jobsearch-ViewjobPaneWrapper > div > div > div > "
        "div.jobsearch-JobComponent-embeddedHeader > div > div > div:nth-child(1) > "
        "div.jobsearch-JobInfoHeader-title-container > h2 > span"
    )
    job_location_selector = "div.css-6z8o9s:nth-child(2)"

    def __init__(self):
        super().__init__(page_address=None)


    def fetch_jobs(self, role: str, location: str) -> list:
        self.page_address = f"https://se.indeed.com/jobs?q={role}&l={location}"
        self.start()

        try:
            card_list = self.page.wait_for_selector(self.card_list_selector, timeout=5000)
            cards = card_list.query_selector_all("> *")
        except PlaywrightTimeoutError:
            self.stop()
            raise TimeoutError("No jobs found!")

        jobs_data = []

        for card in cards:
            
            job_data = {}

            if card.query_selector("div[id*='mosaic']"):
                continue

            try:
                card.click(timeout=2000)
            except PlaywrightTimeoutError:
                continue

            try:
                job_data["job_title"] = self.page.wait_for_selector(self.job_title_selector, timeout=4000).text_content()[0:-11]
            except PlaywrightTimeoutError:
                continue

            try:
                job_data["company_name"] = self.page.wait_for_selector(self.company_name_selector, timeout=4000).text_content()
            except PlaywrightTimeoutError:
                continue

            try:
                job_data["job_description"] = self.page.wait_for_selector(self.job_description_selector, timeout=4000).text_content()
            except PlaywrightTimeoutError:
                continue

            try:
                job_data["job_location"] = self.page.wait_for_selector(self.job_location_selector, timeout=4000).text_content()
            except PlaywrightTimeoutError:
                continue
                
            jobs_data.append(job_data)
        
        self.stop()
        return jobs_data

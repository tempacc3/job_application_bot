from third_party.browser import Browser
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError
from time import sleep

class Gmail(Browser):
    
    open_new_selector = '.T-I.T-I-KE.L3'
    to_selector = '.agP.aFw'
    subject_selector = 'input[name="subjectbox"]'
    content_selector = '.Am.Al.editable.LW-avf.tS-tW'
    send_selector = '.T-I.J-J5-Ji.aoO.v7.T-I-atl.L3'
    attachment_selector = '.a1.aaA.aMZ'

    def __init__(self):
        super().__init__(page_address="https://mail.google.com/#inbox")

    def send(self, application) -> list:
        try:
            self.page.wait_for_selector(self.open_new_selector, timeout=5000).click()
        except PlaywrightTimeoutError:
            raise TimeoutError("Failed to enter Gmail inbox, have you logged in?.")

        self.page.wait_for_selector(self.to_selector).fill(application["Email"])
        self.page.wait_for_selector(self.subject_selector).fill(application["Subject"])
        self.page.wait_for_selector(self.content_selector).type(application["Cover Letter"])

        with self.page.expect_file_chooser() as fc_info:
            self.page.wait_for_selector(self.attachment_selector).click()
        file_chooser = fc_info.value
        file_chooser.set_files(application["Resume Path"])
        self.page.wait_for_selector(self.send_selector).click()
        sleep(2)

